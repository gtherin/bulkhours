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


def gpt_evaluation(student_data, teacher_data, max_score=10):
    from . import gpt

    if gpt.evaluation_instructions is not None:
        print("")
        return gpt.get_grade(student_data, teacher_data, max_score)

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
        data_test, data_ref = data_test[data_test != None], data_ref[data_ref != None]

    if type(data_test) == str:
        estimation_error = np.abs(
            1.0
            - difflib.SequenceMatcher(
                None, data_test.replace("\n", ""), data_ref.replace("\n", "")
            ).ratio()
        )
    else:
        if hasattr(data_test, "shape") and data_test.shape != data_ref.shape:
            return min_score

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

    :param show_max_score_code=False
    :param show_student_code=False
    :param show_teacher_code=False
    :param show_evaluation_code=False
    :param run=False
    :param execute=True
    :param catch_error=True

    :returns: this is a description of what is returned
    """

    # Return default grade if Nothing available
    if student_data.get_code("main_execution") == "":
        return Grade(comment="No answer available")

    # Get the formatted codes
    student_code, teacher_code, evaluation_code = contexts.get_contexts_codes(
        student_data, teacher_data, execute
    )

    if "help=true" in evaluation_code.replace(" ", "").lower():
        print(student_evaluation_function.__doc__)

    # Hide plot by default
    if not (do_plot := "do_plot=true" in evaluation_code.replace(" ", "").lower()):
        plt.ioff()

    # 1. Teacher
    if "show_teacher_code=true" in evaluation_code.replace(" ", "").lower():
        print("############# teacher_code ##################")
        print(teacher_code)

    # 2. Teacher
    if execute:
        IPython.get_ipython().run_cell(teacher_code)

    # 3. Teacher
    if "show_teacher_dir=true" in evaluation_code.replace(" ", "").lower():
        print("############# teacher_dir ##################")
        IPython.get_ipython().run_cell("[t for t in dir(teacher) if t[0] != '_']")

    # 1. Student
    if "show_student_code=true" in evaluation_code.replace(" ", "").lower():
        print("############# student_code ##################")
        print(student_code)

    # 2. Student
    if execute:
        IPython.get_ipython().run_cell(student_code)

    # 3. Student
    if "show_student_dir=true" in evaluation_code.replace(" ", "").lower():
        print("############# student_dir ##################")
        IPython.get_ipython().run_cell("[s for s in dir(student) if s[0] != '_']")

    # Run the teacher code and get max_score from it
    max_score = get_max_score(evaluation_code, execute=execute)

    if "admin.gpt_eval" in evaluation_code:
        res = gpt_evaluation(student_data, teacher_data, max_score=max_score)
        #if normalize_score:
        #    res.score *= max_score

        return res

    # Run the student code if needed
    if not use_student_context:
        evaluation_code = evaluation_code.replace("student.", "")

    if "show_evaluation_code=true" in evaluation_code.replace(" ", "").lower():
        print("############# evaluation_code ##################")
        print(evaluation_code)

    if "debug=true" in evaluation_code.replace(" ", "").lower():
        contexts.run_cell(evaluation_code, True)
        grade = Grade(
            score=float(os.environ["FINAL_SCORE"]),
            comment="""Analytical evaluation failed.
Somme more comments should ba available soon.                           
""",
        )
    else:
        try:
            contexts.run_cell(evaluation_code, False)
            grade = Grade(
                score=float(os.environ["FINAL_SCORE"]),
                comment="""Analytical evaluation failed.
Somme more comments should ba available soon.                           
""",
            )
        except:
            grade = Grade(score=Grade.EVALUATION_CRASHED, comment="No answer available")

    if not do_plot:
        plt.ion()

    return grade
