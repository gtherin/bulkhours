import sys
import argparse
import subprocess

from .data import *  # noqa
from .evaluation import *  # noqa
from .widgets.buttons import *  # noqa


def ask_chat_gpt(
    question="", api_key="YOURKEY", model="gpt-3.5-turbo", temperature=0.5, is_code=False, size="256x256"
):
    """
    temperature Conservateur(0) => Creatif(1)
    """
    import openai

    if api_key == "YOURKEY":
        IPython.display.display(
            IPython.display.Markdown(
                """## Interroger Chat-GPT
Apres la creation d'un compte ChatGpt:
* https://platform.openai.com/ai-text-classifier
Vous devez creer une clé d'API
"""
            )
        )
        return

    openai.api_key = api_key  # Have your own to run this cell !!!
    print("")

    if model in ["image"]:
        response = openai.Image.create(prompt=question, n=1, size=size)
        image_url = response["data"][0]["url"]
        IPython.display.display(IPython.display.Image(url=image_url))
        return

    completion = openai.ChatCompletion.create(
        model=model, messages=[{"role": "user", "content": (prompt := question)}], temperature=temperature
    )

    # Display prompt
    IPython.display.display(IPython.display.Markdown("### " + prompt))

    content = completion["choices"][0]["message"]["content"]

    # Display answer
    if is_code:
        c = content.split("```")
        if len(c) > 2:
            IPython.display.display(IPython.display.Code(c[1]))
        else:
            IPython.display.display(IPython.display.Code(content))
    else:
        IPython.display.display(IPython.display.Markdown(content))
