import os
import json
import datetime

from .. import core
from . import tools


def get_cfilename(cfg, cell_id):
    return core.tools.abspath(
        f"data/cache/{cfg.subject}/{cfg.virtual_room}/admin_{cfg.notebook_id}_{cell_id}.json", create_dir=True
    )

def get_cdata(cfg, cell_id):
    if os.path.exists(filename:= get_cfilename(cfg, cell_id)):
        with open(filename) as json_file:
            return json.load(json_file)
    return {}


def get_answers(cell_id, refresh=True, update_git=False, verbose=False, aliases={}):
    cfg = core.tools.get_config(is_new_format=True)
    students_list = tools.get_users_list(no_admin=False)

    cdata = get_cdata(cfg, cell_id)

    docs = core.firebase.get_collection(cell_id, cinfo=cfg).stream()

    data = {}
    for answer in docs:

        # Find the right name if typo in the db name
        student_id = str(answer.id).replace(" ", "")
        if student_id in aliases:
            student_id = aliases[student_id]

        if students_list.query(f"mail == '{student_id}'").empty:
            print(
                f"\x1b[41m\x1B[37mL'étudiant \033[1m'{student_id}'\033[0m\x1b[41m\x1B[37m est inconnu. Régularisez la situation depuis le menu dashboard: 'bulkhours.admin.dashboard()'\x1b[0m"
                if cfg.language == "fr"
                else f"\x1b[41m\x1B[37mStudent \033[1m'{student_id}'\033[0m\x1b[41m\x1B[37m is unknown. Please fix the situation in the dashboard: 'bulkhours.admin.dashboard()'\x1b[0m"
            )

        if student_id in cdata:
            cdata[student_id].update(answer.to_dict())
        else:
            cdata[student_id] = answer.to_dict()

        data[student_id] = cdata[student_id]

    with open(filename:= get_cfilename(cfg, cell_id), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    tools.update_github(update_git, msg=f"Cache file ({filename}) of {cell_id}", verbose=verbose)

    return data


def update_notes(cell_id, grades):
    cfg = core.tools.get_config(is_new_format=True)

    uptime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for k in grades.index:
        update_note_in_db(cell_id, grades["mail"][k], grades[cell_id + ".n"][k], uptime, cfg=cfg)


def update_note_in_db(cell_id, user, note, uptime, is_manual=False, cfg=None):

    if not core.tools.GradesErr.is_valid(note):
        return

    info = {"note": note, "note_upd": uptime}

    if is_manual:
        info["note_src"] = "manual"

    try:
        return core.firebase.get_document(question=cell_id, user=user, cinfo=cfg).update(info)
    except:
        return core.firebase.get_document(question=cell_id, user=user, cinfo=cfg).set(info)


def update_note(cell_id, user, note, verbose=True, is_manual=False):

    cfg = core.tools.get_config(is_new_format=True)

    # Get grades
    data = get_cdata(cfg, cell_id)
    if user not in data:
        data[user] = {}

    uptime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if user in data and "note" in data[user]:
        cmd = (
            f"Pour {cell_id}/{user}, mise à jour de la note de {data[user]['note']} à {note} ({uptime})"
            if cfg.language == "fr"
            else f"For {cell_id}/{user}, update note from {data[user]['note']} to {note} ({uptime})"
        )
    else:
        cmd = (
            f"Pour {cell_id}/{user}, mise à jour de la à {note} ({uptime})"
            if cfg.language == "fr"
            else f"For {cell_id}/{user}, set note from to {note} at {uptime}"
        )

    if verbose:
        print(f"\x1b[35m\x1b[1m{cmd}\x1b[m")

    # Set grades
    data[user]["note"] = note
    with open(get_cfilename(cfg, cell_id), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    update_note_in_db(cell_id, user, note, uptime, is_manual=is_manual, cfg=cfg)
