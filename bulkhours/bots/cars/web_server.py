#!/usr/bin/env python3
import asyncio
import json
import os
import shutil
import subprocess
import tempfile
import threading
import time
import urllib.request
from pathlib import Path
from typing import Any

import cv2
import numpy as np

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, PlainTextResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from robot_controller import RobotController

try:
    from vilib import Vilib
except Exception:  # pragma: no cover - runtime environment dependent
    Vilib = None
    _vilib_import_error = "initial import failed"
else:
    _vilib_import_error = ""

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "web" / "static"

app = FastAPI(title="PiCar-X Web Control")
robot = None
robot_error = ""
camera_stream_ready = False
camera_stream_error = ""
tts_engine = ""
tts_error = ""
music_player = ""
music_error = ""
music_file = ""
music_proc = None
vision_error = ""
detector_net = None
detector_init_error = ""
detect_cache_at = 0.0
detect_cache_payload: dict[str, Any] = {"ok": False, "objects": [], "detail": "not ready"}
detect_lock = threading.Lock()

MODEL_DIR = BASE_DIR / ".models"
MODEL_PROTO = MODEL_DIR / "mobilenet_ssd_deploy.prototxt"
MODEL_WEIGHTS = MODEL_DIR / "mobilenet_ssd.caffemodel"
MUSIC_DIR = Path.home() / "Music"

MOBILENET_CLASSES = [
    "background",
    "aeroplane",
    "bicycle",
    "bird",
    "boat",
    "bottle",
    "bus",
    "car",
    "cat",
    "chair",
    "cow",
    "diningtable",
    "dog",
    "horse",
    "motorbike",
    "person",
    "pottedplant",
    "sheep",
    "sofa",
    "train",
    "tvmonitor",
]

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


def _detect_tts_engine() -> tuple[str, str]:
    for cmd in ("espeak-ng", "espeak"):
        if shutil.which(cmd):
            return cmd, ""
    return "", "No TTS engine found. Install with: sudo apt install -y espeak-ng"


def _get_vilib():
    global Vilib, _vilib_import_error
    if Vilib is not None:
        return Vilib
    try:
        from vilib import Vilib as _Vilib
        Vilib = _Vilib
        _vilib_import_error = ""
        return Vilib
    except Exception as exc:  # pragma: no cover - runtime environment dependent
        _vilib_import_error = str(exc)
        return None


def _speak_text(text: str) -> tuple[bool, str]:
    cleaned = " ".join(str(text).strip().split())
    if not cleaned:
        return False, "empty text"
    if len(cleaned) > 240:
        cleaned = cleaned[:240]

    if not tts_engine:
        return False, tts_error or "TTS engine unavailable"

    try:
        env = dict(os.environ)
        env.setdefault("SDL_AUDIODRIVER", "alsa")

        # Synthesize to wav then play with ffplay to use the same audio path as working music playback.
        with tempfile.NamedTemporaryFile(prefix="picarx_tts_", suffix=".wav", delete=False) as f:
            wav_path = f.name

        subprocess.run([tts_engine, "-v", "fr", "-w", wav_path, cleaned], check=True)
        subprocess.run(
            ["ffplay", "-nodisp", "-autoexit", "-loglevel", "error", "-volume", "100", wav_path],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            env=env,
        )
        try:
            os.remove(wav_path)
        except Exception:
            pass
        return True, "spoken"
    except Exception as exc:
        return False, str(exc)


def _detect_music_player() -> tuple[str, str]:
    for cmd in ("ffplay", "aplay"):
        if shutil.which(cmd):
            return cmd, ""
    return "", "No player found. Install ffmpeg or alsa-utils"


def _list_music_files() -> list[Path]:
    if not MUSIC_DIR.exists():
        return []

    files = list(MUSIC_DIR.glob("*.mp3")) + list(MUSIC_DIR.glob("*.wav"))
    files.sort(key=lambda p: p.name.lower())
    return files


def _select_default_music() -> tuple[str, str]:
    if not MUSIC_DIR.exists():
        return "", f"Music directory not found: {MUSIC_DIR}"

    preferred = ["Emergency_Alarm.wav", "startup.mp3", "connected.mp3", "happy.wav"]
    for name in preferred:
        path = MUSIC_DIR / name
        if path.exists():
            return str(path), ""

    candidates = _list_music_files()
    if not candidates:
        return "", f"No .mp3/.wav files in {MUSIC_DIR}"
    return str(candidates[0]), ""


