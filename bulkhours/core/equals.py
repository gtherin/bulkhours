# Functions to compare student results to teacher results

import IPython
import difflib
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

from . import contexts
from .grade import Grade
from .line_parser import LineParser


def gpt_evaluation(student_data, teacher_data):
    from . import gpt

    if gpt.evaluation_instructions is not None:
        print("")
        grade, _ = gpt.get_grade(student_data, teacher_data)
        return grade

    print("🚧Need to implement evaluation_instructions")
    return np.nan


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

    # Get error from student
    if type(data_test) in [list, tuple]:
        data_test = np.array(data_test)
        data_ref = np.array(data_ref)

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


def get_evaluation_code(teacher_data):
    evaluation_code = teacher_data.get_code("evaluation")
    if "def student_evaluation_function" not in evaluation_code:
        evaluation_code += """\ndef student_evaluation_function():\n    return bulkhours.admin.gpt_eval("syntax", max_score=10)"""

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


def get_max_score(teacher_data, execute=True):
    # Get the formatted evaluation code
    evaluation_code = get_evaluation_code(teacher_data)

    print(evaluation_code)
    return
    # Include gpt instructions
    nevaluation_code = ""
    for e in evaluation_code.split("\n"):
        if "admin.gpt_eval" in e:
            l = LineParser.get_func_args(e, func_id="bulkhours.admin.gpt_eval")
            nevaluation_code += (
                e.replace("bulkhours.admin.gpt_eval", l["max_score"] + "  #") + "\n"
            )
        else:
            nevaluation_code += e + "\n"

    evaluation_code = nevaluation_code
    do_debug = "debug=true" in evaluation_code.replace(" ", "").lower()

    # Run the teacher code if needed
    if execute:
        contexts.build_context(
            teacher_data,
            "main_execution",
            "teacher",
            evaluation_code,
            f"teacher." in evaluation_code,
            do_debug=do_debug,
        )

    try:
        evaluation_code = evaluation_code.replace("bulkhours.admin.replace(", "#")
        contexts.run_cell(evaluation_code.replace("student.", "teacher."), stdout=False)
        return float(os.environ["FINAL_SCORE"])
    except:
        return Grade.MAX_SCORE_NOT_AVAILABLE


def evaluate_student(
    student_data,
    teacher_data,
    raw=False,
    use_student_context=True,
    user="",
    verbose=False,
    execute=True,
    normalize_score=True,
):
    """
    This function is used to evaluate the student code.

    :param debug: this is a first param
    :returns: this is a description of what is returned
    """

    student_code = student_data.get_code("main_execution")

    if student_code == "":
        return Grade.NO_ANSWER_FOUND

    # Get the formatted evaluation code
    evaluation_code = get_evaluation_code(teacher_data)
    do_debug = "debug=true" in evaluation_code.replace(" ", "").lower()
    do_plot = "do_plot=true" in evaluation_code.replace(" ", "").lower()

    # Hide plot by default
    if not do_plot:
        plt.ioff()

    # Run the teacher code and get max_score from it
    max_score = get_max_score(teacher_data, execute=execute)

    if "admin.gpt_eval" in evaluation_code:
        score = gpt_evaluation(student_data, teacher_data)
        if normalize_score:
            score *= max_score

        if raw:
            return score

        return f"{score}/{max_score}"

    # Run the student code if needed
    if execute:
        contexts.build_context(
            student_data,
            "main_execution",
            "student",
            evaluation_code,
            f"student." in evaluation_code,
            do_debug=do_debug,
            use_context=use_student_context,
            user=user,
        )
    if not use_student_context:
        evaluation_code = evaluation_code.replace("student.", "")

    evaluation_code = evaluation_code.replace("bulkhours.admin.replace(", "#")
    if "show_code=true" in teacher_data.get_code("evaluation").replace(" ", "").lower():
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

    if raw:
        return score

    return f"{score}/{max_score}"
