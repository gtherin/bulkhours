import IPython
import difflib
from . import contexts
import numpy as np


def is_equal(data_test, data_ref, norm="Linf-norm", error=1e-8, policy="strict", min_score=0, max_score=10):
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

    if type(data_test) != type(data_ref):
        print(f"\nFINAL_SCORE={min_score}/{max_score}\n")
        return min_score

    # Get error from student
    if type(data_test) == list:
        data_test = np.array(data_test)
        data_ref = np.array(data_ref)

    if type(data_test) == str:
        estimation_error = np.abs(
            1.0 - difflib.SequenceMatcher(None, data_test.replace("\n", ""), data_ref.replace("\n", "")).ratio()
        )
    else:
        estimation_error = np.abs(data_test - data_ref)

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
    print(f"\nFINAL_SCORE={final_score}/{max_score}\n")
    return final_score


def explain_student(student_data, teacher_data, raw=False):
    """
    Execute the evaluation code
    My numpydoc description of a kind
    of very exhautive numpydoc format docstring.

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


def aggregate_notes(teacher_data, evaluation_code, scores):
    """
    This is an example of Google style.

    Args:
        scores: This is the first param.

    Returns:
        This is a description of what is returned.
    """
    agg_evaluation_code, counter = "", 0
    for l in evaluation_code.splitlines():
        if ".is_equal" in l:
            l = l[: l.rfind("bulkhours.is_equal")] + scores[counter][: scores[counter].find("/")]
            counter += 1
        agg_evaluation_code += l + "\n"

    agg_evaluation_code = agg_evaluation_code.replace("student_evaluation_function", "do_evaluate_student")
    agg_evaluation_code += "print(f'FINAL_SCORE={r}/%s')\n" % teacher_data.max_score

    if "show_code=true" in teacher_data.get_code("evaluation").replace(" ", "").lower():
        print(agg_evaluation_code)
    out = contexts.exec_code(agg_evaluation_code, False)
    return [a.replace("FINAL_SCORE=", "") for a in out if "FINAL_SCORE=" in a][0].replace(")", "")


def evaluate_student(student_data, teacher_data, raw=False, use_student_context=True):
    """
    This is a reST style.

    :param debug: this is a first param
    :returns: this is a description of what is returned
    """
    # Get the formatted evaluation code
    evaluation_code = teacher_data.get_code("evaluation") + "\nr = student_evaluation_function()\n"

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

    out = contexts.exec_code(evaluation_code, do_debug)
    scores = [a.replace("FINAL_SCORE=", "") for a in out if "FINAL_SCORE=" in a]
    if do_debug:
        print("SCORES:", scores)

    score = aggregate_notes(teacher_data, evaluation_code, scores)
    if do_debug:
        print("SCORE:", score)

    if raw:
        return float(score[: score.find("/")])

    return score