def _resolve_music_path(selected_name: str | None) -> tuple[str, str]:
    if selected_name is None:
        return music_file, ""

    wanted = str(selected_name).strip()
    if not wanted:
        return music_file, ""

    # Restrict selection to filenames from MUSIC_DIR only.
    for path in _list_music_files():
        if path.name == wanted:
            return str(path), ""
    return "", f"Music file not found: {wanted}"


def _play_music(selected_name: str | None = None) -> tuple[bool, str]:
    global music_proc, music_file
    if not music_player:
        return False, music_error or "music player unavailable"
    selected_path, select_error = _resolve_music_path(selected_name)
    if select_error:
        return False, select_error
    if not selected_path:
        return False, "no music file found"

    try:
        env = dict(os.environ)
        env.setdefault("SDL_AUDIODRIVER", "alsa")

        if music_proc is not None and music_proc.poll() is None:
            music_proc.terminate()

        if music_player == "ffplay":
            # Spawn detached playback so websocket remains responsive.
            music_proc = subprocess.Popen(
                [
                    "ffplay",
                    "-nodisp",
                    "-autoexit",
                    "-loglevel",
                    "error",
                    "-volume",
                    "100",
                    selected_path,
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                start_new_session=True,
                env=env,
            )
        else:
            music_proc = subprocess.Popen(
                ["aplay", selected_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                start_new_session=True,
                env=env,
            )
        music_file = selected_path
        return True, f"playing: {Path(selected_path).name} via {music_player}"
    except Exception as exc:
        return False, str(exc)


def _stop_music() -> tuple[bool, str]:
    global music_proc
    if music_proc is None or music_proc.poll() is not None:
        return True, "music already stopped"
    try:
        music_proc.terminate()
        music_proc = None
        return True, "music stopped"
    except Exception as exc:
        return False, str(exc)


def _try_start_camera_stream() -> tuple[bool, str]:
    """Start Vilib web stream when available.

    Returns:
        (ready, error_message)
    """
    vilib_mod = _get_vilib()
    if vilib_mod is None:
        detail = _vilib_import_error or "vilib is not available in the current Python environment"
        return False, f"vilib unavailable: {detail}"

    try:
        # Stream is served by Vilib at http://<pi-ip>:9000/mjpg.
        vilib_mod.camera_start(vflip=False, hflip=False)
        vilib_mod.display(local=False, web=True)
        return True, ""
    except Exception as exc:  # pragma: no cover - camera hardware dependent
        return False, str(exc)


def _detect_object_and_speak(timeout_s: float = 2.5) -> tuple[bool, str]:
    vilib_mod = _get_vilib()
    if vilib_mod is None:
        # No Vilib import: use OpenCV detector directly on MJPEG snapshot.
        ok, fallback_detail = _detect_object_opencv()
        if not ok:
            cause = _vilib_import_error or "unknown import error"
            return False, f"vilib unavailable ({cause}); fallback failed: {fallback_detail}"
        speak_ok, speak_detail = _speak_text(f"I see {fallback_detail}")
        if speak_ok:
            return True, f"detected: {fallback_detail}"
        return True, f"detected: {fallback_detail}, but TTS failed: {speak_detail}"

    if not camera_stream_ready:
        # Camera stream may still be externally available; try fallback detector anyway.
        ok, fallback_detail = _detect_object_opencv()
        if not ok:
            return False, f"camera stream not ready; fallback failed: {fallback_detail}"
        speak_ok, speak_detail = _speak_text(f"I see {fallback_detail}")
        if speak_ok:
            return True, f"detected: {fallback_detail}"
        return True, f"detected: {fallback_detail}, but TTS failed: {speak_detail}"

    try:
        vilib_mod.image_classify_switch(True)
        start = time.monotonic()
        label = ""
        acc = 0.0

        while time.monotonic() - start < timeout_s:
            params = getattr(vilib_mod, "image_classification_obj_parameter", {}) or {}
            label = str(params.get("name", "")).strip()
            acc = float(params.get("acc", 0.0) or 0.0)
            if label:
                break
            time.sleep(0.1)

        vilib_mod.image_classify_switch(False)

        if not label:
            # Fallback when tflite_runtime is unavailable: OpenCV DNN on current frame.
            ok, fallback_detail = _detect_object_opencv()
            if not ok:
                return False, fallback_detail
            label = fallback_detail
            acc = 1.0

        sentence = f"I see {label}"
        speak_ok, speak_detail = _speak_text(sentence)
        if speak_ok:
            return True, f"detected: {label} ({acc:.2f})"
        return True, f"detected: {label} ({acc:.2f}), but TTS failed: {speak_detail}"
    except Exception as exc:
        # Common on this setup: missing tflite_runtime in Vilib image classifier.
        err = str(exc)
        if "tflite_runtime" in err:
            ok, fallback_detail = _detect_object_opencv()
            if not ok:
                return False, f"{err}; fallback failed: {fallback_detail}"
            speak_ok, speak_detail = _speak_text(f"I see {fallback_detail}")
            if speak_ok:
                return True, f"detected: {fallback_detail}"
            return True, f"detected: {fallback_detail}, but TTS failed: {speak_detail}"
        return False, err


def _ensure_detector() -> tuple[bool, str]:
    global detector_net, detector_init_error
    if detector_net is not None:
        return True, ""

    # OpenCV DNN init is not reliably thread-safe on this ARM setup.
    with detect_lock:
        if detector_net is not None:
            return True, ""

        try:
            MODEL_DIR.mkdir(parents=True, exist_ok=True)

            if not MODEL_PROTO.exists():
                urllib.request.urlretrieve(
                    "https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/master/deploy.prototxt",
                    str(MODEL_PROTO),
                )
            if not MODEL_WEIGHTS.exists():
                urllib.request.urlretrieve(
                    "https://github.com/chuanqi305/MobileNet-SSD/raw/master/mobilenet_iter_73000.caffemodel",
                    str(MODEL_WEIGHTS),
                )

            detector_net = cv2.dnn.readNetFromCaffe(str(MODEL_PROTO), str(MODEL_WEIGHTS))
            detector_init_error = ""
            return True, ""
        except Exception as exc:
            detector_net = None
            detector_init_error = str(exc)
            return False, detector_init_error


def _detect_object_opencv(conf_threshold: float = 0.45) -> tuple[bool, str]:
    ok, objects, detail = _detect_objects_opencv(conf_threshold=conf_threshold)
    if not ok:
        return False, detail
    if not objects:
        return False, "no object detected"
    return True, str(objects[0]["label"])


def _detect_objects_opencv(conf_threshold: float = 0.45) -> tuple[bool, list[dict[str, Any]], str]:
    ok, err = _ensure_detector()
    if not ok:
        return False, [], f"detector unavailable: {err}"

    try:
        frame = None

        # Prefer MJPEG snapshot when available.
        try:
            with urllib.request.urlopen("http://127.0.0.1:9000/mjpg.jpg", timeout=2) as resp:
                jpg = resp.read()
            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        except Exception:
            frame = None

        # If Vilib stream is unavailable, read one frame directly from camera.
        # Avoid opening /dev/video0 concurrently when Vilib already owns the camera.
        if frame is None:
            if camera_stream_ready:
                return False, [], "cannot read MJPEG snapshot while Vilib camera is active"
            cap = cv2.VideoCapture(0)
            try:
                ok_cap, img = cap.read()
                if ok_cap and img is not None:
                    frame = img
            finally:
                cap.release()

        if frame is None:
            return False, [], "cannot read camera frame (mjpg and /dev/video0 failed)"

        h, w = frame.shape[:2]

        blob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)),
            0.007843,
            (300, 300),
            127.5,
        )
        detector_net.setInput(blob)
        detections = detector_net.forward()

        objects: list[dict[str, Any]] = []
        for i in range(detections.shape[2]):
            conf = float(detections[0, 0, i, 2])
            idx = int(detections[0, 0, i, 1])
            if conf < conf_threshold or not (0 <= idx < len(MOBILENET_CLASSES)):
                continue

            x1 = int(detections[0, 0, i, 3] * w)
            y1 = int(detections[0, 0, i, 4] * h)
            x2 = int(detections[0, 0, i, 5] * w)
            y2 = int(detections[0, 0, i, 6] * h)

            x1 = max(0, min(w - 1, x1))
            y1 = max(0, min(h - 1, y1))
            x2 = max(0, min(w - 1, x2))
            y2 = max(0, min(h - 1, y2))
            if x2 <= x1 or y2 <= y1:
                continue

            objects.append(
                {
                    "label": MOBILENET_CLASSES[idx],
                    "confidence": conf,
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2,
                    "w": w,
                    "h": h,
                }
            )

        objects.sort(key=lambda obj: float(obj["confidence"]), reverse=True)

        if not objects:
            return False, [], "no object detected"
        return True, objects, "ok"

    except Exception as exc:
        return False, [], str(exc)


