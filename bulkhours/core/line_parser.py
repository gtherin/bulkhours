import argparse
import json
import os
from .colors import st
import IPython

from . import tools
from .cache_manager import CacheManager


def format_opt(label, raw2norm=True):
    rr = {"-": "__minus__", "@": "__at__", " ": "__space__", "/": "__slash__"}
    if len(label) > 0 and label[0] != "-":
        for k, v in rr.items():
            label = label.replace(k, v) if raw2norm else label.replace(v, k)
    return label


def format_opts(argv):
    nargv = []
    for a in argv:
        if a[0] != "-" and nargv[-1][0] != "-":
            nargv[-1] += " " + a
        else:
            nargv.append(a)
    return [format_opt(a) for a in nargv]


def get_available_widgets():
    jsonfile = os.path.dirname(__file__) + "/widgets.json"
    with open(jsonfile) as json_file:
        return json.load(json_file)


def get_argparser(is_admin):
    parser = argparse.ArgumentParser(
        prog="%%evaluation_cell_id",
        add_help=False,
        description=st(
            """La fonction magique 'evaluation_cell_id' permet d'identifier une cellule pour pouvoir evaluer son contenu"""
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    basic = parser.add_argument_group("Options de base")
    basic.add_argument(
        "-i",
        "--cell-id",
        default=None,
        required=True,
        help=st(
            """Identifiant unique de la cellule (pour un triplet 'subject/virtual_room/notebook_id')
Il permet de faire correspondre la cellule avec sa solution"""
        ),
    )

    available_widgets = get_available_widgets()
    basic.add_argument(
        "-t",
        "--type",
        default="bkcode",
        choices=list(available_widgets.keys()),
        help=st("Pour les différents types de cellules connus"),
    )

    basic.add_argument(
        "-w",
        "--widgets",
        default=None,
        help=st(
            f"""Identifiant de l'utilisateur soumettant la réponse 
            {available_widgets}"""
        ),
    )

    basic.add_argument(
        "-l",
        "--label",
        type=str,
        default="",
        help=st("Label permettant"),
    )

    basic.add_argument(
        "-o",
        "--options",
        default="",
        help=st("Identifiant de l'utilisateur soumettant la réponse"),
    )

    basic.add_argument(
        "-d",
        "--default",
        default="",
        help=st("Fonctionnalité beta pour un serveur jupyter local"),
    )

    if is_admin:
        admin = parser.add_argument_group("Options d'administration")

        admin.add_argument("-u", "--user", default=None, help=st("Identifiant de l'utilisateur soumettant la réponse"))
        admin.add_argument("-a", "--answer", default="", help=st("Fonctionnalité beta pour un serveur jupyter local"))
    meta_options = parser.add_argument_group("Options méta")

    meta_options.add_argument("-h", "--help", dest="help", action="store_true", help=st("Affiche ce texte"))
    meta_options.add_argument(
        "-p", "--puppet", default="", help=st("Fonctionnalité beta pour un serveur jupyter local")
    )

    return parser


class LineParser:
    def __repr__(self):
        info = [
            f"{v}={getattr(self, v)}"
            for v in [
                "cell_id",
                "type",
                "answer",
                "default",
                "label",
                "options",
                "language",
                "restricted",
                "chatgpt",
                "norm20",
                "notebook_id",
                "subject",
                "virtual_room",
                "user",
            ]
            if hasattr(self, v)
        ]
        return ", ".join(info)

    def __init__(self, line, cell_source, is_cell=True):
        if "evaluation_cell_id " in line:
            line = line.split("evaluation_cell_id ")[-1]

        self.line, cell = line, cell_source
        config = tools.get_config()
        self.is_admin = tools.is_admin(config=config)

        if line != "":
            parser = get_argparser(self.is_admin)
            pdata = parser.parse_args(format_opts(line.split()))
            if pdata.help:
                parser.print_help()

            for k, v in vars(pdata).items():
                setattr(self, k, format_opt(v, raw2norm=False) if v and v is not None else v)

        available_widgets = get_available_widgets()
        if self.is_admin:
            ewidgets = "oa" if "def student_evaluation_function" in cell else "o"
            available_widgets = {k: v + ewidgets for k, v in available_widgets.items()}

        if hasattr(self, "widgets") and self.widgets is None:
            self.widgets = (
                available_widgets[self.type] if self.type in available_widgets else available_widgets["default"]
            )

        for p in ["language", "restricted", "chatgpt", "norm20", "subject"]:
            if p in config["global"]:
                setattr(self, p, config["global"][p])

        if not hasattr(self, "user") or self.user is None:
            self.user = config["email"]

        for p in ["notebook_id", "virtual_room"]:
            setattr(self, p, config[p])

        if not hasattr(self, "cell_id"):
            return

        self.icell_id = self.notebook_id + "_" + self.cell_id

        for a in ["student", "teacher"]:
            o = f"{a}.{self.cell_id}"
            if o not in CacheManager.objects:
                CacheManager.objects[o] = dict()
                IPython.get_ipython().run_cell(f"from argparse import Namespace\n{o} = Namespace()")

            for l in cell_source.splitlines():
                if o == l.replace(" ", "")[: len(o)]:
                    args = l.split(".")
                    if len(args) > 2:
                        v = args[2].split()[0]
                        ov = args[2].replace("'", '"').split('"')
                        if len(ov := args[2].replace("'", '"').split('"')) == 3:  # For string
                            CacheManager.objects[o][v] = ov[1]
                            setattr(self, v, ov[1])
                        elif len(ov := args[2].split("=")) == 2:  # Otherwise
                            CacheManager.objects[o][v] = ov[1]
                            setattr(self, v, ov[1])
                        else:  # Fuck, I don't what is going on
                            CacheManager.objects[o][v] = ov

        if is_cell:
            CacheManager.objects["current_cell"] = self.cell_id
            os.environ["BLK_CELL_ID"] = self.icell_id
