import sys
import IPython
import ipywidgets

from .. import core
from . import answers
from . import tools


def get_alias_name(cuser):
    if "@" in cuser:
        auser = cuser.split("@")[0].split(".")
        return auser[0].capitalize() + "." + auser[1][0]
    return cuser


def show_answer(out, cuser, answer, style=None):
    color = "green" if cuser == "solution" else "red"
    cuser = get_alias_name(cuser)
    show_raw_code = style == "dark"  # not ("google.colab" in sys.modules and style != "dark")

    with out:
        # Show code
        core.tools.html(f"Code ({cuser})", size="4", color=color, use_ipywidgets=True, display=True)
        if "answer" in answer:
            core.tools.code(answer["answer"], display=True, style=style)  # , raw=show_raw_code

        # Execute code
        core.tools.html(f"Execution ({cuser})💻", size="4", color=color, use_ipywidgets=True, display=True)
        if "answer" in answer:
            core.tools.eval_code(answer["answer"])


def create_evaluation_buttonanswer(cell_id, cuser, answer, solution):
    config = core.tools.get_config()

    language = config["global"]["language"]
    label = core.tools.html(get_alias_name(cuser), size="6", color="#4F4F4F", use_ipywidgets=True)
    abuttons = core.buttons.get_buttons_list(label="", language=language, user="solution")
    output = ipywidgets.Output()

    grade = core.Grade.get(answer)

    widget = ipywidgets.FloatSlider(
        min=0,
        max=10,
        value=grade,
        step=0.5,
        continuous_update=True,
        orientation="horizontal",
        readout=True,
        readout_format=".1f",
    )
    widget.style.handle_color = "lightblue"

    def sevaluate(data, output):
        with output:
            output.clear_output()
            answers.update_grade(cell_id, cuser, widget.value, name="grade_man")

    if "main_execution" in answer and "main_execution" in answer and core.gpt.evaluation_instructions is not None:
        abuttons["a"].b.description = "🤖Correct student"

    def autocorrect(data, output):

        reset = """# Create a 2 axes figure
fig, axes = plt.subplots(1, 2, figsize=(15, 4))
sns.set_palette("hls")

# 1. Implement a normal(/gaussian) function
def gaussian(x: np.ndarray, mu: float, sig: float) -> np.ndarray:
    return x  # ...

ax = axes[0]
ax.set_title("Normal distributions")
x = np.linspace(-10, 10, 200)
# 2. Plot the previous function with the previous x
# ...
# 3. Plot the scipy norm pdf function (with mu=2 and sigma=3).
# ...
# 4. Generate 1000 random events according with the previous distribution
# Plot the histogram
# ...
ax.legend()

ax = axes[1]
for k in np.geomspace(2, 128, num=7, dtype=int):
    # 5. Plot the student pdf function for a 95%CI (with k as parameter).
    # ...

    # 6. Calculate the Shapiro and Kolmogov tests pvalues for 5000 random events generated with the previous distribution
    shapiro_pvalue = 0  # ...
    kolmogorov_pvalue = 0  # ...

    # 7. Get the skew estimator and calculate it with the Pearson estimator (with a norm.cdf).
    skew, sperson = 0, 0  # ...

    print(f'k={k}, skew={skew:.2f}, skew(Pearson)={sperson:.2f}, pval(Shapiro)={shapiro_pvalue:.2f}, pval(Kolmogorov)={kolmogorov_pvalue:.2f}')

ax.set_xlim([-2, 2])
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$P_{Student}(x)$")
ax.set_title(r"$Student$ Probability density")
ax.legend()

# 8. Comment the points 6 and 7
print("... MY COMMENT")

"""
        if "main_execution" in answer and "main_execution" in answer and core.gpt.evaluation_instructions is not None:
            prompt = f"""{core.gpt.evaluation_instructions}
Initial solution:\n<start>{reset}</start>
Final solution:\n<end>{solution['main_execution']}<end>
Student solution:\n<answer>{answer['main_execution']}</answer>\n"""                
            response = core.ask_chat_gpt(question=prompt, model="gpt-3.5-turbo", temperature=0., raw=True, openai_token=core.gpt.evaluation_openai_token)

            try:
                grade = response.split("Grade: ")[1]
                if "/" in grade:
                    grade = grade.split("/")[0]
                grade = float(grade)
                answers.update_grade(cell_id, cuser, grade, grade_name="grade_bot", comment=response)
            except:
                print(f"Grade was not properly extracted from response:\n{response}")
            return

        print("🚧Need to implement autocorrect here")

    def sevaluate2(b):
        return core.buttons.update_button(b, abuttons["e"], output, None, sevaluate)

    def sautocorrect(b):
        return core.buttons.update_button(b, abuttons["a"], output, None, autocorrect)

    abuttons["e"].b.on_click(sevaluate2)
    abuttons["a"].b.on_click(sautocorrect)

    IPython.display.display(ipywidgets.HBox([label, widget, abuttons["e"].b, abuttons["a"].b]), output)


def evaluate(cell_id, user="NEXT", show_correction=False, style=None, **kwargs):
    cell_answers = answers.get_answers(cell_id, **kwargs)
    config = core.tools.get_config(is_new_format=True)

    users = tools.get_users_list(no_admin=False)
    ausers = users.set_index("auser")["mail"].to_dict()

    nuser, did_find_answer = user, False
    for cuser, answer in cell_answers.items():

        grade = core.Grade.get(answer)

        if (user == "NEXT" and grade == core.Grade.DEFAULT_GRADE) or user == cuser or (user in ausers and ausers[user] == cuser):
            nuser, did_find_answer = cuser, True
            if show_correction and "solution" in cell_answers:
                out1 = ipywidgets.Output(layout={"width": "50%"})
                out2 = ipywidgets.Output(layout={"width": "50%"})
                tabs = ipywidgets.HBox([out1, out2])

                show_answer(out1, cuser, answer, style=style)
                # bulkhours.c.set_style(out2, "sol_background")
                show_answer(out2, "solution", cell_answers["solution"], style=style)

            else:
                tabs = ipywidgets.Output(layout={"width": "100%"})
                show_answer(tabs, cuser, answer, style=style)

            out = ipywidgets.Output(layout={"border": "1px solid #CFCFCF", "width": "100%"})
            # bulkhours.c.set_style(out, "cell_background")
            with out:
                solution = cell_answers["solution"] if "solution" in cell_answers else None
                create_evaluation_buttonanswer(cell_id, cuser, answer, solution)

            IPython.display.display(ipywidgets.VBox([tabs, out]))
            return

    if not did_find_answer:
        core.tools.html(
            f"Pas de réponse disponible pour {nuser}"
            if config.language == "fr"
            else f"{nuser} answer is not available",
            use_ipywidgets=True,
        )
