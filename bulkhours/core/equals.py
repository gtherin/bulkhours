# Functions to compare student results to teacher results

import IPython
import difflib
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

from . import contexts
from .grade import Grade
from . import tools
from .line_parser import LineParser
from .cell_parser import CellParser


def gpt_evaluation(student_data, teacher_data):
    from . import gpt

    if gpt.evaluation_instructions is not None:
        print("")
        return gpt.get_grade(student_data, teacher_data)

    print("🚧Need to implement evaluation_instructions")
    return Grade()


def is_equal(
    data_test,
    data_ref,
    norm="Linf-norm",
    error=1e-8,
    policy="strict",
    min_score=0,
    max_score=10,
    cmax_score=False,
):
    """Return the student score compared to a benchmark value

    Parameters:
    :param data_test: data to be checked
    :param data_ref: by default teacher.data

    :param norm: element wise comparison by default:
       - Linf-norm: distance = max(|data_test-data_ref|)
       - L1-norm: distance = |data_test-data_ref|_1
       - L2-norm:= distance = ||data_test-data_ref||_2

    :param error: tolerance on the results comparison
    :param min_score: the minimal grade a student can get. defaults to 0.
    :param max_score: the maximal grade a student can get. defaults to 10

    :param policy:
      - strict: policy is max_score if |distance| < error, 0 otherwise
      - gaussian: policy max_score * exp(-(distance/error)**2/2)

    :return: a grade between the minimal grade and maximal grade

    examples
    return bulkhours.is_equal(data_test)
    return bulkhours.is_equal(my_func(data), teacher.my_func(data), error=1e-8)
    return bulkhours.is_equal(data_test, data_ref=0.9525741268)
    return bulkhours.is_equal(data_test, data_ref=np.array([1, 2, 3]), max_score=5, policy="strict", error=1e-8)
    return bulkhours.is_equal(data_test, data_ref=3, max_score=5, policy="gaussian", error=1e-8)
    """

    if cmax_score:
        return max_score

    if type(data_test) != type(data_ref):
        return min_score

    # Get data type
    for func in ["numpy", "as_list"]:
        if "tensorflow" in str(type(data_test)) and hasattr(data_test, func):
            data_test, data_ref = getattr(data_test, func)(), getattr(data_ref, func)()

    # Get error from student
    if type(data_test) in [list, tuple]:
        data_test, data_ref = np.array(data_test), np.array(data_ref)

    if type(data_test) == str:
        estimation_error = np.abs(
            1.0
            - difflib.SequenceMatcher(
                None, data_test.replace("\n", ""), data_ref.replace("\n", "")
            ).ratio()
        )
    else:
        estimation_error = np.abs(data_test - data_ref)

    if type(estimation_error) == pd.DataFrame:
        estimation_error = estimation_error.values

    if norm in ["L1-norm", "L1norm"]:
        distance = np.sum(estimation_error)
    elif norm in ["L2-norm", "L2norm"]:
        distance = np.linalg.norm(estimation_error)
    else:  # Linf-norm
        distance = np.max(estimation_error)

    if policy in ["gaussian", "normal"]:
        score = np.exp(-((distance / error) ** 2) / 2)
    else:  # strict
        score = np.clip(float(distance < error), 0, 1)

    final_score = np.round(score * (max_score - min_score) + min_score, 1)
    return final_score


def execute_teacher_code(student_data, teacher_data, raw=False, tmode="explanation"):
    """Function to explain the answer to the student

    Parameters
    ----------
    first : array_like
        the 1st param name `first`
    second : {'value', 'other'}, optional
        the 3rd param, by default 'value'

    Returns
    -------
    string
        a value in a string
    """
    if f"def student_{tmode}_function" in (tcode := teacher_data.get_code(tmode)):
        if "show_code=true" in tcode.replace(" ", "").lower():
            print(tcode)

        IPython.get_ipython().run_cell(tcode)
        IPython.get_ipython().run_cell(f"student_{tmode}_function()")


def get_evaluation_code(evaluation_code, enrich=True):
    if type(evaluation_code) != str:
        evaluation_code = evaluation_code.get_code("evaluation")
    if "def student_evaluation_function" not in evaluation_code:
        evaluation_code += """\ndef student_evaluation_function():\n    return bulkhours.admin.gpt_eval("syntax", max_score=10)"""
    if not enrich:
        return evaluation_code

    return (
        f""" 
import os
os.environ['FINAL_SCORE'] = "0"
%s
global eresult
eresult = student_evaluation_function()
os.environ['FINAL_SCORE'] = str(eresult)
"""
        % evaluation_code
    )


def get_max_score(revaluation_code, execute=True):
    def comment_function_call(func_id):
        l = LineParser.get_func_args(e, func_id=func_id)
        max_score = l["max_score"] if "max_score" in l else "10"
        return e.replace(func_id, max_score + "  #") + "\n"

    evaluation_code = ""
    for e in revaluation_code.split("\n"):
        if "bulkhours.admin.gpt_eval" in e:
            evaluation_code += comment_function_call("bulkhours.admin.gpt_eval")
        elif "bulkhours.is_equal" in e:
            evaluation_code += comment_function_call("bulkhours.is_equal")
        else:
            evaluation_code += e + "\n"

    if "show_max_score_code=true" in evaluation_code.replace(" ", "").lower():
        print(evaluation_code)

    try:
        contexts.run_cell(evaluation_code.replace("student.", "teacher."), stdout=False)
        return float(os.environ["FINAL_SCORE"])
    except:
        return Grade.MAX_SCORE_NOT_AVAILABLE


