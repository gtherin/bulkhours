from IPython.core.magic import Magics, cell_magic, magics_class, line_cell_magic, needs_local_scope
import IPython
import ipywidgets

from .widgets.buttons import get_buttons_list, update_button
from .logins import *
from . import firebase
from . import install
from .widgets import bulk_widget as widget_helper
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

        bwidget = widget_helper.create_widget(self.cinfo, cell, self.in_french, self.shell)
        abuttons = get_buttons_list(bwidget.get_label_widget(), self.in_french)
        gtext = ipywidgets.Text("")

        bbox = []
        ws = []
        for w in self.cinfo.widgets:
            if w == "|":
                bbox.append(ipywidgets.HBox(ws))
                ws = []
            elif w == "w":
                ws += [bwidget.widget]
            elif w == "g":
                ws += [gtext, abuttons[w].b]
            elif w == "l" and abuttons[w] is not None:
                ws.append(abuttons[w])
            elif abuttons[w]:
                ws.append(abuttons[w].b)
        if len(ws) > 0:
            bbox.append(ipywidgets.HBox(ws))

        def get_exec_line(l, func):
            return f"""def func_{l}(b): return update_button(b, "{l}", {func}, output, abuttons, [bwidget, output], dict())"""

        butts = {"m": "send_message", "t": "write_exec_process", "c": "display_correction", "s": "submit"}

        def func_m(b):
            return update_button(b, "m", bwidget.__class__.send_message, output, abuttons, [bwidget, output], dict())

        def func_t(b):
            return update_button(
                b, "t", bwidget.__class__.write_exec_process, output, abuttons, [bwidget, output], dict()
            )

        def func_c(b):
            return update_button(
                b, "c", bwidget.__class__.display_ecorrection, output, abuttons, [bwidget, output], dict()
            )

        def func_s(b):
            return update_button(b, "s", bwidget.__class__.submit, output, abuttons, [bwidget, output], dict())

        def func_a(b):
            return update_button(
                b,
                "g",
                gpt.ask_chat_gpt,
                output,
                abuttons,
                [gtext.value],
                dict(api_key=self.api_key, is_code=True, temperature=0.5),
            )

        for l, func in butts.items():
            exec("""abuttons["{l}"].b.on_click(func_{l})""".format(l=l))
        exec("""abuttons["g"].b.on_click(func_a)""")

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
            bwidget.basic_execution(bbox[1], bwidget, output)
            return

        bbox = bbox[0] if len(bbox) == 1 else ipywidgets.VBox(bbox)
        IPython.display.display(bbox, output)