def _detect_snapshot(min_interval_s: float = 0.6) -> dict[str, Any]:
    global detect_cache_at, detect_cache_payload
    now = time.monotonic()
    if now - detect_cache_at < min_interval_s and detect_cache_payload:
        return detect_cache_payload

    # Keep one detector run at a time: concurrent OpenCV DNN forwards can crash here.
    if not detect_lock.acquire(blocking=False):
        if detect_cache_payload:
            return detect_cache_payload
        return {
            "ok": False,
            "objects": [],
            "detail": "detection busy",
            "ts": time.time(),
        }

    try:
        now = time.monotonic()
        if now - detect_cache_at < min_interval_s and detect_cache_payload:
            return detect_cache_payload

        ok, objects, detail = _detect_objects_opencv(conf_threshold=0.45)
        payload: dict[str, Any] = {
            "ok": ok,
            "objects": objects,
            "detail": detail,
            "ts": time.time(),
        }
        detect_cache_at = now
        detect_cache_payload = payload
        return payload
    finally:
        detect_lock.release()


@app.get("/")
def index() -> FileResponse:
    return FileResponse(str(STATIC_DIR / "index.html"))


@app.get("/api/health")
def health() -> dict:
    return {
        "ok": True,
        "robot_ready": robot is not None,
        "robot_error": robot_error,
        "robot": robot.state() if robot is not None else None,
        "tts_ready": bool(tts_engine),
        "tts_engine": tts_engine,
        "tts_error": tts_error,
        "music_ready": bool(music_player and music_file),
        "music_player": music_player,
        "music_file": music_file,
        "music_error": music_error,
        "vision_ready": camera_stream_ready and Vilib is not None,
        "vision_error": vision_error,
    }


