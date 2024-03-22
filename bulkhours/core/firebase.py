import os
import json
import datetime
import pandas as pd
from argparse import Namespace
from . import tools
from .tools import REF_USER


def get_paris_time():
    if tools.get_platform() == "sagemaker":
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    import zoneinfo

    return datetime.datetime.now(tz=zoneinfo.ZoneInfo("Europe/Paris")).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def get_question_id(question, sep="_", cinfo=None):
    if cinfo is None:
        return question
    if type(cinfo) == dict:
        cinfo = Namespace(**cinfo)

    return (
        cinfo.subject
        + sep
        + cinfo.virtual_room
        + sep
        + cinfo.notebook_id
        + sep
        + question
    )

def get_engine(database=None, **kwargs):
    if "BULK_DUSER" not in os.environ:
        return None
    import sqlalchemy as sa
    tools.install_if_needed("mariadb")

    if "BULK_DUSER" not in os.environ:
        return None
    user, dbs, dbk  = os.environ['BULK_DUSER'], os.environ['BULK_DBS'], os.environ['BULK_DTOKEN']
    return sa.create_engine(f"mariadb+mariadbconnector://{user}:{dbk}@{dbs}:3306/{database}", **kwargs)

ENGINE = get_engine(database="moodle", echo=False)
BENGINE = get_engine(database="bulkdb", echo=True)

def read_sql(request, echo=False, usebkdb=False, **kwargs):
    engine = BENGINE if usebkdb else ENGINE # get_engine(echo=echo, pool_size=10, max_overflow=20)
    with engine.connect() as connection:
        df = pd.read_sql(request, connection, **kwargs)
    engine.dispose()
    return df

def to_sql(df, table_name, usebkdb=False, if_exists="replace", **kwargs):
    engine = BENGINE if usebkdb else ENGINE # get_engine(echo=echo, pool_size=10, max_overflow=20)
    print("DEBUG", engine, table_name, if_exists)
    df = df.rename(columns={"mail": "email", "uptime": "update_time"})

    if if_exists == "update_or_insert":
        dfold = read_sql(table_name, engine)
        indexes = df.index.names
        if not dfold.empty:
            df = pd.concat([dfold.set_index(indexes).assign(new=0), df.assign(new=1)], axis=1)

        # TODO: make it work
        with engine.begin() as connection:
            #df.to_sql(table_name + "_tmp", connection, if_exists="replace")
            df.to_sql(table_name, connection, if_exists="replace")
        #engine.dispose()

        #with engine.begin() as connection:
        #    sql = f"""update moodle.{table_name} as f set token = t.token FROM {table_name}_tmp as t where f.subject = t.subject and f.key = t.key"""
        #    connection.execute(sql)

    else:
        with engine.begin() as connection:
            df.to_sql(table_name, connection, if_exists=if_exists)
    engine.dispose()


class DbDocument:
    data_base_cache = None
    data_base_info = None

    compliant_fields = {
        "bkloud": [
            "type",
            "project_id",
            "private_key_id",
            "private_key",
            "client_email",
            "client_id",
            "auth_uri",
        ]
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
        "notebook": {"exercices": "", "evaluation": "", "page": "", "is_locked": ""},
        "session": dict(
            email="john.doe@un.known",
            notebook_id="n",
            database="data/cache/starwars.json",
            subject="s",
        ),
    }

    @staticmethod
    def write_cache_data() -> None:
        if DbDocument.data_base_info is not None:
            with open(DbDocument.data_base_info, "w", encoding="utf-8") as f:
                json.dump(DbDocument.data_base_cache, f, ensure_ascii=False, indent=4)

    @staticmethod
    def read_cache_data() -> None:
        if DbDocument.data_base_info is not None and os.path.exists(
            DbDocument.data_base_info
        ):
            with open(DbDocument.data_base_info) as json_file:
                DbDocument.data_base_cache = json.load(json_file)

    @staticmethod
    def set_cache_data(database) -> None:
        DbDocument.data_base_cache = {}
        if type(database) == dict:
            DbDocument.data_base_cache = database
        elif type(database) == str:
            if not os.path.exists(os.path.dirname(database)):
                database = os.path.abspath(
                    os.path.dirname(__file__) + f"/../../{database}"
                )
            DbDocument.data_base_info = database
            DbDocument.read_cache_data()
        else:
            print("Fuck")

    def __init__(self, question, user) -> None:
        self.question, self.user = question, user

    @property
    def id(self):
        return self.user

    def set(self, data) -> None:
        DbDocument.read_cache_data()
        if self.question not in DbDocument.data_base_cache:
            DbDocument.data_base_cache[self.question] = {}

        DbDocument.data_base_cache[self.question][self.user] = data
        DbDocument.write_cache_data()

    def get(self):
        return self

    def to_dict(self):
        return DbDocument.data_base_cache[self.question][self.user]

    def update(self, data) -> None:
        DbDocument.read_cache_data()
        DbDocument.data_base_cache[self.question][self.user].update(data)
        DbDocument.write_cache_data()

    def delete_fields(self, data, fields) -> None:
        DbDocument.read_cache_data()
        for c in fields:
            if c in data:
                del data[c]
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
        DbDocument.read_cache_data()
        if self.question not in DbDocument.data_base_cache:
            return []
        return [
            DbDocument(self.question, user)
            for user in DbDocument.data_base_cache[self.question]
        ]


