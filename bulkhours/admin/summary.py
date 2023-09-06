import json
from .. import core
from .exercice import Exercices, Exercice
from . import tools


def summary(
    no_admin=False,
    reload_cache=True,
    cinfo="*.n",
    update_git=False,
    columns=None,
    cmap="RdBu",  # bwr_r RdBu
    export_notes=True,
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

    config = core.tools.get_config(**kwargs)

    if "help" in config and config["help"]:
        st = lambda x: f"\x1b[30m\x1b[1m{x}\x1b[m"
        print(st(summary.__doc__))

    virtual_room, subject, notebook_id = (config.get(v) for v in ["virtual_room", "subject", "notebook_id"])
    language = config["global"].get("language")
    course_info = config[notebook_id]
    exos = course_info["exercices"].split(";")

    if reload_cache:
        from .cache import cache_answers

        cache_answers(reload_cache if type(reload_cache) == list else exos, update_git=update_git, verbose=False)

    data = tools.get_users_list(no_admin=no_admin)
    exercices = Exercices(users := list(data.mail.unique()), exos, course_info, config)

    for exo in exos:
        filename = core.tools.abspath(
            f"data/cache/{subject}/{virtual_room}/admin_{notebook_id}_{exo}.json", create_dir=True
        )

        with open(filename) as json_file:
            answers = json.load(json_file)

            for user, adata in answers.items():
                if user not in users:
                    print(
                        f"\x1b[41mL'étudiant {user} est inconnu. Ajouter le depuis le menu dashboard:\nbulkhours.admin.dashboard()\x1b[0m"
                        if language == "fr"
                        else f"\x1b[41mStudent {user} is unknown. Please declare it in the dashboard: bulkhours.admin.dashboard()\x1b[0m"
                    )
                exercices.update_data(user, exo, adata)

    if cinfo in ["", "A"]:
        for s in Exercice.fields:
            data = exercices.merge_dataframe(data, s, suffix="." + s[0])
    elif cinfo in ["*.c", "*.t", "*.n"]:
        data = exercices.merge_dataframe(data, [s for s in Exercice.fields if s[0] == cinfo[-1]][0])

    data = data.set_index("mail")
    data = data[["nom", "prenom", "all"] + exos] if columns is None else data[columns]

    if export_notes:
        import base64
        import IPython

        res = data.to_csv(index=False)

        filename = f"notes_{subject}_{virtual_room}_{notebook_id}.csv"
        b64 = base64.b64encode(res.encode())
        payload = b64.decode()
        btn_label, btn_style = "Export notes", "bk_secondary"

        button_styles = core.c.get_html_buttons_styles_code()
        html_button = f"""<html><head><meta name="viewport" content="width=device-width, initial-scale=1">{button_styles}</head>
        <body><a download="{filename}" href="data:text/csv;base64,{payload}" download>
        <button title="⚠️Seulement disponible à l'évaluateur⚠️.
💾Envoi de la réponse (contenu de la cellule actuelle) comme solution officielle.
" class="button {btn_style}">{btn_label}</button></a></body></html>"""
        IPython.display.display(tools.styles(data, cmap=cmap) if cmap is not None else data)
        IPython.display.display(IPython.display.HTML(html_button))
        return

    return tools.styles(data, cmap=cmap) if cmap is not None else data
