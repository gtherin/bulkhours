import os
import json
import datetime
import zoneinfo
from argparse import Namespace
from . import tools

REF_USER = "solution"


def get_question_id(question, sep="_", prefix=True, cinfo=None):
    if cinfo is None:
        return question
    if type(cinfo) == dict:
        cinfo = Namespace(**cinfo)

    if not prefix:
        return cinfo.subject + "_" + question

    if cinfo.notebook_id not in question:
        question = cinfo.notebook_id + "_" + question

    if cinfo.subject not in question or cinfo.virtual_room not in question:
        return cinfo.subject + sep + cinfo.virtual_room + sep + question

    return question


class DbDocument:
    data_base_cache = None
    data_base_info = None

    compliant_fields = {
        "bkloud": ["type", "project_id", "private_key_id", "private_key", "client_email", "client_id", "auth_uri"]
        + [
            "token_uri",
            "auth_provider_x509_cert_url",
            "client_x509_cert_url",
            "universe_domain",
        ],
        "global": {
            "admins": "",
            "chatgpt": False,
            "language": "fr",
            "norm20": False,
            "restricted": False,
            "virtual_rooms": "room1",
        },
        "notebook": {"exercices": "", "evaluation": "", "page": ""},
        "session": dict(email="john.doe@un.known", notebook_id="", database="data/cache/free1.json", subject=""),
    }

    @staticmethod
    def write_cache_data() -> None:
        with open(DbDocument.data_base_info, "w", encoding="utf-8") as f:
            json.dump(DbDocument.data_base_cache, f, ensure_ascii=False, indent=4)

    @staticmethod
    def set_cache_data(database) -> None:
        DbDocument.data_base_cache = {}
        if type(database) == dict:
            DbDocument.data_base_cache = database
        elif type(database) == str:
            if not os.path.exists(os.path.dirname(database)):
                database = os.path.abspath(os.path.dirname(__file__) + f"/../../{database}")
            DbDocument.data_base_info = database
            if os.path.exists(database):
                with open(database) as json_file:
                    DbDocument.data_base_cache = json.load(json_file)
        else:
            print("Fuck")

    def __init__(self, question, user) -> None:
        self.question, self.user = question, user

    @property
    def id(self):
        return self.user

    def set(self, data) -> None:
        DbDocument.data_base_cache[self.question][self.user] = data
        DbDocument.write_cache_data()

    def get(self):
        return self

    def to_dict(self):
        return DbDocument.data_base_cache[self.question][self.user]

    def update(self, data) -> None:
        DbDocument.data_base_cache[self.question][self.user].update(data)
        DbDocument.write_cache_data()


class DbCollection:
    def __init__(self, question) -> None:
        self.question = question

    def document(self, user) -> None:
        if self.question not in DbDocument.data_base_cache:
            DbDocument.data_base_cache[self.question] = {}
        if user not in DbDocument.data_base_cache[self.question]:
            DbDocument.data_base_cache[self.question][user] = {}

        return DbDocument(self.question, user)

    def stream(self):
        return [DbDocument(self.question, user) for user in DbDocument.data_base_cache[self.question]]


class DbClient:
    def __init__(self) -> None:
        pass

    def collection(self, question, prefix=True, cinfo=None):
        question_id = get_question_id(question, prefix=prefix, cinfo=cinfo)
        if DbDocument.data_base_cache is None:
            from google.cloud import firestore

            return firestore.Client().collection(question_id)
        else:
            return DbCollection(question_id)


def init_config(config_id, config):
    collection = DbClient().collection(f"{config.get('subject')}_info".replace("/", "_"))
    if config_id not in config:
        config[config_id] = {}

    if not collection.document(config_id).get().to_dict():
        save_config(config_id, config)
    config[config_id].update(collection.document(config_id).get().to_dict())

    return config


def init_database(config) -> None:
    from .installer import get_tokens

    config = tools.get_config(**config)

    for k, v in DbDocument.compliant_fields["session"].items():
        if k not in config:
            config[k] = v

    if "global" not in config:
        config["global"] = {}
    if "bkache@" in config["database"] or "bkloud@" in config["database"]:
        config["global"].update(get_tokens(config["database"]))
    if "subject" in config["global"]:
        config["subject"] = config["global"]["subject"]
    else:
        config["global"]["subject"] = config["subject"]

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (cfilename := tools.abspath("bulkhours/bunker/pi.pyc"))
    if type(database := config["database"]) == dict:
        with open(cfilename, "w") as f:
            json.dump(database, f, ensure_ascii=False, indent=4)
    elif "bkloud@" in database:
        with open(cfilename, "w") as f:
            cols = DbDocument.compliant_fields["bkloud"]
            json.dump({k: v for k, v in config["global"].items() if k in cols}, f, ensure_ascii=False, indent=4)

    else:
        datafile = config["global"]["data_cache"] if "data_cache" in config["global"] else database
        datafile = tools.abspath(datafile)

        DbDocument.set_cache_data(datafile)

    config = init_config("global", config)

    if "virtual_room" not in config:
        config["virtual_room"] = config["global"]["virtual_rooms"].split(";")[0]

    config = init_config(config["notebook_id"], config)

    return tools.update_config(config)


