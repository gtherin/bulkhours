import re

from .line_parser import LineParser


def get_equals_args(code, func_id="bulkhours.is_equal"):
    args = code.replace(" ", "").split(func_id)
    if len(args) == 1:
        return {}

    args = re.split(r",\s*(?![^()]*\))", args[1][1 : args[1].rfind(")")])

    fargs = {}
    for i, a in enumerate(args):
        if i == 0 and "=" not in a:
            fargs["data_test"] = a
        elif i == 1 and "=" not in a:
            fargs["data_ref"] = a.replace("student.", "teacher.")
        elif "=" in a:
            fargs[a.split("=")[0]] = a.split("=")[1]

    return fargs


class CellParser:
    meta_modes = ["evaluation", "explanation", "hint"]

    def __init__(self, parse_cell=False, **kwargs):
        # Reformat db info to cell format
        if "cell_source" in kwargs and type(cell_source := kwargs["cell_source"]) == dict:
            raw_code = [cell_source[e] for e in ["main_execution"] + CellParser.meta_modes if e in cell_source]
            kwargs["cell_source"] = "\n".join(raw_code)

        self.is_cell_source = "cell_source" in kwargs and type(kwargs["cell_source"]) == str
        self.minfo = kwargs
        if parse_cell and self.is_cell_source:
            self.get_cell_decomposition()

    def store_info(self, key, val, ekey=None, verbose=False):
        if key not in self.minfo:
            self.minfo[key] = {}

        if ekey == "code":
            if ekey not in self.minfo[key]:
                self.minfo[key][ekey] = ""
            self.minfo[key][ekey] += val
            if verbose:
                print(f"{self.user}::{key}={val}", end="")

        elif ekey is None:
            self.minfo[key] = val
        else:
            self.minfo[key][ekey] = val

    def get_code(self, c):
        # TODO: Fix this hack. Need to be run to avoid problems, if not launched, solution=user
        self.get_cell_decomposition()
        return self.minfo[c]["code"] if c in self.minfo and "code" in self.minfo[c] else ""

    @property
    def max_score(self):
        return (
            self.minfo["evaluation"]["max_score"]
            if "max_score" in self.minfo["evaluation"]
            else self.minfo["evaluation"]["emp_max_score"]
        )

    def is_cell_type(self):
        return self.minfo["cinfo"] in ["bkcode", "bkscript"]

    @staticmethod
    def c2python(l):
        for tmode in CellParser.meta_modes:
            func_id = f"student_{tmode}_function"
            for t in ["float", "int", "bool"]:
                if f"{t} {func_id}" in l:
                    l = (
                        l.replace(f"{t} {func_id}(", f"def {func_id}(")
                        .replace(";", "")
                        .replace("{", ":")
                        .replace("bool ", "")
                        .replace("true", "True")
                        .replace("false", "False")
                    )
        return l

    @staticmethod
    def remove_meta_functions_execution(code):
        ncode = ""
        for l in code.splitlines():
            if l.split("(")[0] not in [f"student_{m}_function" for m in CellParser.meta_modes]:
                ncode += l + "\n"
        return ncode

    @classmethod
    def crunch_data(cls, cinfo, user, data=None):
        if data is None:
            from . import firebase

            data = firebase.get_solution_from_corrector(cinfo.cell_id, corrector=user, cinfo=cinfo)
        return cls(cinfo=cinfo, parse_cell=True, cell_source=data, user=user, source="")

    def is_evaluation_available(self):
        return "evaluation" in self.minfo and self.minfo["evaluation"] != ""

    def do_run_evaluation(self):
        return self.is_evaluation_available() and (
            "run=true" in self.get_code("evaluation").lower()
            or "\nstudent_evaluation_function(" in self.get_code("main_execution")
        )

    def is_evaluation_visible(self):
        if self.minfo["cell_source"] is None:
            return False
        return "visible" not in self.minfo or not self.minfo["visible"]

    def is_explanation_available(self):
        return "explanation" in self.minfo and self.minfo["explanation"] != ""

    def is_hint_available(self):
        return "hint" in self.minfo and self.minfo["hint"] != ""

    def block_is_start(self, l, func_id):
        return f"def {func_id}(" in l or f"float {func_id}(" in l or f"int {func_id}(" in l

    def block_is_end(self, l):
        return len(l) > 0 and l[0] != " "

    def block_end(self, l):
        # Remove endline for c++ function
        if l[0] == "}":
            l = ""
        return l

    def block_start(self, l, tmode, func_id):
        self.minfo[tmode] = get_equals_args(l, func_id=func_id)
        self.minfo[tmode]["visible"] = True
        if tmode == "evaluation":
            self.minfo[tmode]["emp_max_score"] = 0

    def block_equal_line(self, mode, l):
        indent = " " * (re.sub(r"^([\s]*)[\s]+.*$", r"\g<1>", l).count(" ") + 1)
        args = get_equals_args(l, func_id="bulkhours.is_equal")
        if "data_ref" not in args:
            args["data_ref"] = args["data_test"].replace("student.", "teacher.")
        args["min_score"] = float(args["min_score"]) if "min_score" in args else 0
        args["max_score"] = float(args["max_score"]) if "max_score" in args else 10

        """if "data_ref" not in args and "data_test" in args:
            if "student." in args["data_test"]:
                l = l[: l.rfind(")")] + ", data_ref=%s)" % args["data_test"].replace("student.", "teacher.")
            else:
                l = l[: l.rfind(")")] + f", data_ref=teacher.{args['data_test']})"

        if (
            "data_test" in args
            and "student." in args["data_test"]
            and "data_ref" in args
            and "teacher." not in args["data_ref"]
        ):
            l = f"{indent}{args['data_test'].replace('student.', 'teacher.')} = {args['data_ref']}\n{l}  # cleaned"
        """
        if "equals" not in self.minfo[mode]:
            self.minfo[mode]["equals"] = []

        self.minfo[mode]["equals"].append(args)
        self.minfo[mode]["emp_max_score"] += args["max_score"]

        func = "bulkhours.is_equal"
        l2 = l[: l.rfind(func) + len(func)] + "(%s)\n" % (", ".join([f"{k}={v}" for k, v in args.items()]),)
        # indent = " " * (re.sub(r"^([\s]*)[\s]+.*$", r"\g<1>", l).count(" ") + 1)
        # if not do_debug:
        #    l = f"{indent}try:\n    {l}\n{indent}except:\n{indent}    print('FINAL_SCORE={min_score}/{max_score}')\n"
        # print(l)
        # print(l2)

        return l2

    def get_dbcell_decomposition(self):
        info = {
            "main_execution": self.get_code("main_execution"),
            "explanation": self.get_code("explanation"),
            "hint": self.get_code("hint"),
            "evaluation": self.get_code("evaluation"),
            "answer": self.minfo["answer"],
        }
        info["atype"] = self.minfo["cinfo"].type
        info["visible"] = True
        info["user"] = self.minfo["user"]

        return info

    def get_cell_decomposition(self):
        cell_source, cell_id = self.minfo["cell_source"], self.minfo["cinfo"].cell_id
        for tmode in ["main_execution"] + CellParser.meta_modes:
            if tmode in self.minfo and "code" in self.minfo[tmode]:
                self.minfo[tmode]["code"] = ""

        mode = "main_execution"
        self.store_info(mode, "", ekey="code", verbose=False)
        if cell_source is None:
            return

        for l in cell_source.splitlines():
            l = CellParser.c2python(l)

            for tmode in CellParser.meta_modes:
                func_id = f"student_{tmode}_function"

                # Switch modes
                if self.block_is_start(l, func_id):
                    self.block_start(l, mode := tmode, func_id)

                elif mode == tmode and self.block_is_end(l):
                    mode, l = "main_execution", self.block_end(l)

                # Remove execution lines for meta functions
                if l.split("(")[0] in [f"student_{tmode}_function("]:
                    l = ""

            if "%evaluation_cell_id" == l.replace(" ", "").split("-")[0]:
                info = LineParser(l, cell_source, is_cell=False)
                self.minfo[cell_id] = vars(info)

            if ".is_equal" in l:
                l = self.block_equal_line(mode, l)

            self.store_info(mode, l + "\n", ekey="code", verbose=False)

        if self.is_cell_type():
            self.minfo["answer"] = cell_source
        else:
            self.minfo["answer"] = self.minfo["main_execution"]["code"]
