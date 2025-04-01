import IPython
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os
import re
import requests

from . import tools
from .grade import Grade

evaluation_instructions = ""
evaluation_openai_token = "YOUR_KEY"
evaluation_replicate_token = "YOUR_KEY"
tokens = {}
evaluation_model = "gpt-4o-mini"
evaluation_client = None

llms = {"mistral-7b": "mistralai/mistral-7b-v0.1", "llama-3-8b": "meta/meta-llama-3-8b-instruct"}


def get_token(tokenkey, token="YOUR_KEY"):
    if token != "YOUR_KEY":
        return token

    if tokenkey in os.environ:
        return os.environ[tokenkey]

    if tokenkey in tokens:
        return tokens[tokenkey]

    try:
        from google.colab import userdata
        return userdata.get(tokenkey)
    except:
        pass

    return tools.get_value(tokenkey)


def ask_deepseek_gpt(prompt="",
    token="YOUR_KEY",
    model="deepseek-chat",
    temperature=0.5,
    top_p=1,
    size="256x256"
    ):
    response = requests.post("https://api.deepseek.com/v1/chat/completions", 
                             headers={"Authorization": f"Bearer {get_token('DEEPSEEK_API_KEY', token=token)}"}, 
                             json={"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}]})

    return response.json()["choices"][0]["message"]["content"]


def ask_opensource_gpt(
    prompt="",
    token="YOUR_KEY",
    model="mistral-7b",
    temperature=0.5,
    top_p=1,
    size="256x256",
):
    os.environ["REPLICATE_API_TOKEN"] = get_token('REPLICATE_API_TOKEN', token=token)
    replicate = tools.install_if_needed("replicate")

    full_response = ""
    for event in replicate.stream(llms[model], input={
        "prompt": prompt,
        "max_new_tokens": 512, #"temperature": temperature, "top_p": top_p, "repetition_penalty": 1
    }):
        full_response += str(event)

    #input={"prompt": prompt, "temperature": temperature, "top_p": top_p, "max_length": 512, "repetition_penalty": 1},

    return full_response


# https://stackoverflow.com/questions/75396481/openai-gpt-3-api-error-this-models-maximum-context-length-is-4097-tokens
def ask_chat_gpt(
    prompt="",
    token="YOUR_KEY",
    model="gpt-4o-mini",
    temperature=0.5,
    top_p=1,
    size="256x256",
):
    openai = tools.install_if_needed("openai")

    if token == "YOUR_KEY":
        token = get_token('OPENAI_API_KEY', token=token)
    if token is None or token == "YOUR_KEY":
        token = get_token('openai_token', token=token)

    if token in ["YOUR_KEY", "", None]:
        IPython.display.display(
            IPython.display.Markdown(
                """## Interroger Chat-GPT
Après la creation d'un compte ChatGpt:
* https://platform.openai.com/ai-text-classifier
Vous devez créer une clé d'API
"""
            )
        )
        return

    if model in ["image"]:
        response = openai.Image.create(prompt=prompt, n=1, size=size)
        image_url = response["data"][0]["url"]
        IPython.display.display(IPython.display.Image(url=image_url))
        return

    # Ask chat-gpt
    completion = evaluation_client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": evaluation_instructions}, {"role": "user", "content": prompt}],
        temperature=temperature,
        top_p=top_p,
    )
    # Get content
    return completion.choices[0].message.content


def ask_gpt(
    prompt="",
    model="gpt-4o-mini",
    token="YOUR_KEY",
    is_code=False,
    raw=False,
    temperature=0.5,
    top_p=1,
    size="256x256",
):
    """
    temperature: number or null
    Optional Defaults to 1
    What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.
    We generally recommend altering this or top_p but not both.
        temperature Conservative(0) => Creative(1)

    - top_p number or null Optional Defaults to 1
    An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

    We generally recommend altering this or temperature but not both.

    - user:
    The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. If you offer a preview of your product to non-logged in users, you can send a session ID instead.

    You can include end-user IDs in your API requests via the user parameter as follows:

    """

    if model in [
        "gpt-4-1106-preview",
        "gpt-4o-mini",
        "gpt-4-32k-0613",
        "gpt-3.5-turbo-0125",
        "image",
    ]:
        rofunc = ask_chat_gpt
    elif model in ['deepseek-r1']:
        rofunc = ask_deepseek_gpt
    elif model in llms:
        rofunc = ask_opensource_gpt
    else:
        raise Exception(f"Model {model} is unknown.")

    content = rofunc(
        prompt=prompt,
        token=token,
        model=model,
        temperature=temperature,
        top_p=top_p,
        size=size,
    )

    # return raw data
    if raw:
        return content

    # Display prompt
    IPython.display.display(IPython.display.Markdown("### " + prompt))

    # Display answer
    if is_code:
        c = content.split("```")
        if len(c) > 2:
            IPython.display.display(IPython.display.Code(c[1]))
        else:
            IPython.display.display(IPython.display.Code(content))
    else:
        is_markdown = False
        for c in content.split("```"):
            is_markdown = not is_markdown
            if is_markdown:
                IPython.display.display(IPython.display.Markdown(c))
            else:
                IPython.display.display(IPython.display.Code(c))


def get_grade(student_data, teacher_data, max_score, token="YOUR_KEY", evalcode=None, verbose=False, raw=False):

    if (
        "main_execution" in student_data.minfo
        and "main_execution" in teacher_data.minfo
        and evaluation_instructions is not None
    ):
    
        prompt = f"""{evaluation_instructions}
- question:\n<start>\n{teacher_data.get_reset()}\n</start>
- actual solution:\n<end>\n{teacher_data.get_solution()}\n</end>
- student's solution:\n<answer>\n{student_data.get_solution()}\n</answer>\n""".replace("MAX_SCORE", "10")#str(max_score))

        if verbose:
            print(prompt)

        evaluation_model = "gpt-4o-mini" if evalcode is None else evalcode
        response = ask_gpt(
            prompt=prompt, model=evaluation_model, temperature=0.01, raw=raw, token=token
        )
        if raw:
            return response

        # Get student user
        user = student_data.minfo["user"]
        try:
            grade = float((response.split("<grade>"))[1].split("</grade>")[0])
            grade_color = matplotlib.colors.rgb2hex(
                plt.get_cmap("RdBu")(grade / 10.0)
            )
            comment = (response.split("<summary>"))[1].split("</summary>")[0]
            #comment = response.split("</grade>")[1]
            IPython.display.display(
                IPython.display.Markdown(
                    f"#### <b>{user}: <font color='{grade_color}'>grade={grade}</font></b>\n{comment}"
                )
            )
            return Grade(score=grade, comment=comment)
        except:
            IPython.display.display(
                IPython.display.Markdown(
                    f"#### <b>{user}: <font color='red'>grade is unknown</font></b>\n{response}"
                )
            )

            return Grade(score=np.nan, comment=response)


def evaluate_with_gpt(messages, max_score, model, temperature=0, top_p=0.5):

    if model != "chat-gpt":
        data = bulkhours.core.gpt.ask_gpt(messages, model=model, raw=True, temperature=temperature, top_p=top_p)
    else:
        completion = evaluation_client.chat.completions.create(model="gpt-4o-mini", messages=messages, temperature=temperature, top_p=top_p)
        data = completion.choices[0].message.content

    student_blocks = data.split("<student>")
    students = {}

    min_score, max_score = 1000, 0
    for block in student_blocks:
        if block.strip():  # Skip empty blocks
            email_match = re.search(r"<email>(.*?)</email>", block)
            email = email_match.group(1) if email_match else ""

            summary_match = re.search(r"<summary>(.*?)</summary>", block, re.DOTALL)
            summary = summary_match.group(1).strip() if summary_match else ""

            grade_match = re.search(r"<grade>(\d+)</grade>", block)
            grade = int(grade_match.group(1)) if grade_match else np.nan
            if min_score > grade:
                min_score = grade
            if max_score < grade:
                max_score = grade

            students[email] = Grade(score=grade, src="bot", comment=summary)

    for email, grade in students.items():
        #grade_color = (grade - min_score) / (max_score - min_score)
        grade_color = grade.score / float(max_score)
        grade_color = grade_color + 0.25 * (1. if grade_color >= 0.5 else -1.)

        grade_color = matplotlib.colors.rgb2hex(plt.get_cmap("RdBu")(grade_color))
        IPython.display.display(
            IPython.display.Markdown(
                f"#### <b>{email}: <font color='{grade_color}'>grade={grade.score}</font></b>\n{grade.comment}"
            )
        )

    return students
