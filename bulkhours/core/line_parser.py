import re
import argparse
import json
import os
from .colors import st
import IPython

from . import tools
from .cache_manager import CacheManager


def format_opts(argv):
    """This function merges arguments together
    Example:
    -i cell_d -c Salut les gars becomes
    ['-i', 'cell_id', '-c', 'Salut__space__les__space__gars']
    instead of
    ['-i', 'cell_id', '-c', 'Salut', 'les', 'gars']
    With format_func, it will become:
    ['-i', 'cell_id', '-c', 'Salut les gars']
    """
    nargv = []
    for a in argv:
        if a[0] != "-" and nargv[-1][0] != "-":
            nargv[-1] += " " + a
        else:
            nargv.append(a)
    return [tools.format_opt(a) for a in nargv]


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
        "--tags",
        default="",
        help=st("Tags caracteristiques de l'exercice"),
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
    basic.add_argument(
        "-r",
        "--rdir",
        default="",
        help=st("directory of the test"),
    )

    basic.add_argument(
        "--hide", dest="hide", action="store_true", help=st("L'exercice est caché initialement")
    )

    if is_admin:
        admin = parser.add_argument_group("Options d'administration")

        admin.add_argument(
            "-u",
            "--user",
            default=None,
            help=st("Identifiant de l'utilisateur soumettant la réponse"),
        )
        admin.add_argument(
            "-a",
            "--answer",
            default="",
            help=st("Fonctionnalité beta pour un serveur jupyter local"),
        )

    meta_options = parser.add_argument_group("Options méta")
    meta_options.add_argument(
        "-h", "--help", dest="help", action="store_true", help=st("Affiche ce texte")
    )
    meta_options.add_argument(
        "-p",
        "--puppet",
        default="",
        help=st("Fonctionnalité beta pour un serveur jupyter local"),
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
                "hide",
                "options",
                "language",
                "restricted",
                "is_locked",
                "chatgpt",
                "norm20",
                "notebook_id",
                "subject",
                "rdir",
                "virtual_room",
                "user",
            ]
            if hasattr(self, v)
        ]
        return ", ".join(info)

    @classmethod
    def from_bkc(cls, exercise, cshortname, shortname, groupname, user=tools.REF_USER):
        cinfo = cls(f"%%evaluation_cell_id -i {exercise}", "\n", is_cell=True)
        cinfo.subject = cshortname
        cinfo.notebook_id = shortname
        cinfo.virtual_room = groupname
        cinfo.user = user
        return cinfo

    @classmethod
    def from_cell_id_user(cls, cell_id, user=tools.REF_USER):
        cinfo = cls(f"%%evaluation_cell_id -i {cell_id}", "\n", is_cell=True)
        cinfo.user = user
        return cinfo

    def __init__(self, line, cell_source, is_cell=True):
        self.init(line, cell_source, is_cell=is_cell)

    def init(self, line, cell_source, is_cell=True):
        # Get the options (The first "-" found")
        opts_line = line[line.find("-") :]

        # get options
        self.line, cell = line, cell_source
        cfg = tools.get_config()
        self.is_admin = tools.is_admin(cfg=cfg)

        if opts_line != "":
            parser = get_argparser(self.is_admin)
            pdata = parser.parse_args(format_opts(opts_line.split()))
            if pdata.help:
                parser.print_help()

            for k, v in vars(pdata).items():
                setattr(
                    self,
                    k,
                    tools.format_opt(v, raw2norm=False) if v and v is not None else v,
                )
        else:
            # print("Line is empty")
            return

        available_widgets = get_available_widgets()
        if self.is_admin:
            ewidgets = "oa"  # if "def student_evaluation_function" in cell else "o"
            available_widgets = {k: v + ewidgets for k, v in available_widgets.items()}

        if not hasattr(self, "widgets") or self.widgets is None:
            self.widgets = (
                available_widgets[self.type]
                if self.type in available_widgets
                else available_widgets["default"]
            )
        
        if cfg is not None:
            for p in ["language", "restricted", "chatgpt", "norm20", "subject"]:
                if p in cfg.g:
                    setattr(self, p, cfg.g[p])

            if not hasattr(self, "user") or self.user is None:
                self.user = cfg.email

            for p in ["notebook_id", "virtual_room"]:
                setattr(self, p, cfg[p])

        mode = "production" if cfg is None or "mode" not in cfg else cfg["mode"]
        if mode == "passive":
            self.widgets = self.widgets.replace("s", "")
        if mode == "production" and self.is_admin:
            self.widgets = self.widgets.replace("s", "").replace("c", "")

        if not hasattr(self, "cell_id"):
            return

        if IPython.get_ipython() and self.rdir != "":
            with IPython.utils.io.capture_output() as captured:
                IPython.get_ipython().run_cell(f"%cd {self.rdir}")

        for a in ["student", "teacher"]:
            o = f"{a}.{self.cell_id}"
            if o not in CacheManager.objects:
                CacheManager.objects[o] = dict()
                if IPython.get_ipython():
                    IPython.get_ipython().run_cell(
                        f"from argparse import Namespace\n{o} = Namespace()"
                    )

            for l in cell_source.splitlines():
                if o == l.replace(" ", "")[: len(o)]:
                    args = l.split(".")
                    if len(args) > 2:
                        v = args[2].split()[0]
                        ov = args[2].replace("'", '"').split('"')
                        if (
                            len(ov := args[2].replace("'", '"').split('"')) == 3
                        ):  # For string
                            CacheManager.objects[o][v] = ov[1]
                            setattr(self, v, ov[1])
                        elif len(ov := args[2].split("=")) == 2:  # Otherwise
                            CacheManager.objects[o][v] = ov[1]
                            setattr(self, v, ov[1])
                        else:  # Fuck, I don't what is going on
                            CacheManager.objects[o][v] = ov

        if is_cell:
            CacheManager.objects["current_cell"] = self.cell_id
            os.environ["BULK_CELL_ID"] = self.cell_id

    @staticmethod
    def get_func_args(code, func_id="bulkhours.is_equal"):
        args = code.replace(" ", "").split(func_id)
        if len(args) == 1:
            return {}

        args = re.split(r",\s*(?![^()]*\))", args[1][1 : args[1].rfind(")")])

        if func_id == "bulkhours.is_equal":
            kwargs = ["norm", "error", "policy", "min_score", "max_score", "cmax_score"]
        else:
            kwargs = ["debug", "run", "min_score", "max_score"]

        fargs = {}
        for i, a in enumerate(args):
            sa = a.split("=")

            if func_id == "bulkhours.is_equal" and i == 0:
                if sa[0].replace(" ", "") == "data_test" and len(sa) > 1:
                    fargs["data_test"] = "=".join(sa[1:])
                else:
                    fargs["data_test"] = a
            elif func_id == "bulkhours.is_equal" and i == 1:
                if sa[0].replace(" ", "") == "data_ref":
                    fargs["data_ref"] = "=".join(sa[1:])
                elif sa[0].replace(" ", "") in kwargs:
                    fargs[sa[0]] = "=".join(sa[1:])
                else:
                    fargs["data_ref"] = a
            elif "=" in a:
                fargs[sa[0]] = "=".join(sa[1:])

        if func_id == "bulkhours.is_equal" and "data_ref" not in fargs:
            fargs["data_ref"] = fargs["data_test"].replace("student.", "teacher.")

        return fargs
