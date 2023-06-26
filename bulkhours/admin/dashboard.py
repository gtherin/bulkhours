import IPython
from IPython.core.magic import Magics, magics_class, line_cell_magic, needs_local_scope
import json
import ipywidgets
from argparse import Namespace

import bulkhours_premium
from . import tools


class WidgetDashboard(bulkhours_premium.WidgetTextArea):
    widget_id = "dashboard"

    def __init__(self, config, abuttons):
        self.cinfo = Namespace(**config)
        self.cinfo.abuttons = abuttons
        self.widget = self.init_widget()

    def init_widget(self):
        IPython.display.display(
            IPython.display.HTML(
                """<style>
    .widget-radio-box {
        flex-direction: row !important;     
    }
    .widget-radio-box label{
        margin:5px !important;
        width: 200px !important;
    }
</style>"""
            )
        )
        self.output = ipywidgets.Output()

        config = bulkhours_premium.tools.get_config()

        virtual_room, subject, notebook_id = (config.get(v) for v in ["virtual_room", "subject", "notebook_id"])
        language, chatgpt, norm20, restricted, virtual_rooms = (
            config["global"].get(v) for v in ["language", "chatgpt", "norm20", "restricted", "virtual_rooms"]
        )

        self.ws = {
            k: ipywidgets.Text(
                value=config["notebooks"][notebook_id][k], layout=ipywidgets.Layout(flex="4 1 0%", width="auto")
            )
            for k in ["evaluation", "exercices", "page"]
        }

        self.ws["chatgpt"] = ipywidgets.Checkbox(
            value=chatgpt,
            description="🤖Autoriser ChatGpt" if language == "fr" else "🤖Allow ChatGpt",
            indent=False,
            layout=ipywidgets.Layout(width="auto", flex_flow="row", display="flex"),
        )
        self.ws["norm20"] = ipywidgets.Checkbox(
            value=norm20,
            description="📜Norme à 20" if language == "fr" else "📜Norm to 20",
            indent=False,
            layout=ipywidgets.Layout(width="auto", flex_flow="row", display="flex"),
        )
        self.ws["restricted"] = ipywidgets.Checkbox(
            value=restricted,
            description="🔒Acces restreint" if language == "fr" else "🔒Restrict access",
            indent=False,
            layout=ipywidgets.Layout(width="auto", flex_flow="row", display="flex"),
        )
        form_item_layout = ipywidgets.Layout(display="flex", flex_flow="row", justify_content="space-between")

        label = (
            f"Paramètres du cours (nb_id={notebook_id}, salle virtuelle={virtual_room})"
            if language == "fr"
            else f"Course parameters (nb_id={notebook_id}, virtual classroom={virtual_room})"
        )
        self.ws["title"] = bulkhours_premium.tools.html(label, size="5", color="green")

        xwidgets = []  # self.ws["title"]]

        self.ws["virtual_room"] = ipywidgets.RadioButtons(value=virtual_room, options=virtual_rooms.split(";"))

        self.ws["language"] = ipywidgets.RadioButtons(value=language, options=["fr", "en"])

        if 0:
            xwidgets.append(
                ipywidgets.Box(
                    [
                        bulkhours_premium.tools.html(
                            "Salle virtuelle active" if language == "fr" else "Active virtual classroom",
                            layout=ipywidgets.Layout(flex="1 1 0%", width="auto"),
                        ),
                        self.ws["virtual_room"],
                    ],
                    layout=form_item_layout,
                )
            )

        for vroom in virtual_rooms.split(";") + ["admins"]:
            self.ws[vroom] = ipywidgets.Text(
                value=config["global"][vroom], layout=ipywidgets.Layout(flex="4 1 0%", width="auto")
            )
            xwidgets.append(
                ipywidgets.Box(
                    [
                        bulkhours_premium.tools.html(vroom, layout=ipywidgets.Layout(flex="1 1 0%", width="auto")),
                        self.ws[vroom],
                    ],
                    layout=ipywidgets.Layout(display="flex", flex_flow="row", justify_content="space-between"),
                )
            )

        xwidgets.append(
            ipywidgets.Box(
                [
                    bulkhours_premium.tools.html("Exercices", layout=ipywidgets.Layout(flex="1 1 0%", width="auto")),
                    self.ws["exercices"],
                ],
                layout=form_item_layout,
            )
        )
        if 0:
            xwidgets.append(
                ipywidgets.Box(
                    [
                        bulkhours_premium.tools.html(
                            "Evaluation", layout=ipywidgets.Layout(flex="1 1 0%", width="auto")
                        ),
                        self.ws["evaluation"],
                    ],
                    layout=form_item_layout,
                )
            )
        xwidgets.append(
            ipywidgets.Box(
                [
                    bulkhours_premium.tools.html("Page", layout=ipywidgets.Layout(flex="1 1 0%", width="auto")),
                    self.ws["page"],
                ],
                layout=form_item_layout,
            )
        )

        with open(tools.get_config_file(subject=subject, cell_id="tokens")) as f:
            tokens = json.load(f)

            xwidgets.append(
                ipywidgets.Box(
                    [
                        bulkhours_premium.tools.html(
                            "Students tokens", layout=ipywidgets.Layout(flex="1 1 0%", width="auto")
                        ),
                        ipywidgets.Text(
                            value='tokens = "%s"' % tokens[virtual_room],
                            layout=ipywidgets.Layout(flex="4 1 0%", width="auto"),
                            disabled=True,
                        ),
                    ],
                    layout=form_item_layout,
                )
            )

        xwidgets.append(
            ipywidgets.Box(
                [
                    self.ws["chatgpt"],
                    self.ws["norm20"],
                    self.ws["restricted"],
                    self.ws["language"],
                    self.cinfo.abuttons["delete_solution"].b,
                    self.cinfo.abuttons["save_changes"].b,
                ],
                layout=form_item_layout,
            )
        )

        return ipywidgets.Box(
            xwidgets,
            layout=ipywidgets.Layout(
                display="flex", flex_flow="column", border="solid 2px", align_items="stretch", width="100%"
            ),
        )

    def delete_solution_on_click(self, output, update_git=True, update_db=True):
        cinfo = bulkhours_premium.tools.get_config(is_namespace=True)
        bulkhours_premium.firebase.delete_documents(cinfo, self.ws["exercices"].value, verbose=True)

    def submit_on_click(self, output, update_git=True, update_db=True):
        config = bulkhours_premium.tools.get_config()
        cinfo = bulkhours_premium.tools.get_config(is_namespace=True)
        notebook_id = config["notebook_id"]

        if config["virtual_room"] != self.ws["virtual_room"].value:
            cmd = (
                f"La salle active passe de '{self.ws['virtual_room'].value}' à '{config['virtual_room']}'"
                if config["global"]["language"] == "fr"
                else f"Set the active room from '{self.ws['virtual_room'].value}' to '{config['virtual_room']}'"
            )
            print(f"\x1b[32m\x1b[1m{cmd}\x1b[m")

            config["virtual_room"] = self.ws["virtual_room"].value

        config["global"].update({k: self.ws[k].value for k in ["chatgpt", "norm20", "restricted", "language"]})

        virtual_rooms = config["global"]["virtual_rooms"].split(";")
        config["global"].update({vroom: self.ws[vroom].value.replace(",", ";") for vroom in virtual_rooms})

        config["notebooks"][notebook_id].update(
            {k: self.ws[k].value.replace(",", ";") for k in ["exercices", "evaluation", "page", "virtual_room"]}
        )

        if update_db:
            bulkhours_premium.firebase.get_document("info", "global", prefix=False, cinfo=cinfo).set(config["global"])
            bulkhours_premium.firebase.get_document("info", notebook_id, prefix=False, cinfo=cinfo).set(
                config["notebooks"][notebook_id]
            )

        with open(tools.get_config_file(subject=config["subject"], cell_id="global"), "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        bulkhours_premium.tools.update_config(config)

        cmd = (
            "Mise à jour des informations du dashboard"
            if config["global"]["language"] == "fr"
            else "Update dashboard information"
        )

        # tools.update_github(update_git, files=[nfname], msg=cmd)


def dashboard(update_git=True, **kwargs):
    """La fonction dashboard permet d'éditer les options d'un cours

    Parameters:
    :param no_admin: Do not show the admin in the summary
    :param reload_cache: input data to do the test
    :param update_git: update data on the cloud

    :return: a note between the minimal note and maximal note
    """

    config = bulkhours_premium.tools.get_config(**kwargs)

    virtual_room, notebook_id = (config.get(v) for v in ["virtual_room", "notebook_id"])

    if "help" in config and config["help"]:
        st = lambda x: f"\x1b[30m\x1b[1m{x}\x1b[m"
        print(st(dashboard.__doc__))

    output = ipywidgets.Output()
    language = config["global"]["language"]

    abuttons = {
        "delete_solution": bulkhours_premium.buttons.SwitchButton(
            "delete_solution",
            width="200px",
            fr=f"Effacer les réponses ({virtual_room})",
            en=f"Delete answers ({virtual_room})",
            language=language,
            sleep_on=2,
        ),
        "save_changes": bulkhours_premium.buttons.SwitchButton(
            "save_changes",
            width="200px",
            fr=f"Sauver les changements",
            en=f"Save changes",
            language=language,
            sleep_on=2,
        ),
    }

    bwidgeta = WidgetDashboard(config, abuttons)

    # bwidgeta = WidgetDashboard(dict(nbid=notebook_id, abuttons=abuttons))
    # bwidgeta = WidgetDashboard(dict(nbid=notebook_id, abuttons=abuttons))
    # print(config)

    def func_delete_solution(b):
        return bulkhours_premium.buttons.update_button(
            b, bwidgeta.cinfo.abuttons["delete_solution"], output, bwidgeta, "delete_solution_on_click"
        )

    bwidgeta.cinfo.abuttons["delete_solution"].b.on_click(func_delete_solution)

    def func_c(b):
        return bulkhours_premium.buttons.update_button(
            b,
            bwidgeta.cinfo.abuttons["save_changes"],
            output,
            bwidgeta,
            "submit_on_click",
            kwargs=dict(update_git=update_git),
        )

    bwidgeta.cinfo.abuttons["save_changes"].b.on_click(func_c)

    # with output:
    IPython.display.display(bwidgeta.widget)
    IPython.display.display(output)
