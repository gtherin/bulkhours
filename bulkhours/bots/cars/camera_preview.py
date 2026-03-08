import cv2
import time

from movement import advance_cm


def main():
    can_show = True
    try:
        cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
    except Exception:
        can_show = False
        print("OpenCV GUI backend unavailable. Running without preview window.")

    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    if cap.isOpened():
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_BRIGHTNESS, 100)

    use_picamera2 = False

    # Probe one frame. On newer Pi camera stacks, V4L2 may open but not stream.
    success, img = cap.read() if cap.isOpened() else (False, None)
    if not success or img is None:
        cap.release()
        try:
            from picamera2 import Picamera2
            picam2 = Picamera2()
            cfg = picam2.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"})
            picam2.configure(cfg)
            picam2.start()
            time.sleep(1.5)
            use_picamera2 = True
            print("Using Picamera2 backend")
        except Exception as exc:
            raise RuntimeError(
                "Camera opened but no frames via OpenCV V4L2. Install Picamera2: sudo apt install -y python3-picamera2"
            ) from exc

    while True:
        if use_picamera2:
            frame_rgb = None
            for _ in range(10):
                try:
                    frame_rgb = picam2.capture_array()
                except Exception:
                    frame_rgb = None
                if frame_rgb is not None:
                    break
                time.sleep(0.1)

            if frame_rgb is None:
                print("Picamera2 failed to capture frames. Check CSI cable orientation/seat and camera power.")
                break
            img = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
        else:
            success, img = cap.read()
            if not success or img is None:
                print("Camera frame read failed. Is another app using /dev/video0?")
                break

        if can_show:
            cv2.imshow("Video", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            # Keep the loop alive for headless capture mode.
            time.sleep(0.03)

    if use_picamera2:
        picam2.stop()
    else:
        cap.release()
    if can_show:
        cv2.destroyAllWindows()


def advance_10cm(px_obj, speed=50, cm_per_sec=20.0):
    """Convenience wrapper to reuse the shared move helper."""
    advance_cm(px_obj, distance_cm=10.0, speed=speed, cm_per_sec=cm_per_sec)

if __name__ == "__main__":
    main()