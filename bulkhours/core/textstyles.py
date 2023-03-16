import IPython
import ipywidgets


class SwitchButton:
    def __init__(self, label, on_description, on_description_fr, off_description, off_description_fr) -> None:
        self.label = label
        self.on_description_en, self.off_description_en = on_description, off_description
        self.on_description_fr, self.off_description_fr = on_description_fr, off_description_fr
        self.show_answer = True
        self.in_french = False

    def update_style(self, button, on=True):
        button.button_style = self.on["button_style"] if on else self.off["button_style"]
        button.description = self.on["description"] if on else self.off["description"]

    @property
    def on(self):
        return self.on_description_fr if self.in_french else self.on_description_en

    @property
    def off(self):
        return self.off_description_fr if self.in_french else self.off_description_en

    def g(self, in_french):
        self.in_french = in_french
        args = self.on
        args.update(dict(flex_flow="column", align_items="stretch", layout=ipywidgets.Layout(width="max-content")))

        return ipywidgets.Button(**args)


sbuttons = [
    SwitchButton(
        "submit",
        dict(description="Send answer to corrector", button_style="primary"),
        dict(description="Envoyer au correcteur", button_style="primary"),
        dict(description="Answer sent to corrector", button_style="success"),
        dict(description="Correction envoyée", button_style="success"),
    ),
    SwitchButton(
        "correct",
        dict(description="Show correction", button_style="primary"),
        dict(description="Voir la correction", button_style="primary"),
        dict(description="Hide correction", button_style="danger"),
        dict(description="Cacher la correction", button_style="danger"),
    ),
    SwitchButton(
        "message",
        dict(description="Message from corrector", button_style="info"),
        dict(description="Message au correcteur", button_style="info"),
        dict(description="Hide message from corrector", button_style="warning"),
        dict(description="Cacher le message du correcteur", button_style="warning"),
    ),
    SwitchButton(
        "evaluate",
        dict(description="Sauvegarder la note", button_style="info"),
        dict(description="Sauvegarder la note", button_style="info"),
        dict(description="Note sauvegardée", button_style="warning"),
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
