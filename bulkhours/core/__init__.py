import sys
import argparse
import subprocess

from .data import *  # noqa
from .evaluation import *  # noqa
from .widgets.buttons import *  # noqa


def runrealcmd(command, verbose=True):
    logfile = open("install.log", "w")
    stdout, stderr = subprocess.PIPE, subprocess.STDOUT
    stdout, stderr = logfile, logfile
    process = subprocess.Popen(command, stdout=stdout, shell=True, stderr=stderr, bufsize=1, close_fds=True)
    print(f"RUN {command}")
    process.wait()


def git_push(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Git helper")
    parser.add_argument("-m", "--message", help="Message", default="Some changes")
    args = parser.parse_args(argv)

    vfile = os.path.abspath(os.path.dirname(__file__)) + "/../__version__.py"
    version = (oversion := open(vfile).readline().split('"')[1]).split(".")
    nversion = f"{version[0]}.{version[1]}.{int(version[2])+1}"

    with open(vfile, "w") as the_file:
        the_file.write(f"""__version__ = "{nversion}"\n""")

    print(f"Update {oversion} => {nversion}")
    with open("git_push.sh", "w") as f:
        f.write(f"""git pull && git add . && git commit -m "{args.message}" && git push""")
    print(
        subprocess.run("bash git_push.sh".split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True).stdout
    )

    # cmd = f"""git add . && git commit -m "{args.message}" && git push"""
    # Popen(cmd, stdout=PIPE, shell=True, stderr=STDOUT)


def ask_chat_gpt(question="", api_key="YOURKEY", model="gpt-3.5-turbo"):
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

    completion = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": (prompt := question)}],
    )

    # Display answer
    IPython.display.display(IPython.display.Markdown("### " + prompt))
    IPython.display.display(IPython.display.Markdown(completion["choices"][0]["message"]["content"]))
