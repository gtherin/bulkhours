import json
import IPython
import pandas as pd

from .. import core
from .exercice import Exercices, Exercice
from . import answers as aanswers
from . import tools


def get_num_answers(cfg):
    anscs = {}
    for e in cfg.n["exercices"].split(";"):
        anss = aanswers.get_answers(e)
        for k, _ in anss.items():
            if k not in anscs:
                anscs[k] = 0
            anscs[k] += 1
    return anscs


def get_groups(aliases={}, virtual_rooms=[None]):
    cfg = core.tools.get_config(is_new_format=True)

    for v in virtual_rooms:
        if v is not None:
            tools.switch_classroom(v)

        anscs = get_num_answers(cfg)

        data = tools.get_users_list()
        naliases = {}
        groups = aanswers.get_answers("mygroup")
        for k, v in groups.items():
            members = [p for p in v["answer"].split('"') if "@" in p]
            rm, an = k, 1
            for p in members:
                if p in aliases:
                    p = aliases[p]

                if p not in data.mail.unique() and ".doe@" not in p:
                    aanswers.user_is_unknown(cfg, p, "group")
                if p in anscs and anscs[p] > an:
                    rm = p
                    an = anscs[p]
            for p in members:
                if p in aliases:
                    p = aliases[p]
                if ".doe@" not in p and rm != p:
                    naliases[p] = rm

    aliases = {}
    for k, v in naliases.items():
        if k not in aliases.values():
            aliases[k] = v

    return dict(sorted(aliases.items(), key=lambda x: x[1]))


def summary(
    no_admin=False,
    reload_cache=True,
    cinfo="*.g",
    update_git=False,
    columns=None,
    cmap="RdBu",  # bwr_r RdBu
    export_notes=True,
    aliases={},
    hide_grades=False,
    aggregate=None,
    apply=None,
    sorted_by=True,
    **kwargs,
):
    """Permet de faire un point sur

    Parameters:
    :param no_admin: Do not show the admin in the summary
    :param reload_cache: input data to do the test
    :param cinfo: by default, display the notes
    :param columns: Only show selecetd columns
    :param cmap: Colormap to use the notes
    :param update_git: update data on the cloud

    :return: a grade between the minimal grade and maximal grade
    """

    cfg = core.tools.get_config(is_new_format=True, **kwargs)
    if not core.tools.is_admin(cfg=cfg):
        raise Exception("Only available for the admins🎓")

    if cfg.show_help:
        st = lambda x: f"\x1b[30m\x1b[1m{x}\x1b[m"
        print(st(summary.__doc__))

    exos = cfg.n["exercices"].split(";")

    # Get aliases from db if not filled
    if aliases != {}:
        core.firebase.get_document(question="info", user="aliases", cinfo=cfg).set(
            aliases
        )
    else:
        aliases = (
            core.firebase.get_document(question="info", user="aliases", cinfo=cfg)
            .get()
            .to_dict()
        )
    if aliases is None:
        aliases = {}

    if reload_cache:
        from .cache import cache_answers

        cache_answers(
            reload_cache if type(reload_cache) == list else exos,
            update_git=update_git,
            verbose=False,
            aliases=aliases,
        )

    data = tools.get_users_list(no_admin=no_admin)

    IPython.display.display(
        IPython.display.Markdown(
            f"## {cfg.virtual_room}: {(1-data['is_admin']).sum()} students"
        )
    )

    if aggregate is not None:
        grades = pd.DataFrame(
            {
                n: core.firebase.get_document(
                    question_id=f"{cfg.subject}_{cfg.virtual_room}_{n}_info",
                    user="grades",
                )
                .get()
                .to_dict()
                for n in aggregate
            }
        )
        data = data.merge(grades, how="left", left_on="mail", right_index=True)
        data["all"] = data[aggregate].mean(axis=1)
        data = data.set_index("mail")
        exos, columns = aggregate, None

    else:
        exercices = Exercices(
            users := list(data.mail.unique()), exos, cfg, aliases=aliases
        )

        for exo in exos:
            filename = aanswers.get_cfilename(cfg, exo)

            with open(filename) as json_file:
                answers = json.load(json_file)

                for user, adata in answers.items():
                    exercices.update_data(user, exo, adata)

        if cinfo in ["", "A"]:
            for s in Exercice.fields:
                data = exercices.merge_dataframe(data, s, suffix="." + s[0])
        elif cinfo in ["*.c", "*.t", "*.g"]:
            data = exercices.merge_dataframe(
                data, [s for s in Exercice.fields if s[0] == cinfo[-1]][0]
            )

        data = data.set_index("mail")
        data["all"] = data["all"].round(1)
        core.firebase.get_document(question="info", user="grades", cinfo=cfg).set(
            data["all"].to_dict()
        )

    data = data[["nom", "prenom", "all"] + exos] if columns is None else data[columns]
    if apply is not None:
        data = apply(data, exos)

    for k, v in aliases.items():
        if v in data.index and k in data.index:
            for c in exos:
                data.at[k, c] = data.at[v, c]

    sdata = (
        tools.styles(data, cmap=cmap, hide_grades=hide_grades, sorted_by=sorted_by)
        if cmap is not None
        else data
    )

    if export_notes:
        IPython.display.display(sdata)
        return core.buttons.get_export_button(
            f"notes_{cfg.subject}_{cfg.virtual_room}_{cfg.notebook_id}.csv",
            data=data.to_csv(index=False),
            label="Export notes📝",
            tooltip="""⚠️Seulement disponible pour l'évaluateur⚠️.
💾Envoi de la réponse (contenu de la cellule actuelle) comme solution officielle.""",
        )

    return sdata
