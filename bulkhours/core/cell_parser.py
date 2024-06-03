import datetime

from .line_parser import LineParser
from .grade import Grade
from . import tools


def cell_reset(source):
    """
    # BULKHOURS.REMOVE:START
        # This code won't appear in the reset generation
        # It will appear on the solution though
    # BULKHOURS.REMOVE:END

    # BULKHOURS.PRINT:raw_std = gdf[f"ret_{i}"].ewm(20).std()
        # The previous line will be printed in the reset generation
        # The previous line won't be printed in the solution generation

    print(models["fit1"].forecast(3)) # BULKHOURS.REMOVE:LINE
        # The previous line won't be printed in the reset generation
        # The previous line will be printed in the solution generation

    df["noise"] = sp.stats.norm(loc=3, scale=0.3).rvs(n) # BULKHOURS.INIT:0
    """

    separator = "//" if "//BULKHOURS" in source.replace(" ", "") else "#"
    nsource = []
    keep_line = True


    message = "❗A vous de jouer❗" if 1 else "❗Your code❗"
    message = "" if "//BULKHOURS" in source.replace(" ", "") in source else message

    for s in source.split("\n"):
        s = s.replace("BKRESET", "BULKHOURS")
        if "BULKHOURS." in s:
            l = s.split("BULKHOURS.")
            if "INIT:" in l[1]:
                if "=" in s:
                    s = (
                        s.split("=")[0]
                        + "= "
                        + l[1].replace("INIT:", "")
                        + f"  {separator} ...{message}"
                    )
                elif "return " in s:
                    s = (
                        s.split("return ")[0]
                        + "return "
                        + l[1].replace("INIT:", "")
                        + f"  {separator} ...{message}"
                    )
            if "REMOVE" in l[1]:
                if "START" in l[1]:
                    keep_line = False
                elif "END" in l[1]:
                    keep_line = True
                    s = s.split(separator)[0] + separator + " ...{message}"
                else:
                    indentation = len(s) - len(s.lstrip())
                    s = (" " * indentation) + separator + " ...{message}"
            if "REPLACE" in l[1]:
                indentation = len(s) - len(s.lstrip())
                s = (
                    (" " * indentation)
                    + l[1].replace("REPLACE:", "")
                    + f"  {separator} ..."
                )
            if "PRINT" in l[1]:
                indentation = len(s) - len(s.lstrip())
                s = (" " * indentation) + l[1].replace("PRINT:", "")

        if keep_line:
            nsource.append(s)

    code = "\n".join(nsource)
    for _ in range(3):
        if len(code) > 0 and code[-1] == "\n":
            code = code[:-1]
    # print(code)
    return code


def cell_solution(source):
    separator = "//" if "// BULKHOURS" not in source else "#"
    nsource = []
    for s in source.split("\n"):
        s = s.replace("BKRESET", "BULKHOURS")
        if "BULKHOURS." in s:
            l = s.split("BULKHOURS.")
            if "REMOVE:START" in l[1] or "REMOVE:END" in l[1] or "PRINT" in l[1]:
                continue
            elif "INIT:" in l[1] or "REPLACE:" in l[1] or "REMOVE" in l[1]:
                s = l[0][: l[0].rfind(separator)]

        nsource.append(s)

    code = "\n".join(nsource)
    for _ in range(3):
        if len(code) > 0 and code[-1] == "\n":
            code = code[:-1]
    # print(code)
    return code


