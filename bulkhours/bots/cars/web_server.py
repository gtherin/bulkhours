#!/usr/bin/env python3
import json
import urllib.request
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, PlainTextResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from robot_controller import RobotController

try:
    from vilib import Vilib
except Exception:  # pragma: no cover - runtime environment dependent
    Vilib = None

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "web" / "static"

app = FastAPI(title="PiCar-X Web Control")
robot = None
robot_error = ""
camera_stream_ready = False
camera_stream_error = ""

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


def _try_start_camera_stream() -> tuple[bool, str]:
    """Start Vilib web stream when available.

    Returns:
        (ready, error_message)
    """
    if Vilib is None:
        return False, "vilib is not available in the current Python environment"

    try:
        # Stream is served by Vilib at http://<pi-ip>:9000/mjpg.
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=False, web=True)
        return True, ""
    except Exception as exc:  # pragma: no cover - camera hardware dependent
        return False, str(exc)


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


@app.websocket("/ws")
async def ws_control(websocket: WebSocket) -> None:
    await websocket.accept()
    if robot is None:
        await websocket.send_json(
            {
                "type": "error",
                "error": f"Robot unavailable: {robot_error or 'unknown error'}",
            }
        )
        await websocket.close()
        return

    await websocket.send_json({"type": "state", "robot": robot.state()})

    try:
        while True:
            raw = await websocket.receive_text()
            msg = json.loads(raw)
            msg_type = msg.get("type")

            robot.heartbeat()

            if msg_type == "heartbeat":
                await websocket.send_json({"type": "heartbeat", "ok": True})
                continue

            if msg_type == "drive":
                throttle = int(msg.get("throttle", 0))
                steer = int(msg.get("steer", 0))
                robot.set_steer(steer)
                result = robot.drive(throttle)
                await websocket.send_json({"type": "drive_ack", "result": result})
                continue

            if msg_type == "camera":
                pan = msg.get("pan")
                tilt = msg.get("tilt")
                result = robot.set_camera(pan=pan, tilt=tilt)
                await websocket.send_json({"type": "camera_ack", "result": result})
                continue

            if msg_type == "recenter_camera":
                result = robot.recenter_camera()
                await websocket.send_json({"type": "camera_ack", "result": result})
                continue

            if msg_type == "stop":
                robot.stop()
                await websocket.send_json({"type": "stop_ack", "ok": True})
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
    global camera_stream_ready, camera_stream_error, robot, robot_error
    try:
        robot = RobotController(config_path=str(BASE_DIR / "picar-x.conf"))
        robot_error = ""
    except Exception as exc:  # pragma: no cover - hardware/process dependent
        robot = None
        robot_error = str(exc)

    camera_stream_ready, camera_stream_error = _try_start_camera_stream()