class DbClient:
    def __init__(self) -> None:
        pass

    def collection(self, question=None, question_id=None, cinfo=None):
        if question_id is None:
            question_id = get_question_id(question, cinfo=cinfo)
        if DbDocument.data_base_cache is None:
            from google.cloud import firestore

            return firestore.Client().collection(question_id)
        else:
            return DbCollection(question_id)


def init_config(config_id, cfg):
    collection = DbClient().collection(
        question_id=f"{cfg.subject}_info".replace("/", "_")
    )
    if config_id not in cfg:
        cfg[config_id] = {}

    if not collection.document(config_id).get().to_dict():
        save_config(config_id, cfg)
    cfg[config_id].update(collection.document(config_id).get().to_dict())

    return cfg


def init_database(cfg) -> None:
    from .installer import get_tokens

    tokens = get_tokens(cfg["database"], verbose=False)
    if len(tokens) == 0:
        print(
            f"""⚠️\x1b[41m\x1b[37mYour token does not seem to be valid anymore.\x1b[0m⚠️ 
Check that your token is still valid (contact: contact@bulkhours.fr).
The database has been reset to the local file '{cfg["database"]}'.
"""
        )
        return

    # Configure  database
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (cfilename := tools.safe(ext=True))
    with open(cfilename, "w") as f:
        json.dump({k: tokens[k] for k in DbDocument.compliant_fields["bkloud"]}, f, ensure_ascii=False, indent=4)

    # Get global info
    cfg["global"] = get_document(question_id=cfg["subject"] + "_info", user="global").get().to_dict()
    cfg["global"]["subject"] = cfg["subject"]

    # Get notebook info
    ndata = get_document(question_id=cfg["subject"] + "_info", user=cfg["notebook_id"]).get().to_dict()
    for k, v in DbDocument.compliant_fields["notebook"].items():
        cfg[k] = ndata[k] if k in ndata else v
    cfg[cfg["notebook_id"]] = ndata

    tools.update_config(cfg)

    #for k, v in DbDocument.compliant_fields["session"].items():
    #    cfg[k] = cfg[k] if k in cfg else tokens[k]

    #cfg = init_config("global", cfg)

    #if cfg.notebook_id:
    #    cfg = init_config(cfg.notebook_id, cfg)

    return tools.update_config(cfg)


def get_collection(question=None, question_id=None, cinfo=None):
    if question_id is None:
        question_id = get_question_id(question, cinfo=cinfo)

    return DbClient().collection(question_id=question_id)


def get_document(question=None, question_id=None, user=None, cinfo=None):
    if question_id is None:
        question_id = get_question_id(question, cinfo=cinfo)
    return get_collection(question_id=question_id, cinfo=cinfo).document(user)


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

    if verbose:
        print(f"\x1b[31m\x1b[1mDelete answer for {user}: \x1b[m", end="")

    for question_id in questions_ids:
        if verbose:
            print(f"\x1b[31m\x1b[1m{question_id},\x1b[m", end="")

        get_document(question_id=question_id, user=user, cinfo=cinfo).delete()
        get_document(question_id=question_id + "_log", user=user, cinfo=cinfo).delete()

    print(f"\x1b[31m\x1b[1m (cloud)\x1b[m")


def update_if_possible(document, kwargs):
    try:
        document.update(kwargs)
    except:
        document.set(kwargs)


