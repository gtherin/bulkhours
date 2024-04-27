import matplotlib
import datetime


class Grade:
    DEFAULT_GRADE = -9
    NO_ANSWER_FOUND = -10
    EVALUATION_CRASHED = -11
    ANSWER_FOUND = -12
    MAX_SCORE_NOT_AVAILABLE = -13
    EXERCISE_IS_AVAILABLE = -14
    EXERCISE_IS_HIDDEN = -15
    grad_names = ["grade_man", "grade_ana", "grade_bot"]

    def __init__(
        self, score=None, max_score=None, comment="", src=None, upd=None
    ) -> None:
        self.score, self.max_score = score, max_score
        self.src, self._upd, self.comment = src, upd, comment

    @property
    def upd(self):
        if self._upd is None:
            return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return self._upd

    @staticmethod
    def get_default_score(minfo):
        if "answer" in minfo:
            return Grade.ANSWER_FOUND
        elif (
            "atype" in minfo
            and minfo["atype"] == "code_project"
            and "update_time" in minfo
        ):
            return Grade.ANSWER_FOUND
        else:
            return Grade.NO_ANSWER_FOUND

    @staticmethod
    def create_from_info(minfo, level=None):
        # Get answers info
        info, minfo = {}, minfo.minfo if type(minfo) != dict else minfo

        # Get source
        if level is None:
            info["src"] = (src := Grade.get_default_source(minfo))
        else:
            info["src"] = (src := level)

        for k, v in {"upd": "_upd", "comment": "_comment", "score": ""}.items():
            if f"{src}{v}" in minfo:
                info[k] = minfo[f"{src}{v}"]

        info["score"] = (
            float(info["score"]) if "score" in info else Grade.get_default_score(minfo)
        )
        return Grade(**info)

    @staticmethod
    def check_gradname_validity(grade_name):
        if grade_name not in Grade.grad_names:
            raise Exception(
                f"Grade {grade_name} is not known grade type: {Grade.grad_names}"
            )

    @staticmethod
    def get_default_source(minfo):
        for g in Grade.grad_names:
            if g in minfo:
                return g
        return None

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
        elif int(v) in [Grade.NO_ANSWER_FOUND]:
            return "color:#FF3B52;background-color:#FF3B52;opacity: 40%"
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
