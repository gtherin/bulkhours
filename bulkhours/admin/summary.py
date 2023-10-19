import json
import IPython

from .. import core
from .exercice import Exercices, Exercice
from . import answers as aanswers
from . import tools


def summary(
    no_admin=False,
    reload_cache=True,
    cinfo="*.n",
    update_git=False,
    columns=None,
    cmap="RdBu",  # bwr_r RdBu
    export_notes=True,
    aliases = {},
    hide_grades = False,
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

    :return: a note between the minimal note and maximal note
    """

    cfg = core.tools.get_config(is_new_format=True, **kwargs)
    if not core.tools.is_admin(cfg=cfg):
        raise Exception("Only available for the admins🎓")

    if cfg.show_help:
        st = lambda x: f"\x1b[30m\x1b[1m{x}\x1b[m"
        print(st(summary.__doc__))

    exos = cfg.n["exercices"].split(";")

    if reload_cache:
        from .cache import cache_answers

        cache_answers(reload_cache if type(reload_cache) == list else exos, update_git=update_git, verbose=False, aliases=aliases)

    data = tools.get_users_list(no_admin=no_admin)

    IPython.display.display(IPython.display.Markdown(f"## {cfg.virtual_room}: {(1-data['is_admin']).sum()} students"))

    exercices = Exercices(users := list(data.mail.unique()), exos, cfg)

    for exo in exos:
        filename = aanswers.get_cfilename(cfg, exo)

        with open(filename) as json_file:
            answers = json.load(json_file)

            for user, adata in answers.items():
                exercices.update_data(user, exo, adata)

    if cinfo in ["", "A"]:
        for s in Exercice.fields:
            data = exercices.merge_dataframe(data, s, suffix="." + s[0])
    elif cinfo in ["*.c", "*.t", "*.n"]:
        data = exercices.merge_dataframe(data, [s for s in Exercice.fields if s[0] == cinfo[-1]][0])

    data = data.set_index("mail")
    data = data[["nom", "prenom", "all"] + exos] if columns is None else data[columns]

    for k, v in aliases.items():
        if v in data.index and k in data.index:
            for c in exos:
                data.at[k, c] = data.at[v, c]

    sdata = tools.styles(data, cmap=cmap, hide_grades=hide_grades) if cmap is not None else data

    if export_notes:
        IPython.display.display(sdata)
        return core.buttons.get_export_button(
            f"notes_{cfg.subject}_{cfg.virtual_room}_{cfg.notebook_id}.csv",
            data=data.to_csv(index=False),
            label="Export notes📝",
            tooltip="""⚠️Seulement disponible à l'évaluateur⚠️.
💾Envoi de la réponse (contenu de la cellule actuelle) comme solution officielle.""",
        )

    return sdata
