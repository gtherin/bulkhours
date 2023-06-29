import os
import time

from . import firebase
from . import installer
from . import tools
from . import colors
from . import contexts


def init_config(config_id, collection, config):
    if config_id not in config:
        config[config_id] = {}

    if not collection.document(config_id).get().to_dict():
        firebase.save_config(config_id, config)
    config[config_id].update(collection.document(config_id).get().to_dict())

    return config


def init_prems(config):
    db_label = config["database"].split("@")[0] + "@" if "@" in config["database"] else ""

    email, notebook_id = (config.get(v) for v in ["email", "notebook_id"])
    subject = config["global"].get("subject")

    info = f"subject/virtualroom/nb_id/user='{db_label}{subject}/{config['virtual_room']}/{notebook_id}/"

    if email is None:
        info += f"None ❌\x1b[41m\x1b[37m, email not configurd, no db connection), \x1b[0m"
        return info

    is_known_student = (
        ("virtual_room" in config and email in config["global"][config["virtual_room"]])
        or email in config["global"]["admins"]
        or email == "solution"
    )
    language = config["global"].get("language")
    if config["global"]["admins"] == "":
        is_known_student = True

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


def init_env(packages=None, **kwargs):
    """
    Initialize the environment for the notebook
    email: email of the student
    from_scratch: if True, local variables is reinitialized
    packages:= to install packages from pip or apt-get
    database: database to use

    """

    config = firebase.init_database(kwargs)

    info = init_prems(config)
    start_time = time.time()

    if packages is not None and "BLK_PACKAGES_STATUS" not in os.environ:
        installer.install_dependencies(packages, start_time)
        os.environ["BLK_PACKAGES_STATUS"] = f"INITIALIZED"

    config = tools.get_config()
    colors.set_plt_style()
    version = open(tools.abspath("bulkhours/__version__.py")).readlines()[0].split('"')[1]

    einfo = f", ⚠️\x1b[31m\x1b[41m\x1b[37m in admin/teacher🎓 mode\x1b[0m⚠️" if tools.is_admin(config=config) else ""
    print(f"Import BULK Helper cOURSe (\x1b[0m\x1b[36mversion='{version}'\x1b[0m🚀'{einfo}):", end="")
    if "bkloud" not in config["database"]:
        print(
            f"⚠️\x1b[31mDatabase is local. Export your config file if you need persistency.\x1b[0m⚠️",
            end="",
        )
    print("\n" + info)

    contexts.generate_empty_context("student")
    contexts.generate_empty_context("teacher")
    os.environ["BLK_GLOBAL_STATUS"] = f"INITIALIZED"