@app.get("/api/camera")
def camera_status() -> dict:
    return {
        "ready": camera_stream_ready,
        "error": camera_stream_error,
        "stream_path": "/mjpg",
        "stream_port": 9000,
        "proxy_path": "/video_feed",
    }


@app.get("/api/music")
def music_catalog() -> dict[str, Any]:
    files = [path.name for path in _list_music_files()]
    current_name = Path(music_file).name if music_file else ""
    return {
        "files": files,
        "current": current_name,
        "ready": bool(music_player),
        "error": music_error,
    }


@app.get("/api/detect_snapshot")
def detect_snapshot() -> dict[str, Any]:
    # Keep detection frequency low for CPU budget on Raspberry Pi.
    return _detect_snapshot(min_interval_s=0.6)


@app.get("/video_feed")
def video_feed():
    """Proxy Vilib MJPEG stream through same origin for browser compatibility."""
    upstream = "http://127.0.0.1:9000/mjpg"

    def stream_chunks():
        with urllib.request.urlopen(upstream, timeout=5) as resp:
            while True:
                chunk = resp.read(8192)
                if not chunk:
                    break
                yield chunk

    try:
        with urllib.request.urlopen(upstream, timeout=5) as resp:
            content_type = resp.headers.get(
                "Content-Type", "multipart/x-mixed-replace; boundary=frame"
            )
        return StreamingResponse(stream_chunks(), media_type=content_type)
    except Exception as exc:
        return PlainTextResponse(f"camera proxy error: {exc}", status_code=503)


@app.get("/video_feed_jpg")
def video_feed_jpg():
    """Proxy the latest JPEG frame for low-latency polling mode."""
    upstream = "http://127.0.0.1:9000/mjpg.jpg"
    try:
        with urllib.request.urlopen(upstream, timeout=2) as resp:
            jpg = resp.read()
        return StreamingResponse(
            iter([jpg]),
            media_type="image/jpeg",
            headers={
                "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
                "Pragma": "no-cache",
                "Expires": "0",
            },
        )
    except Exception as exc:
        return PlainTextResponse(f"camera jpg proxy error: {exc}", status_code=503)


