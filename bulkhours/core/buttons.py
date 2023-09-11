import IPython
import ipywidgets
import time
import multiprocessing
import numpy as np
from . import tools
from . import colors

all_labels = {
    "transition_en": "Operation in progress",
    "transition_fr": "Operation en cours   ",
    "transition_style": "warning",
    "error_en": "✖ Error",
    "error_fr": "✖ Erreur",
    "error_style": "danger",
    "submit_o_en": "Send answer to corrector",
    "submit_o_fr": "Envoyer au correcteur",
    "submit_f_en": "Answer sent to corrector",
    "submit_f_fr": "Correction envoyée",
    # "submit_d_en": """📤Envoi de la réponse (contenu de la cellule actuelle) sur le serveur de correction.\n💡La réponse pourra être utilisée pour evaluation""",
    "submit_d_fr": """📤Envoi de la réponse (contenu de la cellule actuelle) au correcteur.\n💡La réponse pourra être utilisée pour évaluation
""",
    "autocorrect_o_en": "Correct students     ",
    "autocorrect_o_fr": "Corriger les étudiants ",
    "autocorrect_f_en": "Solution was published",
    "autocorrect_f_fr": "Solution publiée",
    # "autocorrect_d_en": """Envoi de la réponse (contenu de la cellule actuelle) sur le serveur de correction.\nLa réponse pourra être utilisée pour evaluation""",
    "autocorrect_d_fr": """⚠️Seulement disponible à l'évaluateur⚠️.
📝Utilise le code de la fonction 'student_evaluation_function' pour évaluer tous les étudiants de la classe virtuelle.
""",
    "solution_o_en": "Publish solution     ",
    "solution_o_fr": "Publier la solution ",
    "solution_f_en": "Solution was published",
    "solution_f_fr": "Solution publiée",
    # "solution_d_en": """Envoi de la réponse (contenu de la cellule actuelle) sur le serveur de correction.\nLa réponse pourra être utilisée pour evaluation""",
    "solution_d_fr": """⚠️Seulement disponible à l'évaluateur⚠️.
📤Envoi de la réponse (contenu de la cellule actuelle) comme solution officielle.
💡Si la fonction 'student_evaluation_function' est disponible, elle pourra être utilisée pour évaluer les étudiants.
""",
    "Student_o_en": "Save parameters",
    "Student_o_fr": "Sauvegarder les parametres",
    "Student_f_en": "Parameters have been updated",
    "Student_f_fr": "Parametres mise à jour",
    "correct_o_en": "Show correction",
    "correct_o_fr": "Voir la correction",
    "correct_f_en": "Hide correction",
    "correct_f_fr": "Cacher la correction",
    # "solution_d_en": """Envoi de la réponse (contenu de la cellule actuelle) sur le serveur de correction.\nLa réponse pourra être utilisée pour evaluation""",
    "correct_d_fr": """📥Récupération de la solution du correcteur. Si la solution est disponible, 
- 🎺Elle est affichée, 
- 🎯Elle peut-etre comparée avec le code de la cellule actuelle
""",
    "message_o_en": "Message from corrector",
    "message_o_fr": "Message au correcteur",
    "message_f_en": "Hide message from corrector",
    "message_f_fr": "Cacher le message du correcteur",
    "evaluate_o_en": "Save the grade",
    "evaluate_o_fr": "Sauvegarder la note",
    "evaluate_f_en": "Grade saved",
    "evaluate_f_fr": "Note sauvegardée",
    "email_o_en": "Save the grade",
    "email_o_fr": "Sauvegarder la note",
    "email_f_en": "Grade saved",
    "email_f_fr": "Note sauvegardée",
    "test_o_en": "Save And test",
    "test_o_fr": "Sauver et tester",
    "test_f_en": "Saved and tested",
    "test_f_fr": "Sauvé et testé",
    "gpt_o_en": "Ask Chat-gpt",
    "gpt_o_fr": "Demande à Chat-gpt",
    "gpt_f_en": "Hide result",
    "gpt_f_fr": "Cacher le résultat",
    "user_o_en": "Correct student's answer",
    "user_o_fr": "Analyser la réponse de l'étudiant",
    "user_f_en": "Finish the analysis",
    "user_f_fr": "Finir l'analyse",
}


