#!/usr/bin/env python3
import threading
import time
from pathlib import Path
from typing import Dict

from picarx import Picarx as PiCarX


class RobotController:
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

        self._px = PiCarX(config=config_path)
        self._lock = threading.RLock()
        self._speed = 40
        self._steer = 0
        self._pan = pan_center
        self._tilt = tilt_center
        self._pan_center = pan_center
        self._tilt_center = tilt_center

        self._last_heartbeat = time.monotonic()
        self._heartbeat_timeout_s = heartbeat_timeout_s
        self._running = True

        # Move camera to known initial position.
        self._px.set_cam_pan_angle(self._pan_center)
        self._px.set_cam_tilt_angle(self._tilt_center)

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
            self._px.set_dir_servo_angle(self._steer)
            return self._steer

    def drive(self, throttle: int) -> Dict[str, int | str]:
        """Drive with signed throttle in range [-100, 100]."""
        with self._lock:
            t = self._clamp(throttle, -100, 100)
            speed = abs(t)
            self._speed = speed

            if t > 0:
                self._px.forward(speed)
                motion = "forward"
            elif t < 0:
                self._px.backward(speed)
                motion = "backward"
            else:
                self._px.stop()
                motion = "stop"

            return {"motion": motion, "speed": speed, "steer": self._steer}

    def stop(self) -> None:
        with self._lock:
            self._px.stop()

    def set_camera(self, pan: int | None = None, tilt: int | None = None) -> Dict[str, int]:
        with self._lock:
            if pan is not None:
                self._pan = self._clamp(pan, -60, 60)
                self._px.set_cam_pan_angle(self._pan)
            if tilt is not None:
                self._tilt = self._clamp(tilt, -35, 35)
                self._px.set_cam_tilt_angle(self._tilt)
            return {"pan": self._pan, "tilt": self._tilt}

    def recenter_camera(self) -> Dict[str, int]:
        return self.set_camera(pan=self._pan_center, tilt=self._tilt_center)

    def state(self) -> Dict[str, int | float | bool]:
        return {
            "speed": self._speed,
            "steer": self._steer,
            "pan": self._pan,
            "tilt": self._tilt,
            "heartbeat_timeout_s": self._heartbeat_timeout_s,
            "running": self._running,
        }

    def shutdown(self) -> None:
        with self._lock:
            self._running = False
            self._px.stop()

    def _watchdog_loop(self) -> None:
        while self._running:
            elapsed = time.monotonic() - self._last_heartbeat
            if elapsed > self._heartbeat_timeout_s:
                # Safety stop if client disconnects or stops sending heartbeats.
                with self._lock:
                    self._px.stop()
            time.sleep(0.05)
