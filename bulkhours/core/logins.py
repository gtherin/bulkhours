import os
import json


def get_cred(k="pi.pyc", d=None, config=None):
    with open(d + k, "w") as f:
        json.dump(
            {
                k: v
                for k, v in config.items()
                if k
                in [
                    "type",
                    "project_id",
                    "private_key_id",
                    "private_key",
                    "client_email",
                    "client_id",
                    "auth_uri",
                    "token_uri",
                    "auth_provider_x509_cert_url",
                    "client_x509_cert_url",
                    "universe_domain",
                ]
            },
            f,
            ensure_ascii=False,
            indent=4,
        )

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = d + k


def create_new_global_params(collection, vrooms=[], admins=""):
    collection.document("global").set(
        gparameters := {
            **{vroom: "" for vroom in vrooms},
            **{
                "admins": admins,
                "chatgpt": False,
                "norm20": False,
                "restricted": False,
                "language": "fr",
                "virtual_rooms": ";".join(vrooms),
            },
        }
    )
    return gparameters


def create_new_nb_params(collection, notebook_id):
    collection.document(notebook_id).set(nparameters := {"exercices": "", "evaluation": "", "page": ""})
    return nparameters


def init_database(config):
    from .installer import get_tokens
    from . import firebase

    if "database" not in config:
        config["database"] = "bkache@free1"

    if "bkache@" in config["database"] or "bkloud@" in config["database"]:
        config = {**config, **get_tokens(config["database"])}

    print(config)

    if "data_cache" in config:
        firebase.DbDocument.set_cache_data(config["data_cache"])
    else:
        directory = os.path.dirname(__file__) + "/../../../bulkhours/bulkhours/bunker/"
        get_cred(d=directory, config=config)


def init_prems():
    from . import tools
    from . import firebase

    config = tools.get_config()
    init_database(config)

    email, subject, notebook_id = (config.get(v) for v in ["email", "subject", "notebook_id"])

    collection = firebase.DbClient().collection(f"{subject}_info".replace("/", "_"))
    if subject is not None:
        col = collection.document("global").get().to_dict()
        if not col:
            col = create_new_global_params(collection, subject)
        config["global"] = col

        if "virtual_room" not in config:
            config["virtual_room"] = config["global"]["virtual_rooms"].split(";")[0]

    if notebook_id is not None:
        col = collection.document(notebook_id).get().to_dict()
        if not col:
            col = create_new_nb_params(collection, notebook_id)
        config["notebooks"] = {notebook_id: col}

    tools.update_config(config)

    info = f"subject/virtualroom/nb_id/user= '{subject}/{config['virtual_room']}/{notebook_id}/"

    if email is None:
        info += f"None ❌\x1b[41m\x1b[37m, email not configurd, no db connection), \x1b[0m"
        return info

    is_known_student = (
        ("virtual_room" in config and email in config["global"][config["virtual_room"]])
        or email in config["global"]["admins"]
        or email == "solution"
    )
    language = config["global"].get("language")

    config["eparams"] = False
    if not is_known_student:
        if config["global"]["restricted"]:
            raise Exception.IndexError(
                f"❌\x1b[41m\x1b[37mL'email '{email}' n'est pas configuré dans la base de données. Contacter le professeur svp\x1b[0m"
                if language == "fr"
                else f"❌\x1b[41m\x1b[37mEmail '{email}' is not configured in the database. Please contact the teacher\x1b[0m"
            )
        info += (
            f"{email}❌ (\x1b[41m\x1b[37memail inconnu: contacter le professeur svp\x1b[0m), "
            if language == "fr"
            else f"{email}❌ (\x1b[41m\x1b[37munknown email: please contact the teacher\x1b[0m), "
        )
    else:
        admin = "🎓" if email in config["global"]["admins"] else "✅"
        info += f"{email}{admin}', "

    return info