def get_contexts_codes(student_data, teacher_data):
    """
    This function is used to evaluate the student code.

    :param debug: this is a first param
    :returns: this is a description of what is returned
    """

    student_code = student_data.get_code("main_execution")

    if student_code == "":
        return Grade.NO_ANSWER_FOUND

    # Get the formatted evaluation code
    evaluation_code = get_evaluation_code(teacher_data, enrich=False)

    black = tools.install_if_needed("black")

    evaluation_code = black.format_str(
        evaluation_code, mode=black.Mode(line_length=500)
    )

    student_code = CellParser.remove_meta_functions_execution(
        student_data.get_code("main_execution")
    )
    teacher_code = CellParser.remove_meta_functions_execution(
        teacher_data.get_code("main_execution")
    )

    if "recreate_contexts" in evaluation_code:
        icode, ecode, ecodes = [], [], evaluation_code.split("\n")
        for e in ecodes[1:]:
            if "recreate_contexts" in e:
                ecode.append(ecodes[0])
                rc = LineParser.get_func_args(e, "bulkhours.recreate_contexts")
                if "replace" in rc:
                    print(rc)
                    rc["replace"] = eval(
                        black.format_str(rc["replace"], mode=black.Mode())
                    )
            elif len(ecode) > 0:
                ecode.append(e)
            else:
                icode.append(e[4:])

        student_code = "\n".join(icode) + "\n" + student_code
        teacher_code = "\n".join(icode) + "\n" + teacher_code
        if "replace" in rc:
            for r in rc["replace"]:
                student_code = student_code.replace(r[0], r[1])
                teacher_code = teacher_code.replace(r[0], r[1])

        evaluation_code = get_evaluation_code("\n".join(ecode), enrich=True)
    else:
        evaluation_code = get_evaluation_code(evaluation_code, enrich=True)

    student_code = contexts.generate_context_code(
        student_code, evaluation_code, "student"
    )
    teacher_code = contexts.generate_context_code(
        teacher_code, evaluation_code, "teacher"
    )

    return student_code, teacher_code, evaluation_code


def student_evaluation_function(
    student_data,
    teacher_data,
    use_student_context=True,
    user="",
    verbose=False,
    execute=True,
    normalize_score=True,
):
    """
    This function is used to evaluate the student code.

    show_max_score_code=False
    show_student_code=False
    show_teacher_code=False
    show_evaluation_code=False
    run=False
    execute=True

    :param debug: this is a first param
    :returns: this is a description of what is returned
    """

    # Return default grade if Nothing available
    if student_data.get_code("main_execution") == "":
        return Grade.NO_ANSWER_FOUND

    # Get the formatted codes
    student_code, teacher_code, evaluation_code = get_contexts_codes(
        student_data, teacher_data
    )

    if "help=true" in evaluation_code.replace(" ", "").lower():
        print(__doc__)

    do_debug = "debug=true" in evaluation_code.replace(" ", "").lower()
    do_plot = "do_plot=true" in evaluation_code.replace(" ", "").lower()

    if "show_teacher_code=true" in evaluation_code.replace(" ", "").lower():
        print("############# teacher_code ##################")
        print(teacher_code)

    if "show_student_code=true" in evaluation_code.replace(" ", "").lower():
        print("############# student_code ##################")
        print(student_code)

    # Hide plot by default
    if not do_plot:
        plt.ioff()

    if execute:
        IPython.get_ipython().run_cell(teacher_code)

    if execute:
        IPython.get_ipython().run_cell(student_code)

    # Run the teacher code and get max_score from it
    max_score = get_max_score(evaluation_code, execute=execute)

    if do_debug:
        IPython.get_ipython().run_cell("dir(student)")

    if "admin.gpt_eval" in evaluation_code:
        res = gpt_evaluation(student_data, teacher_data)
        if normalize_score:
            res.score *= max_score

        return res

    # Run the student code if needed
    if not use_student_context:
        evaluation_code = evaluation_code.replace("student.", "")

    if "show_evaluation_code=true" in evaluation_code.replace(" ", "").lower():
        print("############# evaluation_code ##################")
        print(evaluation_code)

    if do_debug:
        contexts.run_cell(evaluation_code, do_debug)
        score = float(os.environ["FINAL_SCORE"])
    else:
        try:
            contexts.run_cell(evaluation_code, do_debug)
            score = float(os.environ["FINAL_SCORE"])
        except:
            score = Grade.EVALUATION_CRASHED

    if not do_plot:
        plt.ion()

    return Grade(
        score=score,
        max_score=max_score,
        comment="""Analytical evaluation failed.
Somme more comments should ba available soon.                           
""",
    )
