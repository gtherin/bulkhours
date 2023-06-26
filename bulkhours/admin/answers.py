import os
import json


from .. import core as bulkhours_premium
from . import tools


def get_answers(cell_id, refresh=False, use_cache_if_possible=True, update_git=False, verbose=True):
    config = bulkhours_premium.tools.get_config()
    cinfo = bulkhours_premium.tools.get_config(is_namespace=True)
    virtual_room, subject, notebook_id = (config.get(v) for v in ["virtual_room", "subject", "notebook_id"])

    students_list = tools.get_users_list(no_admin=False)

    cdata = {}

    icell_id = notebook_id + "_" + cell_id if notebook_id not in cell_id else cell_id

    if (
        os.path.exists(filename := tools.get_exo_file(cell_id=icell_id, subject=subject, virtual_room=virtual_room))
        and 0  # not refresh
    ):
        with open(filename) as json_file:
            cdata = json.load(json_file)

    if (use_cache_if_possible and cdata) and not refresh:
        return cdata

    docs = bulkhours_premium.firebase.get_collection(icell_id, cinfo=cinfo).stream()

    data = {}
    for answer in docs:
        student_id = answer.id
        if students_list.query(f"mail == '{student_id}'").empty:
            print(
                f"'\x1b[41mL'étudiant {student_id} est inconnu. Ajouter le depuis le menu dashboard:\nbulkhours.admin.dashboard()\x1b[0m"
                if config["global"]["language"] == "fr"
                else f"'{student_id}' is unknown. Please change it in the dashboard:\nbulkhours.admin.dashboard()"
            )

        if student_id in cdata:
            cdata[student_id].update(answer.to_dict())
        else:
            cdata[student_id] = answer.to_dict()

        if "note" not in cdata[student_id]:
            cdata[student_id]["note"] = 0

        data[student_id] = cdata[student_id]

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    tools.update_github(update_git, msg=f"Cache file ({filename}) of {cell_id}", verbose=verbose)

    return data


def update_note(cell_id, user, note, verbose=True):
    import datetime

    config = bulkhours.tools.get_config()
    cinfo = bulkhours_premium.tools.get_config(is_namespace=True)
    virtual_room, subject, notebook_id = (config.get(v) for v in ["virtual_room", "subject", "notebook_id"])
    language = config["global"].get("language")

    icell_id = notebook_id + "_" + cell_id if notebook_id not in cell_id else cell_id

    data = {}
    if os.path.exists(filename := tools.get_exo_file(cell_id=icell_id, subject=subject, virtual_room=virtual_room)):
        with open(filename) as json_file:
            data = json.load(json_file)

    uptime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if do_create_data := user not in data:
        data[user] = {}

    if "note" in data[user]:
        cmd = (
            f"Pour {cell_id}/{user}, mise à jour de la note de {data[user]['note']} à {note} ({uptime})"
            if language == "fr"
            else f"For {cell_id}/{user}, update note from {data[user]['note']} to {note} ({uptime})"
        )

    else:
        cmd = (
            f"Pour {cell_id}/{user}, mise à jour de la à {note} ({uptime})"
            if language == "fr"
            else f"For {cell_id}/{user}, set note from to {note} at {uptime}"
        )

    if verbose:
        print(f"\x1b[35m\x1b[1m{cmd}\x1b[m")

    data[user]["note"] = note
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    if do_create_data:
        return bulkhours_premium.firebase.get_document(cell_id, user, cinfo=cinfo).set(
            {"note": note, "update_time": uptime}
        )
    else:
        return bulkhours_premium.firebase.get_document(cell_id, user, cinfo=cinfo).update({"note": note})