class CellParser:
    meta_modes = ["evaluation", "explanation", "hint"]

    @classmethod
    def crunch_data(cls, cinfo=None, user=None, data=None, output=None):
        if data is None:
            from . import firebase

            data = firebase.get_solution_from_corrector(
                cinfo.cell_id, corrector=user, cinfo=cinfo
            )
        if user is not None:
            cinfo.user = user

        return cls(cinfo, data, output=output)

    def __init__(self, cinfo, cell_source, output=None):
        self.parse_cell(cinfo, cell_source)

        if (
            "atype" in self.minfo
            and self.minfo["atype"] == "code_project"
            and "Makefile" in self.minfo
            and "answer" not in self.minfo
        ):
            self.minfo["answer"] = ""
            for k, v in self.minfo.items():
                if "_dot_h" in k or "_dot_cpp" in k:  # or "Makefile" in k:
                    self.minfo["answer"] += f"//////// {k} ////////\n{v}\n"
            self.raw_exec_code = self.minfo["answer"]
            self.minfo["main_execution"] = self.minfo["answer"]
            self.minfo["user"] = self.cinfo.user

        if output is not None and hasattr(output, "outputs"):
            self.outputs = output.outputs
        else:
            self.outputs = []

    def get_update_time(self):
        return (
            self.minfo["update_time"]
            if "update_time" in self.minfo
            else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

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
        # self.parse_cell(self.cinfo, self.cell_source)

        if c in self.minfo:
            if type(self.minfo[c]) == str:
                return self.minfo[c]
            if type(self.minfo[c]) == dict and "code" in self.minfo[c]:
                return self.minfo[c]["code"]

        return ""

    def is_manual_note(self):
        return "grade_man" in self.minfo

    def has_answer(self):
        return "answer" in self.minfo and self.minfo["answer"] != ""

    @property
    def max_score(self):
        return (
            self.minfo["evaluation"]["max_score"]
            if "max_score" in self.minfo["evaluation"]
            else self.minfo["evaluation"]["emp_max_score"]
        )

    def is_cell_type(self):
        return self.cinfo.type in ["bkcode", "bkscript"]

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

    def is_evaluation_available(self):
        return "evaluation" in self.minfo and self.minfo["evaluation"] != ""

    def get_grade(self, level=None):
        return Grade.create_from_info(self.minfo, level=level)

    def do_run_evaluation(self):
        return self.is_evaluation_available() and (
            "run=true" in self.get_code("evaluation").lower()
            or "\nstudent_evaluation_function(" in self.get_code("main_execution")
        )

    def is_evaluation_visible(self):
        if self.cell_source is None:
            return False
        return "visible" not in self.minfo or self.minfo["visible"]

    def is_explanation_available(self):
        return "explanation" in self.minfo and self.minfo["explanation"] != ""

    def is_hint_available(self):
        return "hint" in self.minfo and self.minfo["hint"] != ""

    def block_is_start(self, l, func_id):
        return (
            f"def {func_id}(" in l or f"float {func_id}(" in l or f"int {func_id}(" in l
        )

    def block_is_end(self, l):
        return len(l) > 0 and l[0] != " "

    def block_end(self, l):
        # Remove endline for c++ function
        if l[0] == "}":
            l = ""
        return l

    def block_start(self, l, tmode, func_id):
        self.minfo[tmode] = LineParser.get_func_args(l, func_id=func_id)
        self.minfo[tmode]["visible"] = True
        if tmode == "evaluation":
            self.minfo[tmode]["emp_max_score"] = 0

    def block_equal_line(self, mode, l):
        args = LineParser.get_func_args(l, func_id="bulkhours.is_equal")

        if "data_ref" not in args:
            args["data_ref"] = args["data_test"].replace("student.", "teacher.")
        args["min_score"] = float(args["min_score"]) if "min_score" in args else 0
        args["max_score"] = float(args["max_score"]) if "max_score" in args else 10

        if "equals" not in self.minfo[mode]:
            self.minfo[mode]["equals"] = []

        self.minfo[mode]["equals"].append(args)
        self.minfo[mode]["emp_max_score"] += args["max_score"]

        func = "bulkhours.is_equal"
        l2 = l[: l.rfind(func) + len(func)] + "(%s)\n" % (
            ", ".join([f"{k}={v}" for k, v in args.items()]),
        )
        # indent = " " * (re.sub(r"^([\s]*)[\s]+.*$", r"\g<1>", l).count(" ") + 1)
        # l = f"{indent}try:\n    {l}\n{indent}except:\n{indent}    print('FINAL_SCORE={min_score}/{max_score}')\n"

        return l2

    def get_dbcell_decomposition(self):
        info = {
            "main_execution": self.get_code("main_execution"),
            "explanation": self.get_code("explanation"),
            "hint": self.get_code("hint"),
            "evaluation": self.get_code("evaluation"),
            "answer": self.minfo["answer"]
            if self.has_answer()
            else self.get_code("main_execution"),
            "atype": self.cinfo.type,
            "visible": True,
            "user": self.cinfo.user,
        }

        for o in self.outputs:
            if "name" in o and "text" in o:
                info["output_" + o["name"]] = o["text"]

        return info

    def parse_cell(self, cinfo, cell_source):
        self.cinfo, self.cell_source = cinfo, cell_source

        # If cell_source is already a dictionary, no need to parse anymore
        if type(cell_source) == dict:
            self.minfo = cell_source
            if "main_execution" in self.minfo:
                self.raw_exec_code = self.minfo["main_execution"]
                self.raw_code = "\n".join(
                    [
                        cell_source[e]
                        for e in ["main_execution"] + CellParser.meta_modes
                        if e in cell_source
                    ]
                )
            else:
                self.raw_code, self.raw_exec_code = "", ""
            self.cinfo = self.minfo["cinfo"] if "cinfo" in self.minfo else cinfo
            return
        # Otherwise, parse

        # Parse to create a dictionary
        self.raw_code = cell_source
        self.minfo = {}

        # Init minfo code blocks
        for tmode in ["main_execution"] + CellParser.meta_modes:
            if tmode in self.minfo and "code" in self.minfo[tmode]:
                self.minfo[tmode]["code"] = ""

        # By default, the parsed code goes to the 'main_execution' block of code
        mode = "main_execution"
        self.store_info(mode, "", ekey="code", verbose=False)

        if self.raw_code is not None:
            for l in self.raw_code.splitlines():
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
                    info = LineParser(l, self.raw_code, is_cell=False)
                    self.minfo[info.cell_id] = vars(info)

                if ".is_equal" in l:
                    l = self.block_equal_line(mode, l)

                self.store_info(mode, l + "\n", ekey="code", verbose=False)

        self.raw_exec_code = self.minfo["main_execution"]["code"]

        if self.is_cell_type():
            self.minfo["answer"] = self.get_solution()
        else:
            self.raw_exec_code = self.minfo["main_execution"]["code"]
            if "user" in self.minfo and self.minfo["user"] == tools.REF_USER:
                self.minfo["main_execution"]["code"] = self.get_solution()

    def get_solution(self):
        return cell_solution(self.raw_exec_code)

    def get_reset(self):
        return cell_reset(self.raw_exec_code)
