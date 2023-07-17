# Functions to compare student results to teacher results

import IPython
import difflib
import numpy as np
import pandas as pd
import os

from . import contexts


def is_equal(
    data_test, data_ref, norm="Linf-norm", error=1e-8, policy="strict", min_score=0, max_score=10, cmax_score=False
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
    :param min_score: the minimal note a student can get. defaults to 0.
    :param max_score: the maximal note a student can get. defaults to 10

    :param policy:
      - strict: policy is max_score if |distance| < error, 0 otherwise
      - gaussian: policy max_score * exp(-(distance/error)**2/2)

    :return: a note between the minimal note and maximal note

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
            1.0 - difflib.SequenceMatcher(None, data_test.replace("\n", ""), data_ref.replace("\n", "")).ratio()
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


def explain_student(student_data, teacher_data, raw=False):
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
    if "def student_explanation" in (explanation_code := teacher_data.get_code("explanation")):
        if "show_code=true" in explanation_code.replace(" ", "").lower():
            print(explanation_code)
        IPython.get_ipython().run_cell(explanation_code)


def evaluate_student(student_data, teacher_data, raw=False, use_student_context=True):
    """
    This function is used to evaluate the student code.

    
    :param debug: this is a first param
    :returns: this is a description of what is returned
    """
    # Get the formatted evaluation code
    evaluation_code = (
        teacher_data.get_code("evaluation")
        + """global eresult
eresult = student_evaluation_function()
import os
os.environ['FINAL_SCORE'] = str(eresult)
"""
    )

    do_debug = "debug=true" in evaluation_code.replace(" ", "").lower()

    # Run the teacher code if needed
    out1 = contexts.build_context(
        teacher_data, "main_execution", "teacher", f"teacher." in evaluation_code, do_debug=do_debug
    )

    # Run the student code if needed
    out2 = contexts.build_context(
        student_data,
        "main_execution",
        "student",
        f"student." in evaluation_code,
        do_debug=do_debug,
        use_context=use_student_context,
    )
    if not use_student_context:
        evaluation_code = evaluation_code.replace("student.", "")

    if "show_code=true" in teacher_data.get_code("evaluation").replace(" ", "").lower():
        print(evaluation_code)

    contexts.run_cell(evaluation_code, do_debug)

    score = float(os.environ["FINAL_SCORE"])

    if raw:
        return score

    contexts.run_cell(evaluation_code.replace("student.", "teacher."), stdout=False)
    max_score = float(os.environ["FINAL_SCORE"])

    return f"{score}/{max_score}"
