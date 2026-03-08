#!/usr/bin/env python3
import argparse
import json
import queue
import re
import time
from pathlib import Path

import sounddevice as sd
from vosk import KaldiRecognizer, Model

from picarx import Picarx as PiCarX
from movement import advance_cm


def normalize_asr_text(text):
    normalized = text.lower().replace(",", ".")
    # Common ASR confusions observed on-device.
    replacements = {
        "picard": "picar",
        "pica": "picar",
        "absence": "avance",
        "avence": "avance",
        "rue de": "recule de",
        "recul": "recule",
        "centimes": "cm",
        "centimètre": "cm",
        "centimètres": "cm",
        "centimetre": "cm",
        "centimetres": "cm",
    }
    for k, v in replacements.items():
        normalized = normalized.replace(k, v)
    return normalized


def parse_distance_cmd(text, default_distance_cm=10.0):
    """Extract distance command from French text.

    Supported examples:
    - "avance de 15 cm"
    - "recule de 10 centimetres"
    """
    normalized = normalize_asr_text(text)
    # Accept common spoken French numbers from Vosk output.
    word_to_num = {
        "zero": "0",
        "un": "1",
        "deux": "2",
        "trois": "3",
        "quatre": "4",
        "cinq": "5",
        "six": "6",
        "sept": "7",
        "huit": "8",
        "neuf": "9",
        "dix": "10",
        "onze": "11",
        "douze": "12",
        "treize": "13",
        "quatorze": "14",
        "quinze": "15",
        "seize": "16",
        "vingt": "20",
        "trente": "30",
    }
    for word, num in word_to_num.items():
        normalized = re.sub(rf"\b{word}\b", num, normalized)
    m = re.search(r"\b(avance|recule)\s+de\s+(\d+(?:\.\d+)?)\s*(cm)?\b", normalized)
    if not m:
        # Fallback for imperfect transcripts like "picar avance" or "picar recule de cm".
        m2 = re.search(r"\b(avance|recule)\b", normalized)
        if not m2:
            return None
        return m2.group(1), float(default_distance_cm)
    action = m.group(1)
    distance_cm = float(m.group(2))
    return action, distance_cm


def extract_after_wake_word(text, wake_words):
    normalized = normalize_asr_text(text).replace(",", " ")
    pattern = r"\\b(" + "|".join(re.escape(w.lower()) for w in wake_words) + r")\\b"
    m = re.search(pattern, normalized)
    if not m:
        return None
    return normalized[m.end():].strip()


def main():
    parser = argparse.ArgumentParser(description="French voice control for PiCar-X")
    parser.add_argument(
        "--model-dir",
        default=str(Path.home() / "models" / "vosk-fr"),
        help="Path to unpacked Vosk French model directory",
    )
    parser.add_argument(
        "--samplerate",
        type=int,
        default=None,
        help="Microphone sample rate (default: auto from selected input device)",
    )
    parser.add_argument("--speed", type=int, default=50, help="Forward/backward speed")
    parser.add_argument("--cm-per-sec", type=float, default=20.0, help="Distance calibration constant")
    parser.add_argument("--mic-device", type=int, default=None, help="Optional input device index")
    parser.add_argument("--wake-word", default="picar", help="Wake word required to execute a command")
    parser.add_argument(
        "--wake-variants",
        default="picard,pica",
        help="Comma-separated additional wake variants accepted by ASR",
    )
    parser.add_argument("--default-distance-cm", type=float, default=10.0, help="Fallback distance when ASR misses the number")
    args = parser.parse_args()

    model_path = Path(args.model_dir)
    if not model_path.exists():
        raise FileNotFoundError(
            f"Vosk model not found at {model_path}. Download a French model and unpack there."
        )

    config_path = Path.home() / ".config" / "picar-x" / "picar-x.conf"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    px = PiCarX(config=str(config_path))

    input_info = sd.query_devices(args.mic_device, "input")
    detected_sr = int(input_info["default_samplerate"])
    stream_sr = int(args.samplerate) if args.samplerate else detected_sr

    model = Model(str(model_path))
    recognizer = KaldiRecognizer(model, stream_sr)
    wake_words = [args.wake_word] + [w.strip() for w in args.wake_variants.split(",") if w.strip()]
    audio_q = queue.Queue(maxsize=8)
    last_overflow_warn = 0.0

    def audio_callback(indata, frames, time_info, status):
        nonlocal last_overflow_warn
        if status and getattr(status, "input_overflow", False):
            now = time.monotonic()
            if now - last_overflow_warn > 2.0:
                print("Warning: input overflow (audio too slow).")
                last_overflow_warn = now
        try:
            audio_q.put_nowait(bytes(indata))
        except queue.Full:
            # Drop oldest chunk to keep command latency low.
            try:
                audio_q.get_nowait()
            except queue.Empty:
                pass
            audio_q.put_nowait(bytes(indata))

    print(
        f"Voice control ready. Say: '{args.wake_word} avance de 15 cm' or "
        f"'{args.wake_word} recule de 10 cm'."
    )
    print(f"Using input device: {input_info['name']} @ {stream_sr} Hz")
    print("Say or type Ctrl+C to stop.")

    try:
        try:
            stream = sd.RawInputStream(
                samplerate=stream_sr,
                blocksize=max(stream_sr // 10, 1024),
                device=args.mic_device,
                dtype="int16",
                channels=1,
                latency="low",
                callback=audio_callback,
            )
        except Exception as exc:
            if args.samplerate and stream_sr != detected_sr:
                # Retry with device default if user-selected rate is unsupported.
                stream_sr = detected_sr
                recognizer = KaldiRecognizer(model, stream_sr)
                print(f"Retrying with device default sample rate: {stream_sr} Hz")
                stream = sd.RawInputStream(
                    samplerate=stream_sr,
                    blocksize=max(stream_sr // 10, 1024),
                    device=args.mic_device,
                    dtype="int16",
                    channels=1,
                    latency="low",
                    callback=audio_callback,
                )
            else:
                raise exc

        with stream:
            while True:
                data = audio_q.get()
                # Drain queued chunks to process the freshest audio first.
                while True:
                    try:
                        data = audio_q.get_nowait()
                    except queue.Empty:
                        break

                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "").strip()
                    if not text:
                        continue
                    print(f"Heard: {text}")

                    command_text = extract_after_wake_word(text, wake_words=wake_words)
                    if command_text is None:
                        continue

                    parsed = parse_distance_cmd(command_text, default_distance_cm=args.default_distance_cm)
                    if not parsed:
                        continue

                    action, distance_cm = parsed
                    if action == "avance":
                        advance_cm(px, distance_cm=distance_cm, speed=args.speed, cm_per_sec=args.cm_per_sec)
                    else:
                        # Use negative speed for backward motion with same timing calibration.
                        advance_cm(px, distance_cm=distance_cm, speed=-abs(args.speed), cm_per_sec=args.cm_per_sec)

                    print(f"Executed: {action} de {distance_cm:.1f} cm")
    finally:
        px.stop()


if __name__ == "__main__":
    main()
