import numpy as np
import pandas as pd

from . import tools


class Exercice:
    fields = ["count", "time", "note"]

    def __init__(self, user, exo) -> None:
        self.user, self.exo, self.answer = user, exo, ""
        self.utime, self.note, self.count = np.nan, np.nan, np.nan

    def update_data(self, adata) -> None:
        self.utime, self.note, self.count = adata["update_time"], adata["note"], 1
        if self.note is None:  # Failure of automatic grades
            self.note = -2
        else:
            self.note = float(self.note)


class Exercices:
    def __init__(self, users, exos, course_info, config) -> None:
        self.users, self.exos = list(users), exos
        self.course_info = course_info
        self.config = config
        self.exercices = {u: {e: Exercice(u, e) for e in exos} for u in users}

    def update_data(self, user, exo, adata) -> None:
        if user not in self.exercices:
            self.exercices[user] = {e: Exercice(user, e) for e in self.exos}
        self.exercices[user][exo].update_data(adata)

    def get_dataframe(self, field, suffix=""):
        data = pd.DataFrame(
            {e + suffix: [getattr(self.exercices[u][e], field) for u in self.users] for e in self.exos},
            index=self.users,
        )

        if field == "time":
            for c in data.columns:
                ts = pd.to_datetime(data[c])
                data[c] = ((ts - ts.min()).dt.seconds / 60.0).round()

        if field == "count":
            data["all.c"] = data[[e + ".c" for e in self.exos]].count(axis=1)
        if field == "note":
            ceval = self.course_info["evaluation"]

            data["all"] = np.round(data.fillna(0.0).clip(0).sum(axis=1), 1)
            if "norm20" in self.config["global"] and self.config["global"]["norm20"]:
                data["all"] = data["all"] * 20 / data["all"].max()

            if 0:
                try:
                    data["all"] = (
                        np.round(data.fillna(0.0).clip(0).mean(axis=1), 1)
                        if ceval == ""
                        else data.fillna(0.0).clip(0).rename(columns=lambda value: value.replace(".", "_")).eval(ceval)
                    )
                except:
                    print(
                        f"\x1b[41mEvaluation function '{ceval}' can not be interpreted. Please change it in the dashboard:\nbulkhours.admin.dashboard()\x1b[0m"
                    )

                    data["all"] = np.nan

        return data

    def merge_dataframe(self, data, field, suffix=""):
        return data.merge(self.get_dataframe(field, suffix=suffix), how="left", left_on="mail", right_index=True)
