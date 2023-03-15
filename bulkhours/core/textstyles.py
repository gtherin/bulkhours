import IPython
import ipywidgets


descriptions = [
    [
        dict(description="Send answer to corrector", button_style="primary"),
        dict(description="Answer sent to corrector", button_style="success"),
    ],
    [
        dict(description="Show correction", button_style="primary"),
        dict(description="Hide correction", button_style="danger"),
    ],
    [
        dict(description="Message from corrector", button_style="info"),
        dict(description="Hide message from corrector", button_style="warning"),
    ],
    [
        dict(description="Sauvegarder la note", button_style="info"),
        dict(description="Note sauvegardée", button_style="warning"),
    ],
]


class SwitchButton:
    def __init__(self, label, on_description, off_description) -> None:
        self.label = label
        self.on_description = on_description
        self.off_description = off_description
        self.show_answer = True

        self.on_description.update(
            dict(flex_flow="column", align_items="stretch", layout=ipywidgets.Layout(width="max-content"))
        )
        self.off_description.update(
            dict(flex_flow="column", align_items="stretch", layout=ipywidgets.Layout(width="max-content"))
        )

    def update_style(self, button, on=True):
        button.button_style = self.on_description["button_style"] if on else self.off_description["button_style"]
        button.description = self.on_description["description"] if on else self.off_description["description"]

    @property
    def b(self):
        return ipywidgets.Button(**self.on_description)


sbuttons = [
    SwitchButton(
        "commit",
        dict(description="Envoyer au correcteur", button_style="primary"),
        dict(description="Correction envoyée", button_style="success"),
    ),
    SwitchButton(
        "correct",
        dict(description="Voir la correction", button_style="primary"),
        dict(description="Cacher la correction", button_style="danger"),
    ),
    SwitchButton(
        "message",
        dict(description="Message au correcteur", button_style="info"),
        dict(description="Cacher le message du correcteur", button_style="warning"),
    ),
    SwitchButton(
        "evaluate",
        dict(description="Sauvegarder la note", button_style="info"),
        dict(description="Note sauvegardée", button_style="warning"),
    ),
]


def get_buttons_label():
    return [s.label for s in sbuttons]


def get_button(label):
    return [s for s in sbuttons if s.label == label][0]


def md(mdbody=None, header=None, rawbody=None, codebody=None, hc="red", bc="black"):
    if header:
        IPython.display.display(
            IPython.display.Markdown(f"<b><font face='FiraCode Nerd Font' size=4 color='{hc}'>{header} 📚:<font></b>")
        )

    if mdbody and len(mdbody) > 1:
        IPython.display.display(
            IPython.display.Markdown(f"<font face='FiraCode Nerd Font' size=4 color='{bc}'>{mdbody}<font>")
        )
    if rawbody and len(rawbody) > 1:
        print(rawbody)
    if codebody and len(codebody) > 1:
        IPython.display.display(IPython.display.Code(codebody))
