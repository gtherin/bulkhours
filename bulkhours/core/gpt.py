import IPython
import numpy as np
import matplotlib

from . import tools

evaluation_instructions = None
evaluation_openai_token = "YOUR_KEY"


def ask_chat_gpt(
    question="", openai_token="YOUR_KEY", model="gpt-3.5-turbo", temperature=0.5, is_code=False, size="256x256", raw=False
):
    """
    temperature Conservative(0) => Creative(1)
    """

    import openai

    if openai_token == "YOUR_KEY":
        openai_token = tools.get_value("openai_token")

    if openai_token in ["YOUR_KEY", ""]:
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

    openai.api_key = openai_token

    if model in ["image"]:
        response = openai.Image.create(prompt=question, n=1, size=size)
        image_url = response["data"][0]["url"]
        IPython.display.display(IPython.display.Image(url=image_url))
        return

    # Ask chat-gpt
    completion = openai.ChatCompletion.create(
        model=model, messages=[{"role": "user", "content": (prompt := question)}], temperature=temperature
    )

    # Get content
    content = completion["choices"][0]["message"]["content"]

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


def ask_dall_e(question="", temperature=0.5, size="256x256"):
    ask_chat_gpt(question, model="image", size=size, temperature=temperature, is_code=False)


def get_grade(student_data, teacher_data):
    if "main_execution" in student_data.minfo and "main_execution" in teacher_data.minfo and evaluation_instructions is not None:
        prompt = f"""{evaluation_instructions}
- question:\n<start>\n{teacher_data.get_reset()}\n</start>
- actual solution:\n<end>\n{teacher_data.get_solution()}\n</end>
- student's solution:\n<answer>\n{student_data.get_solution()}\n</answer>\n"""
        
        #print(prompt)
        response = ask_chat_gpt(question=prompt, model="gpt-3.5-turbo", temperature=0., raw=True, openai_token=evaluation_openai_token)

        # Get student user
        user = student_data.minfo["user"]
        try:
            grade = float((response.split("<grade>"))[1].split("</grade>")[0])
            grade_color = matplotlib.colors.rgb2hex(matplotlib.cm.get_cmap("RdBu")(grade/10.))
            comment = response.split("</grade>")[1]
            IPython.display.display(IPython.display.Markdown(f"#### <b>{user}: <font color='{grade_color}'>grade={grade}</font></b>\n{response}"))        
            return grade, comment
        except:
            IPython.display.display(IPython.display.Markdown(f"#### <b>{user}: <font color='red'>grade is unknown</font></b>\n{response}"))

            return np.nan, response
