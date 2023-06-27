from . import firebase


def init_global_params(collection, config):
    if not collection.document("global").get().to_dict():
        firebase.save_config("global", config)
    config["global"].update(collection.document("global").get().to_dict())

    if "notebook_id" not in config:
        config["notebook_id"] = "nob"

    if "virtual_room" not in config:
        config["virtual_room"] = config["global"]["virtual_rooms"].split(";")[0]

    return config


def init_nb_params(collection, config):
    notebook_id = config.get("notebook_id", config)
    if notebook_id not in config:
        config[notebook_id] = {}

    if not collection.document(notebook_id).get().to_dict():
        firebase.save_config(notebook_id, config)
    config[notebook_id].update(collection.document(notebook_id).get().to_dict())

    return config


def init_database(**kwargs):
    from .installer import get_tokens
    from . import tools

    if "from_scratch" not in kwargs:
        kwargs["from_scratch"] = True
    config = tools.get_config(**kwargs)

    if "database" not in config:
        config["database"] = "bkache@free1"

    if "global" not in config:
        config["global"] = {}

    if "bkache@" in config["database"] or "bkloud@" in config["database"]:
        config["global"].update(get_tokens(config["database"]))
    config["subject"] = config["global"]["subject"]

    firebase.DbDocument.init_database(config)

    collection = firebase.DbClient().collection(f"{config.get('subject')}_info".replace("/", "_"))
    config = init_global_params(collection, config)
    config = init_nb_params(collection, config)

    tools.update_config(config)

    return config


def init_prems(**kwargs):
    config = init_database(**kwargs)
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


class CellContext:
    """This context cell contains cell executions:
    - Two are defined by default: 'student' or 'teacher'
    When using the correction code, the stdout and answer are filled
    """

    @property
    def stdout(self):
        return False

    @property
    def answer(self):
        return False


import os
import time


def init_env(packages=None, **kwargs):
    import IPython
    from . import installer
    from . import tools
    from . import colors as c

    info = init_prems(**kwargs)
    start_time = time.time()

    if ipp := IPython.get_ipython():
        from .evaluation import Evaluation
        from ..hpc.compiler import CCPPlugin

        ipp.register_magics(CCPPlugin(ipp))
        ipp.register_magics(Evaluation(ipp))

    if packages is not None and "BLK_PACKAGES_STATUS" not in os.environ:
        installer.install_dependencies(packages, start_time)
        os.environ["BLK_PACKAGES_STATUS"] = f"INITIALIZED"

    config = tools.get_config()
    c.set_plt_style()
    version = open(tools.abspath("bulkhours/__version__.py")).readlines()[0].split('"')[1]

    einfo = f", ⚠️\x1b[31m\x1b[41m\x1b[37m in admin/teacher🎓 mode\x1b[0m⚠️" if tools.is_admin(config=config) else ""
    print(f"Import BULK Helper cOURSe (\x1b[0m\x1b[36mversion='{version}'\x1b[0m🚀'{einfo}):")
    print(f"{info})")
    if "bkloud" not in config["database"]:
        print(
            f"⚠️\x1b[41m\x1b[37mDatabase is not replicated on the cloud. Persistency is not garantee outside the notebook\x1b[0m⚠️"
        )

    return CellContext(), CellContext()
