import numpy as np
import pandas as pd


class Exercice:
    fields = ["count", "time", "grade"]

    def __init__(self, user, exo) -> None:
        from .. import core

        self.user, self.exo, self.answer = user, exo, ""
        self.grade = core.Grade(score=core.Grade.DEFAULT_GRADE)

    def update_data(self, adata) -> None:
        from .. import core

        self.count = 1
        self.grade = core.Grade.create_from_info(adata)

    def get(self, field):
        if field not in Exercice.fields:
            raise Exception(f"{field} is not known")
        if field in ["score", "grade"]:
            return self.grade.score
        if field in ["count"]:
            return self.count
        if field in ["time"]:
            return self.grade.upd

        return getattr(self, field)


class Exercices:
    def __init__(self, users, exos, cfg, aliases={}) -> None:
        self.users, self.exos = list(users), exos
        self.cfg = cfg
        self.aliases = aliases if aliases is not None else {}
        self.exercices = {u: {e: Exercice(u, e) for e in exos} for u in users}

    def update_data(self, user, exo, adata) -> None:
        for k, v in self.aliases.items():
            if v == user:
                self.update_data(k, exo, adata)
        if user not in self.exercices:
            self.exercices[user] = {e: Exercice(user, e) for e in self.exos}
        self.exercices[user][exo].update_data(adata)

    def get_dataframe(self, field, suffix=""):
        data = pd.DataFrame(
            {
                e + suffix: [self.exercices[u][e].get(field) for u in self.users]
                for e in self.exos
            },
            index=self.users,
        )

        if field == "time":
            for c in data.columns:
                ts = pd.to_datetime(data[c])
                data[c] = ((ts - ts.min()).dt.seconds / 60.0).round()

        if field == "count":
            data["all.c"] = data[[e + ".c" for e in self.exos]].count(axis=1)
        if field in ["grade", "score"]:
            ceval = self.cfg.n["evaluation"]

            data["all"] = np.round(data.fillna(0.0).clip(0).sum(axis=1), 1)
            if "norm20" in self.cfg["global"] and self.cfg["global"]["norm20"]:
                data["all"] = data["all"] * 20 / data["all"].max()

            if 0:
                try:
                    data["all"] = (
                        np.round(data.fillna(0.0).clip(0).mean(axis=1), 1)
                        if ceval == ""
                        else data.fillna(0.0)
                        .clip(0)
                        .rename(columns=lambda value: value.replace(".", "_"))
                        .eval(ceval)
                    )
                except:
                    print(
                        f"\x1b[41mEvaluation function '{ceval}' can not be interpreted. Please change it in the dashboard:\nbulkhours.admin.dashboard()\x1b[0m"
                    )

                    data["all"] = np.nan

        return data

    def merge_dataframe(self, data, field, suffix=""):
        return data.merge(
            self.get_dataframe(field, suffix=suffix),
            how="left",
            left_on="mail",
            right_index=True,
        )
