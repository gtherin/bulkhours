import os
import json


from .. import core
from . import tools


def get_answers(cell_id, refresh=True, update_git=False, verbose=False):
    config = core.tools.get_config()
    cinfo = core.tools.get_config(is_namespace=True)
    virtual_room, subject, notebook_id = (config.get(v) for v in ["virtual_room", "subject", "notebook_id"])

    students_list = tools.get_users_list(no_admin=False)
    cdata = {}

    filename = core.tools.abspath(
        f"data/cache/{subject}/{virtual_room}/admin_{notebook_id}_{cell_id}.json", create_dir=True
    )
    if os.path.exists(filename) and not refresh:
        with open(filename) as json_file:
            cdata = json.load(json_file)

    docs = core.firebase.get_collection(cell_id, cinfo=cinfo).stream()

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

    config = core.tools.get_config()
    cinfo = core.tools.get_config(is_namespace=True)
    virtual_room, subject, notebook_id = (config.get(v) for v in ["virtual_room", "subject", "notebook_id"])
    language = config["global"].get("language")

    data = {}
    filename = core.tools.abspath(
        f"data/cache/{subject}/{virtual_room}/admin_{notebook_id}_{cell_id}.json", create_dir=True
    )

    if os.path.exists(filename):
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
        return core.firebase.get_document(question=cell_id, user=user, cinfo=cinfo).set(
            {"note": note, "update_time": uptime}
        )
    else:
        return core.firebase.get_document(question=cell_id, user=user, cinfo=cinfo).update({"note": note})