class SwitchButton:
    def __init__(
        self,
        label,
        sleep_on=None,
        width=None,
        is_button=True,
        bso="primary",
        bsf="success",
        fr=None,
        en=None,
        language=False,
        user="student",
        elabel=None,
        l=None,
    ) -> None:
        self.label, self.user, self.sleep_on, self.width, self.is_button = label, user, sleep_on, width, is_button
        self.show_answer, self.is_on, self.b = True, True, None
        self.lan = language
        all_labels[f"{self.label}_o_style"] = bso
        all_labels[f"{self.label}_f_style"] = bsf
        if fr is not None:
            all_labels[f"{self.label}_fr"] = fr
        if en is not None:
            all_labels[f"{self.label}_en"] = en

        self.l = l if l is not None else self.label[0]
        self.elabel = elabel
        self.g()

    def d(self, blabel):
        for label in [f"{blabel}_s{self.lan}", f"{blabel}_{self.lan}", f"{self.label}_{self.lan}", f"{self.label}_fr"]:
            if label in all_labels:
                return all_labels[label]

        return blabel

    def update_style(self, button, style=None):
        blabel = f"{self.label}_{style}" if style in ["o", "f"] else style
        button.description, button.button_style = self.d(blabel), all_labels[f"{blabel}_style"]
        # button.disabled = style in ["warning", "danger"]
        # button.icon = "fa-spinner fa-pulse fa-1x fa-fw" if style in ["warning"] else ""
        # button.icon = button.icon.replace("/\b(\w)/g", "fa-$1")
        # icon.replace(/\b(\w)/g, 'fa-$1')

    def get_tootip(self):
        for label in [f"{self.label}_d_{self.lan}", f"{self.label}_d_fr", f"{self.label}_d_en"]:
            if label in all_labels:
                return all_labels[label]
        return self.d(f"{self.label}_o")

    def g(self):
        if self.is_button:
            self.b = ipywidgets.Button(
                description=self.d(f"{self.label}_o"),
                button_style=all_labels[f"{self.label}_o_style"],
                flex_flow="column",
                align_items="stretch",
                tooltip=self.get_tootip(),
                layout=ipywidgets.Layout(width=self.width if self.width is not None else "max-content"),
            )
        else:
            self.b = tools.html(self.elabel, size="4", color="black")

        return self.b

    def wait(self, show_answer, button, style="f", sleep=None):
        sleep = self.sleep_on if sleep is None else sleep
        if not sleep:
            return show_answer

        self.update_style(button, style=style)
        description = button.description
        for u in range(int(sleep)):
            d = sleep - u
            button.description = f"{d} " + description
            time.sleep(1)
        return True


def get_all_buttons(label, **kwargs):
    return [
        SwitchButton("autocorrect", l="a", sleep_on=2, width="150px", bso="danger", **kwargs),
        SwitchButton("correct", l="c", width="150px", bsf="danger", **kwargs),
        SwitchButton("email", l="E", bso="info", bsf="danger", width="150px", **kwargs),
        SwitchButton("evaluate", l="e", bso="info", sleep_on=3, width="150px", **kwargs),
        SwitchButton("gpt", l="g", bso="info", bsf="danger", width="150px", **kwargs),
        SwitchButton("label", l="l", elabel=label, is_button=False, **kwargs),
        SwitchButton("message", l="m", bso="info", bsf="danger", width="150px", **kwargs),
        SwitchButton("solution", l="o", sleep_on=2, width="150px", bso="warning", **kwargs),
        SwitchButton("Student", l="S", sleep_on=2, width="200px", **kwargs),
        SwitchButton("submit", l="s", sleep_on=2, width="200px", **kwargs),
        SwitchButton("test", l="t", is_button=True, **kwargs),
        SwitchButton("user", bso="info", bsf="danger", width="150px", **kwargs),
    ]


def get_buttons_list(label=None, **kwargs):
    return {b.l: b for b in get_all_buttons(label, **kwargs)}


def update_button(b, button, output, widget, funct, kwargs=None):
    from . import colors

    if kwargs is None:
        kwargs = {}

    if type(funct) == str:
        funct = getattr(widget.__class__, funct)

    with output:
        output.clear_output()
        colors.set_style(output, "sol_background")
        button.is_on = not button.is_on

        button.update_style(b, style="transition")
        if not button.is_on:
            p1 = multiprocessing.Process(target=funct, args=[widget, output], kwargs=kwargs)
            p1.start()
            fun, sleep = ["🙈", "🙉", "🙊"], 0.3
            fun, sleep = ["🌑", "🌒", "🌓‍", "🌖", "🌗", "🌘"], 0.3
            fun, sleep = ["🤛‍", "✋", "✌"], 0.3
            fun, sleep = ["🏊", "🚴", "🏃"], 0.3
            fun, sleep = ["🙂‍", "😐", "😪", "😴", "😅"], 0.3
            fun, sleep = ["🟥", "🟧", "🟨‍", "🟩", "🟦", "🟪"], 0.3
            ii, description = 0, b.description
            while p1.is_alive():
                b.description = fun[ii % len(fun)] + description

                time.sleep(sleep * np.abs((np.random.normal() + 1)))
                ii += 1

            button.is_on = button.wait(button.is_on, b)

        button.update_style(b, style="o" if button.is_on else "f")


def get_export_button(filename, data=None, label="Download file", tooltip=None, style="bk_secondary", width="150px"):
    import base64

    if data is None:
        with open(filename) as f:
            data = f.readline()

    if tooltip is None:
        tooltip = f"💾Download the file '{filename}'"

    b64 = base64.b64encode(data.encode())
    payload = b64.decode()
    button_styles = colors.get_html_buttons_styles_code()

    html_button = f"""<html><head><meta name="viewport" content="width=device-width, initial-scale=1">{button_styles}</head>
    <body><a download="{filename}" href="data:text/csv;base64,{payload}" download>
    <button title="{tooltip}" class="button {style}" style="width: {width};">{label}</button></a></body></html>"""
    IPython.display.display(IPython.display.HTML(html_button))
