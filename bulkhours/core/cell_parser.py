import re
from .line_parser import LineParser


def cell_reset(source):
    """
# BKRESET.REMOVE:START
    # This code won't appear in the reset generation
    # It will appear on the solution though
# BKRESET.REMOVE:END

# BKRESET.PRINT:raw_std = gdf[f"ret_{i}"].ewm(20).std()
    # The previous line will be printed in the reset generation
    # The previous line won't be printed in the solution generation

print(models["fit1"].forecast(3)) # BKRESET.REMOVE:LINE
    # The previous line won't be printed in the reset generation
    # The previous line will be printed in the solution generation
    
df["noise"] = sp.stats.norm(loc=3, scale=0.3).rvs(n) # BKRESET.INIT:0
    """
    nsource = []

    keep_line = True

    for s in source.split("\n"):
        if "BKRESET." in s:
            l = s.split("BKRESET.")
            if "INIT:" in l[1]:
                if "=" in s:
                    s = s.split("=")[0] + "= " + l[1].replace("INIT:", "") + "  # ..."
                elif "return " in s:
                    s = s.split("return ")[0] + "return " + l[1].replace("INIT:", "") + "  # ..."
            if "REMOVE" in l[1]:
                if "START" in l[1]:
                    keep_line = False
                elif "END" in l[1]:
                    keep_line = True
                    s = s.split("#")[0] + "# ..."
                else:
                    indentation = len(s) - len(s.lstrip())
                    s = (" " * indentation) + "# ..."
            if "REPLACE" in l[1]:
                indentation = len(s) - len(s.lstrip())
                s = (" " * indentation) + l[1].replace("REPLACE:", "") + "  # ..."
            if "PRINT" in l[1]:
                indentation = len(s) - len(s.lstrip())
                s = (" " * indentation) + l[1].replace("PRINT:", "")

        if keep_line:
            nsource.append(s)

    #print("\n".join(nsource))
    return "\n".join(nsource)

def cell_solution(source):

    nsource = []
    for s in source.split("\n"):
        if "BKRESET." in s:
            l = s.split("BKRESET.")
            if "REMOVE:START" in l[1] or "REMOVE:END" in l[1] or "PRINT" in l[1]:
                continue
            elif "INIT:" in l[1] or "REPLACE:" in l[1] or "REMOVE" in l[1]:
                s = l[0][:l[0].rfind("#")]

        nsource.append(s)

    # print("\n".join(nsource))
    return "\n".join(nsource)


class CellParser:
    meta_modes = ["evaluation", "explanation", "hint"]

    @classmethod
    def from_data(cls, data):

        return cls(cinfo=cinfo, parse_cell=True, cell_source=data, user=user, source="")

    @classmethod
    def crunch_data(cls, cinfo, user, data=None):
        if data is None:
            from . import firebase

            data = firebase.get_solution_from_corrector(cinfo.cell_id, corrector=user, cinfo=cinfo)
        return cls(cinfo=cinfo, parse_cell=True, cell_source=data, user=user, source="")

    def __init__(self, parse_cell=True, **kwargs):
        # Reformat db info to cell format
        if "cell_source" in kwargs and type(cell_source := kwargs["cell_source"]) == dict:
            raw_code = [cell_source[e] for e in ["main_execution"] + CellParser.meta_modes if e in cell_source]
            kwargs["cell_source"] = "\n".join(raw_code)

        self.is_cell_source = "cell_source" in kwargs and type(kwargs["cell_source"]) == str
        self.minfo = kwargs
        if parse_cell and self.is_cell_source:
            self.get_cell_decomposition()

    def __init2__(self, **kwargs):
        # Reformat db info to cell format
        if "cell_source" in kwargs and type(cell_source := kwargs["cell_source"]) == dict:
            raw_code = [cell_source[e] for e in ["main_execution"] + CellParser.meta_modes if e in cell_source]
            kwargs["cell_source"] = "\n".join(raw_code)        
        self.is_cell_source = "cell_source" in kwargs and type(kwargs["cell_source"]) == str
        self.minfo = kwargs

        if "cell_id" not in self.minfo:
            if "cinfo" in kwargs:
                info = kwargs["cinfo"]
            else:
                info = LineParser.head_line_from_cell(kwargs["cell_source"])
            self.minfo = vars(info)
            self.minfo["cinfo"] = info
            self.minfo.update(kwargs)
        self.minfo.update({k: v for k, v in kwargs.items() if "grade" in k})

        if self.is_cell_source:
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

    def is_manual_note(self):
        return "note_src" in self.minfo and self.minfo["note_src"] in "manual"
        
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
        self.minfo[tmode] = LineParser.get_func_args(l, func_id=func_id)
        self.minfo[tmode]["visible"] = True
        if tmode == "evaluation":
            self.minfo[tmode]["emp_max_score"] = 0

    def block_equal_line(self, mode, l):
        indent = " " * (re.sub(r"^([\s]*)[\s]+.*$", r"\g<1>", l).count(" ") + 1)
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
            self.raw_exec_code = cell_source
        else:
            self.raw_exec_code = self.minfo["main_execution"]["code"]
            if "user" in self.minfo and self.minfo["user"] == "solution":
                self.minfo["main_execution"]["code"] = self.get_solution()

            self.minfo["answer"] = self.minfo["main_execution"]["code"]

    def get_solution(self):
        return cell_solution(self.raw_exec_code)
    
    def get_reset(self):
        return cell_reset(self.raw_exec_code)        