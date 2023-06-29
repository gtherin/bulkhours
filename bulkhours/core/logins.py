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
    from collections import OrderedDict

    path = OrderedDict()

    def get_path():
        info = "(%s)" % str(", ".join(path.keys()))
        vals = [v if v != "" else "''" for v in path.values()]
        info += " = (%s)" % str(", ".join(vals))
        return info

    path["db"] = (
        config["database"].split("@")[0] + "@" if "@" in config["database"] else config["database"].split("/")[-1]
    )
    path["subject"] = config["subject"]
    path["virtual_room"] = config["virtual_room"]
    path["nb_id"] = config["notebook_id"]
    path["user"] = (email := config["email"])

    if email is None:
        path["user"] = f"None ❌\x1b[41m\x1b[37m, email not configured\x1b[0m"
        return get_path()

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
        path["user"] += (
            "❌ (\x1b[41m\x1b[37memail inconnu: contacter le professeur svp\x1b[0m), "
            if language == "fr"
            else "❌ (\x1b[41m\x1b[37munknown email: please contact the teacher\x1b[0m), "
        )

    else:
        path["user"] += "🎓" if email in config["global"]["admins"] or tools.is_admin(config) else "✅"

    return get_path()


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

    colors.set_plt_style()
    version = open(tools.abspath("bulkhours/__version__.py")).readlines()[0].split('"')[1]

    einfo = f", ⚠️\x1b[31m\x1b[41m\x1b[37m in admin/teacher🎓 mode\x1b[0m⚠️" if tools.is_admin(config=config) else ""
    print(f"Import BULK Helper cOURSe (\x1b[0m\x1b[36mversion='{version}'\x1b[0m🚀'{einfo}):", end="")
    if "bkloud" not in config["database"]:
        print(
            f"⚠️\x1b[31mDatabase is local (security_level={config['security_level']}). Export your config file if you need persistency.\x1b[0m⚠️",
            end="",
        )
    print("\n" + info)

    contexts.generate_empty_context("student")
    contexts.generate_empty_context("teacher")
    os.environ["BLK_GLOBAL_STATUS"] = f"INITIALIZED"