@app.websocket("/ws")
async def ws_control(websocket: WebSocket) -> None:
    await websocket.accept()
    await websocket.send_json(
        {
            "type": "state",
            "robot": robot.state() if robot is not None else None,
            "robot_ready": robot is not None,
            "robot_error": robot_error,
            "tts_ready": bool(tts_engine),
            "tts_engine": tts_engine,
        }
    )

    try:
        while True:
            raw = await websocket.receive_text()
            msg = json.loads(raw)
            msg_type = msg.get("type")

            if robot is not None:
                robot.heartbeat()

            if msg_type == "heartbeat":
                await websocket.send_json({"type": "heartbeat", "ok": True})
                continue

            if msg_type == "drive":
                if robot is None:
                    await websocket.send_json(
                        {"type": "error", "error": f"Robot unavailable: {robot_error or 'unknown error'}"}
                    )
                    continue
                throttle = int(msg.get("throttle", 0))
                steer = int(msg.get("steer", 0))
                robot.set_steer(steer)
                result = robot.drive(throttle)
                await websocket.send_json({"type": "drive_ack", "result": result})
                continue

            if msg_type == "camera":
                if robot is None:
                    await websocket.send_json(
                        {"type": "error", "error": f"Robot unavailable: {robot_error or 'unknown error'}"}
                    )
                    continue
                pan = msg.get("pan")
                tilt = msg.get("tilt")
                result = robot.set_camera(pan=pan, tilt=tilt)
                await websocket.send_json({"type": "camera_ack", "result": result})
                continue

            if msg_type == "recenter_camera":
                if robot is None:
                    await websocket.send_json(
                        {"type": "error", "error": f"Robot unavailable: {robot_error or 'unknown error'}"}
                    )
                    continue
                result = robot.recenter_camera()
                await websocket.send_json({"type": "camera_ack", "result": result})
                continue

            if msg_type == "stop":
                if robot is not None:
                    robot.stop()
                await websocket.send_json({"type": "stop_ack", "ok": True})
                continue

            if msg_type == "speak":
                text = msg.get("text", "")
                ok, detail = await asyncio.to_thread(_speak_text, text)
                await websocket.send_json({"type": "speak_ack", "ok": ok, "detail": detail})
                continue

            if msg_type == "play_music":
                selected = msg.get("file")
                ok, detail = await asyncio.to_thread(_play_music, selected)
                await websocket.send_json({"type": "music_ack", "ok": ok, "detail": detail})
                continue

            if msg_type == "stop_music":
                ok, detail = await asyncio.to_thread(_stop_music)
                await websocket.send_json({"type": "music_ack", "ok": ok, "detail": detail})
                continue

            if msg_type == "detect_object":
                snapshot = await asyncio.to_thread(_detect_snapshot, 0.0)
                objects = snapshot.get("objects") or []
                if snapshot.get("ok") and objects:
                    label = str(objects[0].get("label", "object"))
                    speak_ok, speak_detail = await asyncio.to_thread(_speak_text, f"I see {label}")
                    detail = f"detected: {label}"
                    if not speak_ok:
                        detail = f"{detail}, but TTS failed: {speak_detail}"
                    await websocket.send_json({"type": "detect_ack", "ok": True, "detail": detail})
                else:
                    detail = str(snapshot.get("detail") or "no object detected")
                    await websocket.send_json({"type": "detect_ack", "ok": False, "detail": detail})
                continue

            if msg_type == "servo4_turn":
                if robot is None:
                    await websocket.send_json(
                        {"type": "error", "error": f"Robot unavailable: {robot_error or 'unknown error'}"}
                    )
                    continue
                ok, detail = robot.turn_aux_servo_for(5.0)
                await websocket.send_json({"type": "servo4_ack", "ok": ok, "detail": detail})
                continue

            if msg_type == "led":
                if robot is None:
                    await websocket.send_json(
                        {"type": "error", "error": f"Robot unavailable: {robot_error or 'unknown error'}"}
                    )
                    continue
                on = bool(msg.get("on", False))
                ok, detail = robot.set_led(on)
                await websocket.send_json({"type": "led_ack", "ok": ok, "detail": detail})
                continue

            await websocket.send_json({"type": "error", "error": f"Unknown type: {msg_type}"})
    except WebSocketDisconnect:
        if robot is not None:
            robot.stop()


@app.on_event("shutdown")
def on_shutdown() -> None:
    if Vilib is not None and camera_stream_ready:
        try:
            Vilib.camera_close()
        except Exception:
            pass
    if robot is not None:
        robot.shutdown()


@app.on_event("startup")
def on_startup() -> None:
    global camera_stream_ready, camera_stream_error, robot, robot_error, tts_engine, tts_error
    global music_player, music_error, music_file, vision_error
    try:
        robot = RobotController(config_path=str(BASE_DIR / "picar-x.conf"))
        robot_error = ""
    except Exception as exc:  # pragma: no cover - hardware/process dependent
        robot = None
        robot_error = str(exc)

    tts_engine, tts_error = _detect_tts_engine()
    music_player, music_error = _detect_music_player()
    music_file, file_error = _select_default_music()
    if file_error:
        music_error = f"{music_error}; {file_error}" if music_error else file_error

    camera_stream_ready, camera_stream_error = _try_start_camera_stream()
    vision_error = camera_stream_error