def send_answer_to_corrector(
    cinfo,
    update=True,
    comment="",
    update_time=True,
    fake=False,
    store_log=True,
    **kwargs,
):
    source = "local@" if DbDocument.data_base_info is not None else "cloud@"
    question_alias = source + get_question_id(cinfo.cell_id, sep="/", cinfo=cinfo)
    config = tools.get_config(is_new_format=True)

    user = kwargs["user"] if "user" in kwargs else cinfo.user
    alias = user.split("@")[0]
    if "." in alias:
        alias = alias.split(".")
        alias = alias[0] + "." + alias[1][0]

    if (
        config.security_level == 0
        and cinfo.cell_id not in config[config.notebook_id]["exercices"]
    ):
        config[config["notebook_id"]]["exercices"] += ";" + cinfo.cell_id
        save_config(config.notebook_id, config)

    if "force" in kwargs and kwargs["force"]:
        pass
        # print("⚠️\x1b[31m\x1b[1mForce mode\x1b[m")
    elif (
        user != REF_USER
        and "is_locked" in config[config.notebook_id]
        and (config.virtual_room + ";") in config[config.notebook_id]["is_locked"]
    ):
        if cinfo.language == "fr":
            print(
                "⚠️\x1b[31m\x1b[1mLes réponses ne peuvent plus être soumise dans ce notebook.\x1b[m"
            )
        else:
            print(
                "⚠️\x1b[31m\x1b[1mThe answers can not be submitted anymore for this notebook.\x1b[m"
            )
        return

    if "force" not in kwargs or not kwargs["force"]:  # cinfo.restricted:
        corr = get_solution_from_corrector(
            cinfo.cell_id, corrector=REF_USER, cinfo=cinfo
        )
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

    uptime = get_paris_time()

    if "IPADDRESS" in os.environ:
        kwargs.update({"ip": os.environ["IPADDRESS"]})
    else:
        kwargs.update({"ip": "unknown"})
    if update_time:
        kwargs.update({"update_time": uptime})
    if user == REF_USER and "grade_man" not in kwargs:
        #TODO: CHANGE THAT SHITTY 10
        kwargs.update({"grade_man": 10, "grade_man_upd": uptime})
    else:
        kwargs = {
            k: v
            for k, v in kwargs.items()
            if k not in ["evaluation", "explanation", "hint", "visible"]
        }

    if not fake:
        if (
            update
            and get_document(question=cinfo.cell_id, user=user, cinfo=cinfo)
            .get()
            .to_dict()
        ):
            get_document(question=cinfo.cell_id, user=user, cinfo=cinfo).update(kwargs)
        else:
            get_document(question=cinfo.cell_id, user=user, cinfo=cinfo).set(kwargs)

        if store_log:
            for a in ["answer", "main_execution"]:
                if a in kwargs:
                    update_if_possible(
                        get_document(
                            question=cinfo.cell_id + "_log",
                            user=kwargs["user"],
                            cinfo=cinfo,
                        ),
                        {uptime: kwargs[a]},
                    )
                    break

    if user == REF_USER:
        if cinfo.language == "fr":
            print(
                f"\x1b[31m\x1b[1mLa solution a été soumise à {uptime} pour {question_alias}"
            )
        else:
            print(
                f"\x1b[31m\x1b[1mSolution has been updated at {uptime} for {question_alias}"
            )
    else:
        if "force" in kwargs and kwargs["force"]:
            import IPython

            IPython.display.display(
                IPython.display.Markdown(
                    f"* <font color='#581845'>submission of '{question_alias}/{alias}' at {uptime}</font>"
                )
            )

        elif cinfo.language == "fr":
            comment = (
                "Réponse soumise à"
                if comment == ""
                else "Réponse '" + comment + "' a été soumise à"
            )
            print(
                f"\x1b[32m\x1b[1m{comment} {uptime} pour '{question_alias}/{alias}'. Vous pouvez soumettre plusieurs fois\x1b[m"
            )
        else:
            comment = (
                "Answer has been submited at"
                if comment == ""
                else "Answer " + comment + " has been submited"
            )
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
    DbDocument.read_cache_data()
    return get_document(question=question, user=corrector, cinfo=cinfo).get().to_dict()


def save_config(label, config, verbose=False):
    cols = (
        DbDocument.compliant_fields["global"]
        if label == "global"
        else DbDocument.compliant_fields["notebook"]
    )
    cinfo = Namespace(**config)

    params = {k: config[label][k] if k in config[label] else v for k, v in cols.items()}
    if label == "global":
        for room in params["virtual_rooms"].split(";"):
            params[room] = config[label][room] if room in config[label] else ""

    get_document(
        question_id=cinfo.subject + "_info", user=label, cinfo=Namespace(**config)
    ).set(params)
    tools.update_config(config)

    if verbose:
        cmd = (
            f"Mise à jour des informations des parametres {label}"
            if config["global"]["language"] == "fr"
            else f"Update {label} parameters "
        )

        print(f"\x1b[32m\x1b[1m{cmd}\x1b[m")
