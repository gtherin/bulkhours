import IPython
import ipywidgets


def get_description(i, j, update=False, lan="fr"):
    if lan == "fr":
        descriptions = [
            [
                dict(description="Envoyer au correcteur", button_style="primary"),
                dict(description="Correction envoyée", button_style="success"),
            ],
            [
                dict(description="Voir la correction", button_style="primary"),
                dict(description="Cacher la correction", button_style="danger"),
            ],
            [
                dict(description="Message au correcteur", button_style="info"),
                dict(description="Cacher le message du correcteur", button_style="warning"),
            ],
        ]
    else:
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
        ]
    descriptions[i][j].update(
        dict(flex_flow="column", align_items="stretch", layout=ipywidgets.Layout(width="max-content"))
    )
    if update:
        return descriptions[i][j]["button_style"], descriptions[i][j]["description"]

    return ipywidgets.Button(**descriptions[i][j])


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
