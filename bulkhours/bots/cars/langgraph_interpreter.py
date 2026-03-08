#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path
from typing import TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph


class InterpreterState(TypedDict):
    user_text: str
    result_json: dict


def load_system_prompt(prompt_path: Path) -> str:
    return prompt_path.read_text(encoding="utf-8")


def build_graph(model_name: str, temperature: float, system_prompt: str):
    llm = ChatOpenAI(model=model_name, temperature=temperature)

    def interpret(state: InterpreterState) -> InterpreterState:
        user_text = state["user_text"]
        msg = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
        ]
        raw = llm.invoke(msg).content
        try:
            parsed = json.loads(raw)
        except Exception:
            parsed = {
                "action": "none",
                "distance_cm": None,
                "raw_text": user_text,
                "reason": f"invalid JSON from model: {raw}",
            }
        return {"user_text": user_text, "result_json": parsed}

    graph = StateGraph(InterpreterState)
    graph.add_node("interpret", interpret)
    graph.add_edge(START, "interpret")
    graph.add_edge("interpret", END)
    return graph.compile()


def main():
    parser = argparse.ArgumentParser(description="LangGraph interpreter for PiCar-X French commands")
    parser.add_argument("text", nargs="?", default=None, help="Command text to interpret")
    parser.add_argument(
        "--prompt-file",
        default=str(Path(__file__).with_name("langgraph_prompt.md")),
        help="Path to system prompt instructions",
    )
    parser.add_argument("--model", default="gpt-4o-mini", help="OpenAI model name")
    parser.add_argument("--temperature", type=float, default=0.0)
    args = parser.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError("OPENAI_API_KEY is missing. Export your ChatGPT/OpenAI token first.")

    prompt_path = Path(args.prompt_file)
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

    text = args.text
    if text is None:
        text = input("Commande a interpreter: ").strip()

    graph = build_graph(args.model, args.temperature, load_system_prompt(prompt_path))
    result = graph.invoke({"user_text": text, "result_json": {}})
    print(json.dumps(result["result_json"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
