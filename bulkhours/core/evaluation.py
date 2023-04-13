from IPython.core.magic import Magics, cell_magic, magics_class, line_cell_magic, needs_local_scope
import IPython
import ipywidgets

from .widgets.buttons import get_buttons_list, update_button
from .logins import *
from . import firebase
from . import install
from .widgets.bulk_widget import BulkWidget
from .widgets.code_project import WidgetCodeProject
from . import colors
from . import gpt


@magics_class
class Evaluation(Magics):
    def __init__(self, shell, nid, in_french, api_key):
        super(Evaluation, self).__init__(shell)
        self.nid = nid
        self.in_french = in_french
        self.api_key = api_key
        self.cinfo = None

    @property
    def cell_id(self):
        if self.cinfo.id[0] == "I":
            return self.nid + "_" + self.cinfo.id[1:]
        else:
            return self.cinfo.id

    @line_cell_magic
    @needs_local_scope
    def message_cell_id(self, line, cell="", local_ns=None):
        self.cinfo = install.get_argparser(line, cell)
        firebase.send_answer_to_corrector(self.cinfo, **{self.cinfo.user: cell})

    @line_cell_magic
    @needs_local_scope
    def update_cell_id(self, line, cell="", local_ns=None):
        self.cinfo = install.get_argparser(line, cell)
        if not self.cinfo:
            return

        opts = {
            a.split(":")[0]: cell if a.split(":")[1] == "CELL" else a.split(":")[1]
            for a in self.cinfo.options.split(";")
        }
        firebase.send_answer_to_corrector(self.cinfo, user=self.cinfo.user, **opts)

    @line_cell_magic
    @needs_local_scope
    def evaluation_cell_id(self, line, cell="", local_ns=None):
        self.cinfo = install.get_argparser(line, cell)
        if not self.cinfo:
            return

        output = ipywidgets.Output()
        if self.cinfo.user == "solution":
            colors.set_style(output, "sol_background")

        bwidget = BulkWidget(self.cinfo, cell, in_french=self.in_french)
        abuttons = get_buttons_list(bwidget.get_label_widget(), self.in_french)

        widgets = bwidget.get_widgets()
        gtext = ipywidgets.Text("")

        bbox = []
        ws = []
        for w in self.cinfo.widgets:
            if w == "|":
                bbox.append(ipywidgets.HBox(ws))
                ws = []
            elif w == "w":
                ws += widgets
            elif w == "g":
                ws += [gtext, abuttons[w].b]
            elif w == "l" and abuttons[w] is not None:
                ws.append(abuttons[w])
            elif abuttons[w]:
                ws.append(abuttons[w].b)
        if len(ws) > 0:
            bbox.append(ipywidgets.HBox(ws))

        if self.cinfo.type == "code_project":

            def submit(b):
                return update_button(
                    b, "s", WidgetCodeProject.submit, output, abuttons, [self, bwidget, widgets, output], dict()
                )

            def get_correction(b):
                return update_button(
                    b,
                    "c",
                    WidgetCodeProject.get_core_correction,
                    output,
                    abuttons,
                    [self, bbox[1], bwidget, output],
                    dict(),
                )

        else:

            def submit(b):
                return update_button(
                    b, "s", BulkWidget.submit, output, abuttons, [self, bwidget, widgets, output], dict()
                )

            def get_correction(b):
                return update_button(
                    b, "c", BulkWidget.get_core_correction, output, abuttons, [self, bwidget, widgets], dict()
                )

        abuttons["s"].b.on_click(submit)

        abuttons["c"].b.on_click(get_correction)

        def send_message(b):
            return update_button(b, "m", BulkWidget.send_message, output, abuttons, [self], dict())

        abuttons["m"].b.on_click(send_message)

        def ask_chatgpt(b):
            return update_button(
                b,
                "g",
                gpt.ask_chat_gpt,
                output,
                abuttons,
                [gtext.value],
                dict(api_key=self.api_key, is_code=True, temperature=0.5),
            )

        abuttons["g"].b.on_click(ask_chatgpt)

        def write_exec_process(b):
            return update_button(
                b, "t", WidgetCodeProject.write_exec_process, output, abuttons, [self, bwidget], dict()
            )

        abuttons["t"].b.on_click(write_exec_process)

        if self.cinfo.type == "code" and cell != "":
            with output:
                if self.cinfo.user == "solution":
                    colors.set_style(output, "sol_background")
                self.shell.run_cell(cell)
        elif self.cinfo.type == "markdown":
            IPython.display.display(IPython.display.Markdown(cell))
        elif self.cinfo.type == "formula":
            IPython.display.display(IPython.display.Markdown("$" + cell + "$"))
            print("$" + cell + "$")
        elif self.cinfo.type == "code_project":
            bwidget.widget.basic_execution(bbox[1], bwidget, output)

        bbox = bbox[0] if len(bbox) == 1 else ipywidgets.VBox(bbox)
        IPython.display.display(bbox, output)