def get_collection(question, prefix=True, cinfo=None):
    return DbClient().collection(get_question_id(question, prefix=prefix, cinfo=cinfo))


def get_document(question, user, prefix=True, cinfo=None):
    return get_collection(question, prefix=prefix, cinfo=cinfo).document(user)


def get_questions_ids(questions, cinfo=None):
    # Split questions
    if type(questions) == list:
        return [get_question_id(question, cinfo=cinfo) for question in questions]
    if "," in questions:
        questions = questions.replace(",", ";")
    return [get_question_id(question, cinfo=cinfo) for question in questions.split(";")]


def delete_documents(cinfo, questions, user=REF_USER, verbose=False):
    # Split questions
    questions_ids = get_questions_ids(questions, cinfo=cinfo)

    for question_id in questions_ids:
        if verbose:
            print(f"\x1b[31m\x1b[1mDelete anwser for {question_id}/{user} (cloud)\x1b[m")

        get_document(question_id, user, cinfo=cinfo).delete()


def send_answer_to_corrector(cinfo, update=True, comment="", update_time=True, **kwargs):
    question_alias = get_question_id(cinfo.notebook_id + "/" + cinfo.cell_id, sep="/", cinfo=cinfo)
    source = "local@" if DbDocument.data_base_info is not None else "cloud@"
    question_alias = source + question_alias

    user = kwargs["user"] if "user" in kwargs else cinfo.user
    alias = user.split("@")[0]
    if "." in alias:
        alias = alias.split(".")
        alias = alias[0] + "." + alias[1][0]

    if cinfo.restricted:
        corr = get_solution_from_corrector(cinfo.icell_id, corrector=REF_USER, cinfo=cinfo)
        if corr is not None and user != REF_USER:
            if cinfo.language == "fr":
                print(
                    f"\x1b[31m\x1b[1mLa réponse ne peut être soumise. La solution pour '{question_alias}' a déjà été publiée.\x1b[m"
                )
            else:
                print(
                    f"\x1b[31m\x1b[1mThe answer can not be submitted. Solution for '{question_alias}' has already been published.\x1b[m"
                )
            return

    uptime = datetime.datetime.now(tz=zoneinfo.ZoneInfo("Europe/Paris")).strftime("%Y-%m-%d %H:%M:%S")

    if update_time:
        kwargs.update({"update_time": uptime})
    if user == REF_USER and "note" not in kwargs:
        kwargs.update({"note": 10})
    else:
        kwargs = {k: v for k, v in kwargs.items() if k not in ["evaluation", "explanation", "visible"]}

    if update and get_document(cinfo.icell_id, user, cinfo=cinfo).get().to_dict():
        get_document(cinfo.icell_id, user, cinfo=cinfo).update(kwargs)
    else:
        get_document(cinfo.icell_id, user, cinfo=cinfo).set(kwargs)

    if user == REF_USER:
        if cinfo.language == "fr":
            print(f"\x1b[31m\x1b[1mLa solution a été soumise à {uptime} pour {question_alias}")
        else:
            print(f"\x1b[31m\x1b[1mSolution has been updated at {uptime} for {question_alias}")
    else:
        if cinfo.language == "fr":
            comment = "Réponse soumise à" if comment == "" else "Réponse '" + comment + "' a été soumise à"
            print(
                f"\x1b[32m\x1b[1m{comment} {uptime} pour '{question_alias}/{alias}'. Vous pouvez soumettre plusieurs fois\x1b[m"
            )
        else:
            comment = "Answer has been submited at" if comment == "" else "Answer " + comment + " has been submited"
            print(
                f"\x1b[32m\x1b[1m{comment} {uptime} for '{question_alias}/{alias}'. You can resubmit it several times\x1b[m"
            )

    if cinfo.help:
        print(
            f"""\x1b[33m\x1b[1mLe format est le suivant 'sujet/classe/notebook/exercice/utilisateur':
- sujet (subject): est le module du cours,
- class (virtual_room): est la classe dans la laquelle un cours est enseignant de manière synchrone,
- notebook (notebook_id): est l'identifiant de ce notebook et de celui des élèves,
- exercice (cell_id): est l'identifiant de ce notebook et de celui des élèves,
- user (user): est l'identifiant de l'eleve qui soumet la réponse,
            \x1b[m"""
        )


def get_solution_from_corrector(question, corrector=REF_USER, cinfo=None):
    return get_document(question, corrector, cinfo=cinfo).get().to_dict()


def save_config(label, config, verbose=False):
    cols = DbDocument.compliant_fields["global"] if label == "global" else DbDocument.compliant_fields["notebook"]

    print("KKKKKKKKKKKKKKKKK", label, config)

    params = {k: config[label][k] if k in config[label] else v for k, v in cols.items()}
    if label == "global":
        for room in params["virtual_rooms"].split(";"):
            params[room] = config[label][room] if room in config[label] else ""

    get_document("info", label, prefix=False, cinfo=Namespace(**config)).set(params)

    if verbose:
        cmd = (
            f"Mise à jour des informations des parametres {label}"
            if config["global"]["language"] == "fr"
            else f"Update {label} parameters "
        )

        print(f"\x1b[32m\x1b[1m{cmd}\x1b[m")
