#!/usr/bin/env python3
import threading
import time
import math
from pathlib import Path
from typing import Any, Dict

from robot_hat import Pin, Servo, utils as robot_hat_utils
from .picarx2 import Picarx


class RobotController(Picarx):
    """Single owner for PiCar-X hardware with watchdog safety."""

    def __init__(
        self,
        config_path: str | None = None,
        heartbeat_timeout_s: float = 1.2,
        pan_center: int = -2,
        tilt_center: int = 0,
    ) -> None:
        if config_path is None:
            config_path = str(Path.home() / ".config" / "picar-x" / "picar-x.conf")

        super().__init__(config=config_path)
        self._lock = threading.RLock()
        self._speed = 40
        self._steer = 0
        self._pan = pan_center
        self._tilt = tilt_center
        self._pan_center = pan_center
        self._tilt_center = tilt_center
        self._aux_servo = None
        self._aux_servo_center = 0
        self._aux_motion_thread = None
        self._user_led = None
        self._led_on = False

        # Optional user servo on P4. Keep startup resilient if not connected.
        try:
            self._aux_servo = Servo("P4")
            self._aux_servo.angle(self._aux_servo_center)
        except Exception:
            self._aux_servo = None

        # Optional onboard user LED exposed by Robot HAT as Pin("LED").
        try:
            self._user_led = Pin("LED")
            self._user_led.off()
            self._led_on = False
        except Exception:
            self._user_led = None
            self._led_on = False

        self._last_heartbeat = time.monotonic()
        self._heartbeat_timeout_s = heartbeat_timeout_s
        self._running = True

        # Move camera to known initial position.
        self.set_cam_pan_angle(self._pan_center)
        self.set_cam_tilt_angle(self._tilt_center)

        self._watchdog = threading.Thread(target=self._watchdog_loop, daemon=True)
        self._watchdog.start()

    @staticmethod
    def _clamp(value: int, low: int, high: int) -> int:
        return max(low, min(high, int(value)))

    def heartbeat(self) -> None:
        self._last_heartbeat = time.monotonic()

    def set_speed(self, speed: int) -> int:
        with self._lock:
            self._speed = self._clamp(speed, 0, 100)
            return self._speed

    def set_steer(self, angle: int) -> int:
        with self._lock:
            self._steer = self._clamp(angle, -35, 35)
            self.set_dir_servo_angle(self._steer)
            return self._steer

    def drive(self, throttle: int) -> Dict[str, int | str]:
        """Drive with signed throttle in range [-100, 100]."""
        with self._lock:
            t = self._clamp(throttle, -100, 100)
            speed = abs(t)
            self._speed = speed

            if t > 0:
                self.forward(speed)
                motion = "forward"
            elif t < 0:
                self.backward(speed)
                motion = "backward"
            else:
                self.stop()
                motion = "stop"

            return {"motion": motion, "speed": speed, "steer": self._steer}

    def stop(self) -> None:
        with self._lock:
            super().stop()

    def set_camera(self, pan: int | None = None, tilt: int | None = None) -> Dict[str, int]:
        with self._lock:
            if pan is not None:
                self._pan = self._clamp(pan, -60, 60)
                self.set_cam_pan_angle(self._pan)
            if tilt is not None:
                self._tilt = self._clamp(tilt, -35, 35)
                self.set_cam_tilt_angle(self._tilt)
            return {"pan": self._pan, "tilt": self._tilt}

    def recenter_camera(self) -> Dict[str, int]:
        return self.set_camera(pan=self._pan_center, tilt=self._tilt_center)

    def _agitate_aux_servo(self, safe_duration: float) -> None:
        """Run P4 servo agitation routine in background."""
        with self._lock:
            aux_servo = self._aux_servo
        if aux_servo is None:
            return

        try:
            # Smooth sinusoidal sweep around center.
            amplitude = 45.0
            frequency_hz = 5.0
            update_dt = 0.03
            start = time.monotonic()

            while True:
                elapsed = time.monotonic() - start
                if elapsed >= safe_duration:
                    break
                angle = int(round(amplitude * math.sin(2.0 * math.pi * frequency_hz * elapsed)))
                aux_servo.angle(angle)
                time.sleep(update_dt)
        finally:
            try:
                aux_servo.angle(0)
            except Exception:
                pass

    def turn_aux_servo_for(self, duration_s: float = 5.0) -> tuple[bool, str]:
        """Start smooth P4 left-right agitation for the given duration."""
        with self._lock:
            if self._aux_servo is None:
                return False, "Servo P4 unavailable"
            if self._aux_motion_thread is not None and self._aux_motion_thread.is_alive():
                return False, "Servo P4 is already moving"

        safe_duration = max(0.1, min(30.0, float(duration_s)))

        try:
            self._aux_motion_thread = threading.Thread(
                target=self._agitate_aux_servo,
                args=(safe_duration,),
                daemon=True,
            )
            self._aux_motion_thread.start()
            return True, f"Servo P4 agitation started for {safe_duration:.1f}s"
        except Exception as exc:
            return False, str(exc)

    def set_led(self, on: bool) -> tuple[bool, str]:
        with self._lock:
            if self._user_led is None:
                return False, "Onboard LED unavailable"
            try:
                if bool(on):
                    self._user_led.on()
                    self._led_on = True
                    return True, "LED on"
                self._user_led.off()
                self._led_on = False
                return True, "LED off"
            except Exception as exc:
                return False, str(exc)

    @staticmethod
    def _read_text(path: Path) -> str:
        try:
            return path.read_text(encoding="utf-8").strip()
        except Exception:
            return ""

    def _read_battery(self) -> Dict[str, Any]:
        # Prefer kernel power_supply metrics when available (UPS HAT, battery board, etc.).
        supplies_root = Path("/sys/class/power_supply")
        if supplies_root.exists():
            for dev in sorted(supplies_root.iterdir()):
                if not dev.is_dir():
                    continue

                cap_raw = self._read_text(dev / "capacity")
                volt_raw = self._read_text(dev / "voltage_now")
                status_raw = self._read_text(dev / "status")

                cap = None
                volt_v = None

                try:
                    if cap_raw:
                        cap = int(float(cap_raw))
                except Exception:
                    cap = None

                try:
                    if volt_raw:
                        # voltage_now is commonly in microvolts.
                        volt_v = float(volt_raw) / 1_000_000.0
                except Exception:
                    volt_v = None

                if cap is not None or volt_v is not None:
                    return {
                        "available": True,
                        "source": dev.name,
                        "percent": cap,
                        "voltage_v": volt_v,
                        "status": status_raw or None,
                    }

        # Fallback for Robot HAT: battery level is wired to ADC A4 (via divider).
        try:
            volt_v = float(robot_hat_utils.get_battery_voltage())
            if volt_v > 0:
                return {
                    "available": True,
                    "source": "robot_hat_a4",
                    "percent": None,
                    "voltage_v": volt_v,
                    "status": None,
                }
        except Exception:
            pass

        return {
            "available": False,
            "source": None,
            "percent": None,
            "voltage_v": None,
            "status": None,
        }

    def state(self) -> Dict[str, Any]:
        return {
            "speed": self._speed,
            "steer": self._steer,
            "pan": self._pan,
            "tilt": self._tilt,
            "heartbeat_timeout_s": self._heartbeat_timeout_s,
            "running": self._running,
            "led_on": self._led_on,
            "battery": self._read_battery(),
        }

    def shutdown(self) -> None:
        with self._lock:
            self._running = False
            super().stop()
            try:
                if self._user_led is not None:
                    self._user_led.off()
                    self._led_on = False
            except Exception:
                pass

    def _watchdog_loop(self) -> None:
        while self._running:
            elapsed = time.monotonic() - self._last_heartbeat
            if elapsed > self._heartbeat_timeout_s:
                # Safety stop if client disconnects or stops sending heartbeats.
                with self._lock:
                    super().stop()
            time.sleep(0.05)
