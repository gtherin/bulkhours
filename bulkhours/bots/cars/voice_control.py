#!/usr/bin/env python3
import argparse
import io
import json
import os
import queue
import re
import subprocess
import time
import unicodedata
import wave
from pathlib import Path

import sounddevice as sd
from vosk import KaldiRecognizer, Model
from .robot_controller import RobotController
from movement import advance_cm, route_20_right10_10, turn_right_cm


COMMAND_CATALOG = [
    {"name": "avance_cm_tool", "description": "Advance straight by N cm", "params": ["distance_cm"]},
    {
        "name": "turn_right_cm_tool",
        "description": "Turn right by arc distance with steering",
        "params": ["distance_cm", "steer_angle"],
    },
    {"name": "reverse_cm_tool", "description": "Reverse straight by N cm", "params": ["distance_cm"]},
    {"name": "route_tool", "description": "Run fixed route 20 + right10 + 10", "params": []},
    {"name": "stop_tool", "description": "Stop immediately", "params": []},
    {"name": "play_song_tool", "description": "Play song number N from Music folder", "params": ["song_index"]},
]


def normalize_asr_text(text):
    normalized = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    normalized = normalized.lower().replace(",", ".")
    # Common ASR confusions observed on-device.
    replacements = {
        "picard": "picar",
        "pica": "picar",
        "pi car": "picar",
        "picarx": "picar",
        "car": "picar",
        "absence": "avance",
        "avence": "avance",
        "avancee": "avance",
        "rue de": "recule de",
        "pecule": "recule",
        "reculer": "recule",
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


def parse_song_cmd(text):
    """Extract song command with fixed folder ~/Music.

    Examples:
    - joue chanson 1
    - joue chanson 2 repertoire music
    """
    normalized = normalize_asr_text(text)
    word_to_num = {
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
    }
    for word, num in word_to_num.items():
        normalized = re.sub(rf"\b{word}\b", num, normalized)

    m = re.search(r"\b(joue|play)\s+chanson\s+(\d+)\b", normalized)
    if not m:
        return None
    return int(m.group(2))


def play_song_from_music(song_index):
    music_dir = Path.home() / "Music"
    files = sorted([p for p in music_dir.iterdir() if p.suffix.lower() in {".mp3", ".wav"}])
    if not files:
        raise FileNotFoundError(f"No .mp3/.wav files in {music_dir}")
    if song_index < 1 or song_index > len(files):
        raise IndexError(f"Song index {song_index} out of range 1..{len(files)}")

    target = files[song_index - 1]
    if target.suffix.lower() == ".wav":
        subprocess.run(["aplay", str(target)], check=True)
    else:
        subprocess.run(["mpg123", "-q", str(target)], check=True)
    return target


def extract_after_wake_word(text, wake_words):
    normalized = normalize_asr_text(text).replace(",", " ")
    pattern = r"\b(" + "|".join(re.escape(w.lower()) for w in wake_words) + r")\b"
    m = re.search(pattern, normalized)
    if m:
        return m.group(1), normalized[m.end():].strip()

    # Fallback for ASR phonetic drift at beginning: e.g. "car recule de huit".
    tokens = normalized.split()
    if tokens and tokens[0] in {"car", "picard", "picar", "pica", "pikar"}:
        tail = " ".join(tokens[1:]).strip()
        if re.search(r"\b(avance|recule|stop|route|tourne|droite)\b", tail):
            return tokens[0], tail
    return None, None


def interpret_with_openai(graph, text, fallback_distance_cm):
    result = graph.invoke({"user_text": text, "result_json": {}})
    parsed = result.get("result_json", {})
    action = str(parsed.get("action", "none")).strip().lower()
    distance = parsed.get("distance_cm", None)
    if action in ("advance", "reverse"):
        try:
            distance = float(distance)
        except Exception:
            distance = float(fallback_distance_cm)
    return action, distance, parsed


def transcribe_pcm16_with_openai(pcm_bytes, sample_rate, model_name="gpt-4o-mini-transcribe", language="fr"):
    from openai import OpenAI

    if not pcm_bytes:
        return ""

    wav_buf = io.BytesIO()
    with wave.open(wav_buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # int16
        wf.setframerate(sample_rate)
        wf.writeframes(pcm_bytes)
    wav_buf.seek(0)
    wav_buf.name = "command.wav"

    client = OpenAI()
    transcript = client.audio.transcriptions.create(
        model=model_name,
        file=wav_buf,
        language=language,
    )
    return (getattr(transcript, "text", "") or "").strip()


def build_openai_tool_llm(model_name, temperature):
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain_core.tools import tool
    from langchain_openai import ChatOpenAI

    @tool
    def avance_cm_tool(distance_cm: float):
        """Advance forward by distance in centimeters."""
        return f"advance {distance_cm}"

    @tool
    def turn_right_cm_tool(distance_cm: float = 10.0, steer_angle: int = 25):
        """Turn right by driving an arc of distance_cm centimeters at steer_angle."""
        return f"turn_right {distance_cm} {steer_angle}"

    @tool
    def reverse_cm_tool(distance_cm: float):
        """Reverse backward by distance in centimeters."""
        return f"reverse {distance_cm}"

    @tool
    def stop_tool():
        """Stop the car immediately."""
        return "stop"

    @tool
    def route_tool():
        """Run the route: forward 20 cm, turn right over 10 cm arc, then forward 10 cm."""
        return "route"

    @tool
    def play_song_tool(song_index: int = 1):
        """Play song by index from ~/Music."""
        return f"play_song {song_index}"

    tools = [avance_cm_tool, turn_right_cm_tool, reverse_cm_tool, stop_tool, route_tool, play_song_tool]
    llm = ChatOpenAI(model=model_name, temperature=temperature).bind_tools(tools, tool_choice="required")

    system_prompt = (
        "You are a command-routing agent for PiCar-X. "
        "You must output exactly one tool call from the catalog below. "
        "Pick the closest valid candidate action and infer safe parameters. "
        "If distance is missing, use 10. "
        "If ambiguous or unsafe, use stop_tool. "
        f"Catalog: {json.dumps(COMMAND_CATALOG, ensure_ascii=False)}"
    )

    def invoke(command_text):
        msg = [SystemMessage(content=system_prompt), HumanMessage(content=command_text)]
        return llm.invoke(msg)

    return invoke


def nearest_local_candidate(command_text, default_distance_cm):
    text = normalize_asr_text(command_text)
    song_index = parse_song_cmd(text)
    if song_index is not None:
        return "play_song", float(song_index), 25
    if any(k in text for k in ["stop", "arrete", "arrêt", "arret"]):
        return "stop", None, 25
    if any(k in text for k in ["route", "trajet", "parcours"]):
        return "route", None, 25
    if "droite" in text or "tourne" in text:
        m = re.search(r"(\d+(?:\.\d+)?)", text)
        dist = float(m.group(1)) if m else float(default_distance_cm)
        return "turn_right", dist, 25

    parsed = parse_distance_cmd(text, default_distance_cm=default_distance_cm)
    if not parsed:
        return "none", None, 25
    action_map = {"avance": "advance", "recule": "reverse"}
    return action_map.get(parsed[0], "none"), parsed[1], 25


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
        default="picard,pica,car,picarx",
        help="Comma-separated additional wake variants accepted by ASR",
    )
    parser.add_argument(
        "--openai-trigger-word",
        default="picard",
        help="If this wake word is heard, force OpenAI/LangGraph interpretation",
    )
    parser.add_argument(
        "--print-openai-params",
        action="store_true",
        help="Print OpenAI interpreted action/parameters for each processed command",
    )
    parser.add_argument("--default-distance-cm", type=float, default=10.0, help="Fallback distance when ASR misses the number")
    parser.add_argument(
        "--interpreter",
        choices=["local", "openai"],
        default="local",
        help="Command interpreter backend",
    )
    parser.add_argument(
        "--prompt-file",
        default=str(Path(__file__).with_name("langgraph_prompt.md")),
        help="System prompt file for OpenAI interpreter mode",
    )
    parser.add_argument("--openai-model", default="gpt-4o-mini", help="OpenAI model for interpreter mode")
    parser.add_argument("--openai-temperature", type=float, default=0.0, help="OpenAI temperature")
    parser.add_argument(
        "--openai-mode",
        choices=["json", "tools"],
        default="tools",
        help="OpenAI interpreter mode: JSON parser graph or direct LangChain tool-calls",
    )
    args = parser.parse_args()

    model_path = Path(args.model_dir)
    if not model_path.exists():
        raise FileNotFoundError(
            f"Vosk model not found at {model_path}. Download a French model and unpack there."
        )

    config_path = Path.home() / ".config" / "picar-x" / "picar-x.conf"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    px = RobotController(config_path=str(config_path))

    input_info = sd.query_devices(args.mic_device, "input")
    detected_sr = int(input_info["default_samplerate"])
    stream_sr = int(args.samplerate) if args.samplerate else detected_sr

    model = Model(str(model_path))
    recognizer = KaldiRecognizer(model, stream_sr)
    wake_words = [args.wake_word] + [w.strip() for w in args.wake_variants.split(",") if w.strip()]
    openai_graph = None
    openai_tool_invoke = None

    if args.interpreter == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            raise EnvironmentError("OPENAI_API_KEY is missing. Export your token or use --interpreter local.")
        if args.openai_mode == "json":
            from langgraph_interpreter import build_graph, load_system_prompt

            prompt_path = Path(args.prompt_file)
            if not prompt_path.exists():
                raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
            openai_graph = build_graph(args.openai_model, args.openai_temperature, load_system_prompt(prompt_path))
        else:
            openai_tool_invoke = build_openai_tool_llm(args.openai_model, args.openai_temperature)

    audio_q = queue.Queue(maxsize=8)
    last_overflow_warn = 0.0
    is_processing = False

    def audio_callback(indata, frames, time_info, status):
        nonlocal last_overflow_warn, is_processing
        if is_processing:
            return
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
    print(f"Interpreter: {args.interpreter}")
    print("Say or type Ctrl+C to stop.")

    try:
        try:
            stream = sd.RawInputStream(
                samplerate=stream_sr,
                blocksize=max(stream_sr // 4, 2048),
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
                    blocksize=max(stream_sr // 4, 2048),
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
                    turn_angle = 25

                    matched_wake, command_text = extract_after_wake_word(text, wake_words=wake_words)
                    if command_text is None:
                        continue

                    is_processing = True
                    try:
                        use_openai_for_this_cmd = (
                            args.interpreter == "openai"
                            or (matched_wake is not None and matched_wake == args.openai_trigger_word.lower())
                        )

                        if use_openai_for_this_cmd:
                            if not os.getenv("OPENAI_API_KEY"):
                                print("OPENAI_API_KEY missing: cannot use OpenAI for trigger word.")
                                action, distance_cm = "none", None
                            else:
                                # Lazy init for trigger-word mode when default interpreter is local.
                                if args.openai_mode == "json" and openai_graph is None:
                                    from langgraph_interpreter import build_graph, load_system_prompt

                                    prompt_path = Path(args.prompt_file)
                                    if not prompt_path.exists():
                                        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
                                    openai_graph = build_graph(
                                        args.openai_model,
                                        args.openai_temperature,
                                        load_system_prompt(prompt_path),
                                    )
                                elif args.openai_mode == "tools" and openai_tool_invoke is None:
                                    openai_tool_invoke = build_openai_tool_llm(
                                        args.openai_model,
                                        args.openai_temperature,
                                    )

                            if args.openai_mode == "tools":
                                try:
                                    ai_msg = openai_tool_invoke(command_text)
                                    tool_calls = getattr(ai_msg, "tool_calls", []) or []
                                    if not tool_calls:
                                        print(f"LLM(no-tool): {getattr(ai_msg, 'content', '')}")
                                        action, distance_cm, turn_angle = nearest_local_candidate(
                                            command_text,
                                            default_distance_cm=args.default_distance_cm,
                                        )
                                    else:
                                        tc = tool_calls[0]
                                        tool_name = tc.get("name")
                                        tool_args = tc.get("args", {}) or {}
                                        print(f"LLM(tool): {tool_name} {tool_args}")
                                        if tool_name == "avance_cm_tool":
                                            action = "advance"
                                            distance_cm = float(tool_args.get("distance_cm", args.default_distance_cm))
                                        elif tool_name == "reverse_cm_tool":
                                            action = "reverse"
                                            distance_cm = float(tool_args.get("distance_cm", args.default_distance_cm))
                                        elif tool_name == "turn_right_cm_tool":
                                            action = "turn_right"
                                            distance_cm = float(tool_args.get("distance_cm", 10.0))
                                            turn_angle = int(tool_args.get("steer_angle", 25))
                                        elif tool_name == "route_tool":
                                            action = "route"
                                            distance_cm = None
                                        elif tool_name == "play_song_tool":
                                            action = "play_song"
                                            distance_cm = float(tool_args.get("song_index", 1))
                                        else:
                                            action = "stop"
                                            distance_cm = None
                                except Exception as exc:
                                    print(f"OpenAI tool interpreter error: {exc}")
                                    action, distance_cm = "none", None
                            else:
                                try:
                                    action, distance_cm, parsed_json = interpret_with_openai(
                                        openai_graph,
                                        command_text,
                                        fallback_distance_cm=args.default_distance_cm,
                                    )
                                    print(f"LLM: {json.dumps(parsed_json, ensure_ascii=False)}")
                                except Exception as exc:
                                    print(f"OpenAI interpreter error: {exc}")
                                    action, distance_cm = "none", None

                            if args.print_openai_params:
                                debug_payload = {
                                    "heard": text,
                                    "wake": matched_wake,
                                    "command_text": command_text,
                                    "action": action,
                                    "distance_cm": distance_cm,
                                    "turn_angle": turn_angle,
                                }
                                print(f"OPENAI_INTERPRET: {json.dumps(debug_payload, ensure_ascii=False)}")
                        else:
                            song_index = parse_song_cmd(command_text)
                            if song_index is not None:
                                action, distance_cm = "play_song", float(song_index)
                            else:
                                parsed = parse_distance_cmd(command_text, default_distance_cm=args.default_distance_cm)
                                if not parsed:
                                    continue
                                action_map = {"avance": "advance", "recule": "reverse"}
                                action, distance_cm = action_map.get(parsed[0], "none"), parsed[1]

                        if action == "advance":
                            advance_cm(px, distance_cm=distance_cm, speed=args.speed, cm_per_sec=args.cm_per_sec)
                            print(f"Executed: avance de {distance_cm:.1f} cm")
                        elif action == "reverse":
                            advance_cm(px, distance_cm=distance_cm, speed=-abs(args.speed), cm_per_sec=args.cm_per_sec)
                            print(f"Executed: recule de {distance_cm:.1f} cm")
                        elif action == "route":
                            route_20_right10_10(px, speed=args.speed, cm_per_sec=args.cm_per_sec)
                            print("Executed: route 20 + right10 + 10")
                        elif action == "turn_right":
                            turn_right_cm(
                                px,
                                distance_cm=distance_cm,
                                speed=max(30, args.speed - 10),
                                cm_per_sec=args.cm_per_sec,
                                steer_angle=turn_angle,
                            )
                            print(f"Executed: turn right {distance_cm:.1f} cm")
                        elif action == "stop":
                            px.stop()
                            print("Executed: stop")
                        elif action == "play_song":
                            try:
                                track = play_song_from_music(int(distance_cm))
                                print(f"Executed: joue chanson {int(distance_cm)} -> {track.name}")
                            except Exception as exc:
                                print(f"Play song error: {exc}")
                    finally:
                        is_processing = False
    finally:
        px.stop()


if __name__ == "__main__":
    main()
