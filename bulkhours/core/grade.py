import matplotlib
import datetime


class Grade:
    DEFAULT_GRADE = -9
    NO_ANSWER_FOUND = -10
    EVALUATION_CRASHED = -11
    ANSWER_FOUND = -12
    MAX_SCORE_NOT_AVAILABLE = -13
    grad_names = ["grade_man", "grade_ana", "grade_bot"]

    @staticmethod
    def check_gradname_validity(grade_name):
        if grade_name not in Grade.grad_names:
            raise Exception(
                f"Grade {grade_name} is not known grade type: {Grade.grad_names}"
            )

    @staticmethod
    def src(answer):
        if type(answer) != dict:
            answer = answer.minfo
        for g in Grade.grad_names:
            if g in answer:
                return g
        return None

    @staticmethod
    def get(answer, level=None):
        if type(answer) != dict:
            answer = answer.minfo

        src = Grade.src(answer)
        if src is None or (level is not None and level not in answer):
            if "answer" in answer:
                return Grade.ANSWER_FOUND
            if (
                "atype" in answer
                and answer["atype"] == "code_project"
                and "update_time" in answer
            ):
                return Grade.ANSWER_FOUND

            return Grade.NO_ANSWER_FOUND
        return float(answer[src])

    @staticmethod
    def upd(answer):
        if type(answer) != dict:
            answer = answer.minfo

        src = Grade.src(answer)
        if src is None:
            return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return answer[src + "_upd"]

    @staticmethod
    def set_static_style_info(minvalue=0.0, cmap="RdBu"):
        Grade.mincolor = matplotlib.colors.rgb2hex(
            matplotlib.cm.get_cmap(cmap)(minvalue)
        )

    @staticmethod
    def apply_all_style(v):
        if v != v or v == 0:  # Failure of automatic corrections
            return f"color:#FF3B52;background-color:#FF3B52;opacity: 40%"
        else:
            return None

    @staticmethod
    def apply_style(v, is_corrected):
        opacity = "40" if is_corrected else "60"
        if type(v) == str:
            return None
        elif v != v:  # Failure of automatic corrections
            return (
                f"color:{Grade.mincolor};background-color:{Grade.mincolor};opacity: 70%"
            )
        elif int(v) in [
            Grade.DEFAULT_GRADE,
            Grade.EVALUATION_CRASHED,
            Grade.ANSWER_FOUND,
        ]:
            return f"color:#FF3B52;background-color:#FF3B52;opacity: {opacity}%"
        else:
            return None

    @staticmethod
    def is_valid(grade):
        return grade >= 0
