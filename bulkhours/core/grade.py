import matplotlib

class Grade:

    DEFAULT_GRADE = -9
    NO_ANSWER_FOUND = -10
    EVALUATION_CRASHED = -11
    ANSWER_FOUND = -12
    MAX_SCORE_NOT_AVAILABLE = -13
    grad_names = ["grade_man", "grade_eva", "grade_bot", "note"]

    @staticmethod
    def check_gradname_validity(grade_name):
        if grade_name not in Grade.grad_names:
            raise Exception(f"Grade {grade_name} is not known grade type: {Grade.grad_names}")

    @staticmethod
    def src(answer):
        for g in Grade.grad_names:
            if g in answer:
                return g
        return None

    @staticmethod
    def get(answer):
        src = Grade.src(answer)
        if src is None:
            return Grade.DEFAULT_GRADE
        return answer[src]

    @staticmethod
    def set_static_style_info(minvalue=0.0, cmap="RdBu"):
        Grade.mincolor = matplotlib.colors.rgb2hex(matplotlib.cm.get_cmap(cmap)(minvalue))

    @staticmethod
    def apply_style(v, is_corrected):
        opacity = "40" if is_corrected else "60"
        if type(v) == str:
            return None
        elif v in [Grade.DEFAULT_GRADE, Grade.EVALUATION_CRASHED, Grade.ANSWER_FOUND]:
            return f"color:#FF3B52;background-color:#FF3B52;opacity: {opacity}%"
        elif v != v:  # Failure of automatic corrections
            return f"color:{Grade.mincolor};background-color:{Grade.mincolor};opacity: 70%"
        else:
            return None

    @staticmethod
    def is_valid(note):
        return note >= 0
