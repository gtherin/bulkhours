import IPython
import ipywidgets
import time
import multiprocessing
import numpy as np

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
    "submit_o_sen": "Publish answer     ",
    "submit_o_sfr": "Publier la réponse ",
    "submit_f_sen": "Answer was published",
    "submit_f_sfr": "Réponse publiée",
    "correct_o_en": "Show correction",
    "correct_o_fr": "Voir la correction",
    "correct_f_en": "Hide correction",
    "correct_f_fr": "Cacher la correction",
    "message_o_en": "Message from corrector",
    "message_o_fr": "Message au correcteur",
    "message_f_en": "Hide message from corrector",
    "message_f_fr": "Cacher le message du correcteur",
    "evaluate_o_en": "Save the grade",
    "evaluate_o_fr": "Sauvegarder la note",
    "evaluate_f_en": "Grade saved",
    "evaluate_f_fr": "Note sauvegardée",
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
        self, label, sleep_on=None, width=None, bso="primary", bsf="success", in_french=False, user="student"
    ) -> None:
        self.label, self.user, self.sleep_on, self.width = label, user, sleep_on, width
        self.show_answer, self.is_on, self.b = True, True, None
        all_labels[f"{self.label}_o_style"] = bso
        all_labels[f"{self.label}_f_style"] = bsf
        self.lan = "fr" if in_french else "en"

    def d(self, blabel):
        return (
            all_labels[f"{blabel}_s{self.lan}"]
            if f"{blabel}_s{self.lan}" in all_labels
            else all_labels[f"{blabel}_{self.lan}"]
        )

    def update_style(self, button, style=None):
        blabel = f"{self.label}_{style}" if style in ["o", "f"] else style
        button.description, button.button_style = self.d(blabel), all_labels[f"{blabel}_style"]
        # button.disabled = style in ["warning", "danger"]
        # button.icon = "fa-spinner fa-pulse fa-1x fa-fw" if style in ["warning"] else ""
        # button.icon = button.icon.replace("/\b(\w)/g", "fa-$1")
        # icon.replace(/\b(\w)/g, 'fa-$1')

    def g(self):
        self.b = ipywidgets.Button(
            description=self.d(f"{self.label}_o"),
            button_style=all_labels[f"{self.label}_o_style"],
            flex_flow="column",
            align_items="stretch",
            tooltip=self.d(f"{self.label}_o"),
            layout=ipywidgets.Layout(width=self.width if self.width is not None else "max-content"),
        )
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


def get_all_buttons(**kwargs):
    return [
        SwitchButton("submit", sleep_on=2, width="150px", **kwargs),
        SwitchButton("correct", width="150px", bsf="danger", **kwargs),
        SwitchButton("message", bso="info", bsf="danger", width="150px", **kwargs),
        SwitchButton("evaluate", bso="info", sleep_on=3, width="150px", **kwargs),
        SwitchButton("test", bso="info", sleep_on=1, width="130px", **kwargs),
        SwitchButton("gpt", bso="info", bsf="danger", width="150px", **kwargs),
        SwitchButton("user", bso="info", bsf="danger", width="150px", **kwargs),
    ]


def get_buttons_list(label=None, **kwargs):
    abuttons = get_all_buttons(**kwargs)

    for s in abuttons:
        s.g()

    widgets = {"l": label}
    widgets.update({b.label[0]: b for b in abuttons})
    return widgets


def update_button(b, idx, funct, output, abuttons, args, kwargs):
    from . import colors

    with output:
        output.clear_output()
        colors.set_style(output, "sol_background")
        abuttons[idx].is_on = not abuttons[idx].is_on

        abuttons[idx].update_style(b, style="transition")
        if not abuttons[idx].is_on:
            if 1:
                # try:
                p1 = multiprocessing.Process(target=funct, args=args, kwargs=kwargs)
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

                abuttons[idx].is_on = abuttons[idx].wait(abuttons[idx].is_on, b)

            if 0:
                # except Exception as e:
                abuttons[idx].update_style(b, style="error")
                IPython.display.display(e)
                time.sleep(2)
                abuttons[idx].is_on = True

        abuttons[idx].update_style(b, style="o" if abuttons[idx].is_on else "f")
