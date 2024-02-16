import os
import json
import datetime

from .. import core
from . import tools


def get_cfilename(cfg, cell_id):
    return core.tools.abspath(
        f"data/cache/{cfg.subject}/{cfg.virtual_room}/admin_{cfg.notebook_id}_{cell_id}.json",
        create_dir=True,
    )


def get_cdata(cfg, cell_id):
    if os.path.exists(filename := get_cfilename(cfg, cell_id)):
        with open(filename) as json_file:
            return json.load(json_file)
    return {}


def user_is_unknown(cfg, student_id, cell_id):
    print(
        f"\x1b[41m\x1B[37mL'étudiant \033[1m'{student_id}'\033[0m\x1b[41m\x1B[37m est inconnu ({cell_id}). Régularisez la situation depuis le menu dashboard: 'bulkhours.admin.dashboard()'\x1b[0m"
        if cfg.language == "fr"
        else f"\x1b[41m\x1B[37mStudent \033[1m'{student_id}'\033[0m\x1b[41m\x1B[37m is unknown ({cell_id}). Please fix the situation in the dashboard: 'bulkhours.admin.dashboard()'\x1b[0m"
    )


def get_answers(cell_id, update_git=False, verbose=False, aliases={}):
    cfg = core.tools.get_config(is_new_format=True)
    students_list = tools.get_users_list(no_admin=False)

    cdata = get_cdata(cfg, cell_id)

    docs = core.firebase.get_collection(cell_id, cinfo=cfg).stream()

    data = {}
    for answer in docs:
        # Find the right name if typo in the db name
        student_id = str(answer.id).replace(" ", "")
        if aliases is not None and student_id in aliases:
            student_id = aliases[student_id]

        if students_list.query(f"mail == '{student_id}'").empty:
            user_is_unknown(cfg, student_id, cell_id)

        if student_id in cdata:
            cdata[student_id].update(answer.to_dict())
        else:
            cdata[student_id] = answer.to_dict()

        data[student_id] = cdata[student_id]

    with open(filename := get_cfilename(cfg, cell_id), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    tools.update_github(
        update_git, msg=f"Cache file ({filename}) of {cell_id}", verbose=verbose
    )

    return data

def store_grades(grades, question, cfg=None):

    import os
    #import sqlalchemy as sa
    import mysql.connector as mariadbconnector
    import datetime

    if "BULK_PWD" not in os.environ or "BULK_DBS" not in os.environ:
        print(f"Database is not setup {question}")

    pwd, dbs = os.environ["BULK_PWD"], os.environ["BULK_DBS"]
    
    if cfg is None:
        cfg = core.tools.get_config(is_new_format=True)
    # engine = sa.create_engine(f"mariadb+mariadbconnector://moodle_user:{pwd}@{dbs}:3306/moodle", echo=True)
    engine = mariadbconnector.connect(host=dbs, database='moodle', user='moodle_user', password=pwd)
    table_name = "bulk_" + core.firebase.get_question_id(question=question, cinfo=cfg)
    uptime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    grades.assign(uptime=uptime).to_sql(table_name, engine, if_exists="replace")


def update_grades(cell_id, grades, grade_name, db_storage=True):
    cfg = core.tools.get_config(is_new_format=True)

    uptime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 
    if db_storage:
        store_grades(grades, cell_id, cfg=cfg)

    for k in grades.index:
        update_note_in_db(
            cell_id,
            grades["mail"][k],
            grades[cell_id + ".n"][k],
            uptime,
            cfg=cfg,
            grade_name=grade_name,
            grade_comment=grades[cell_id + ".c"][k],
        )


def update_note_in_db(cell_id, user, grade, uptime, grade_name="grade", grade_comment="", cfg=None):
    core.Grade.check_gradname_validity(grade_name)

    if not core.Grade.is_valid(grade):
        return

    info = {grade_name: grade, grade_name + "_upd": uptime, grade_name + "_comment": grade_comment}

    try:
        return core.firebase.get_document(
            question=cell_id, user=user, cinfo=cfg
        ).update(info)
    except:
        return core.firebase.get_document(question=cell_id, user=user, cinfo=cfg).set(
            info
        )


def update_grade(cell_id, user, grade, verbose=True, grade_name="grade", comment=""):
    cfg = core.tools.get_config(is_new_format=True)

    # Get grades
    data = get_cdata(cfg, cell_id)
    if user not in data:
        data[user] = {}

    uptime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if user in data and grade_name in data[user]:
        cmd = (
            f"Pour {cell_id}/{user}, mise à jour de la note '{grade_name}' de {data[user][grade_name]} à {grade} ({uptime})"
            if cfg.language == "fr"
            else f"For {cell_id}/{user}, update the grade '{grade_name}' from {data[user][grade_name]} to {grade} ({uptime})"
        )
    else:
        cmd = (
            f"Pour {cell_id}/{user}, mise à jour de la note '{grade_name}' à {grade} ({uptime})"
            if cfg.language == "fr"
            else f"For {cell_id}/{user}, set the grade '{grade_name}' from to {grade} at {uptime}"
        )
    import IPython

    if verbose:
        print(f"\x1b[35m\x1b[1m{cmd}\x1b[m")
        if comment != "":
            IPython.display.display(
                IPython.display.Markdown(f"* **{user}**: {comment}")
            )

    # Set grades
    data[user][grade_name] = grade
    with open(get_cfilename(cfg, cell_id), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    update_note_in_db(cell_id, user, grade, uptime, grade_name=grade_name, grade_comment=comment, cfg=cfg)
