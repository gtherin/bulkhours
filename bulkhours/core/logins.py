import os
import time
import IPython

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

    def get_path(join=", "):
        info = "%s" % str(join.join(path.keys()))
        vals = [v if v != "" else "''" for v in path.values()]
        info += " = %s" % str(join.join(vals))
        return info

    if 0:
        path["db"] = (
            config["database"].split("@")[0] + "@" if "@" in config["database"] else config["database"].split("/")[-1]
        )
    path["subject"] = config["subject"] if "subject" in config else "None"
    path["virtual_room"] = config["virtual_room"] if "virtual_room" in config else "None"
    path["nb_id"] = config["notebook_id"] if "notebook_id" in config else "None"
    path["user"] = (email := config["email"] if "email" in config else "None")

    if email is None:
        path["user"] = f"None ❌\x1b[41m\x1b[37m, email not configured\x1b[0m"
        return get_path()

    is_known_student = (
        ("virtual_room" in config and email in config["global"][config["virtual_room"]])
        or email in config["global"]["admins"]
        or email == tools.REF_USER
    )
    language = config["global"].get("language")
    if config["global"]["admins"] == "":
        is_known_student = True

    config["eparams"] = False

    if not is_known_student:
        path["user"] += (
            "❌ (\x1b[41m\x1b[37memail inconnu: contacter le professeur svp\x1b[0m), "
            if language == "fr"
            else "❌ (\x1b[41m\x1b[37munknown email: please contact the teacher\x1b[0m), "
        )
    else:
        path["user"] += "🎓" if email in config["global"]["admins"] or tools.is_admin(config) else "✅"

    return get_path(join="/")


def commercial(language="en", **kwargs):
    if language == "fr":
        text1 = 'Cette page utilise (<i>Package de support de cours interactif</i>). Si vous aimez cette approche🚀🏆🎯, <br/>vous pouvez supporter le projet sur <a href="https://github.com/gtherin/bulkhours">github</a> en donnant quelques etoiles.'
    else:
        text1 = 'This page is using (<i>A Support course package</i>). If you like this approach🚀🏆🎯, <br/>please support the project on <a href="https://github.com/gtherin/bulkhours">github</a> with some stars.'
    IPython.display.display(
        IPython.display.HTML(
            f"""
<table style="opacity:0.8;">
    <tr>
      <td style="background-color: white;"><a href="https://github.com/gtherin/bulkhours"><img style="background-color: white;" src="https://github.com/gtherin/bulkhours/blob/ce2ce67a250b396b7341becf7deb09da961f2698/data/BulkHours.png?raw=true" width="100"></a></td>
      <td style="background-color: white; text-align:left; color:black">{text1}</td>
      <td style="background-color: white;"><a href="https://github.com/gtherin/bulkhours">
      <img style="background-color: white;" src="https://github.com/gtherin/bulkhours/blob/main/data/github.png?raw=true" width="30"></a></td>
      <td style="background-color: white;"><a href="https://github.com/gtherin/bulkhours"><img style="background-color: white;margin-top: 0.5em;" src="https://github.com/gtherin/bulkhours/blob/main/data/like.gif?raw=true" width="150"></a></td>

</tr></table>
"""
        )
    )

def init_from_token(token, ktoken, packages=None, link=None):
    try:
        import jwt

        # Get data
        data = jwt.decode(jwt=token, key=ktoken, algorithms=["HS256"])
        #if data["email"] == data["email"]:
        init_env(packages=packages, link=link, **data)
        return
        #raise Exception(f"Identity {data['email']}is not the expected one")
    except:
        pass
    print(f"""⚠️\x1b[41m\x1b[37mYour token does not seem to be valid. Service might be limited\x1b[0m⚠️""")


def init_env(packages=None, link=None, plt_style="default", **kwargs):
    """Initialize the environment of the user

        Parameters:
        :param email: email of the student/teacher
        :param subject: subject of the course. Recommended to be unique for one entire subject
        :param notebook_id: id of the current notenook. Recommended to be unique per notebook
        :param database: database config can be:
     - A simple string pointing to a file. With this solution, users should deal with separating informations between students and teachers
    Examples:
    database ="data/cache/course2.json"
    database ="/content/mydatabase.json"
     - A string with an identifier token. This token gives you access to: a real-time database (with id check), api to openai, huggingface, etc.
     As this solution might generate reasonable costs, you should contact contact@bulkhours.fr to get a token.
    database = "bkloud@SUBJECT/teacher::eNq-XXXXXXXXXXXHXXXXX-L29tB"
    database = "bkloud@SUBJECT/CLASSROOM_student::eNq-XXXXXXXXXXXHXXXXX-9tB"
     - A dict of config information. Only firestore config are functional for the moment. Examples:
    database = {"type": "service_account", ..., "universe_domain": "googleapis.com"}

        :param openai_token: to activate openai functionalities [chatgpt, dall-e]
        :param huggingface_token: to activate huggingface functionalities [chatgpt, dall-e]
        :param packages: packages to be installed from pip or apt-get


    Examples:
        bulkhours.init_env(
            email="the.lordoflight@got.grrm",  # Email of the teacher
            subject="bulkhours_sessions",      # Recommended to be unique for one entire subject
            notebook_id="course_edition_nb",   # Recommended to be unique per notebook (id of the current notenook)
            database="data/cache/course2.json" # Database file
                          )
    """

    mode = "production" if "mode" not in kwargs else kwargs["mode"]

    quiet_mode = mode == "passive"

    if "database" in kwargs:
        cfg = firebase.init_database(kwargs)
        info = init_prems(cfg)
        info = f'<pre><font color="#212121">{info}</font></pre>'

    else:
        cfg = kwargs
        info = """<span><font color="#212121">Your token does not seem to be valid⛓️‍💥<br/>Services might be limited⚠️</font>"""

    start_time = time.time()

    if "BULK_PACKAGES_STATUS" not in os.environ:
        installer.install_dependencies(packages, start_time, tools.is_admin(cfg=cfg))
        os.environ["BULK_PACKAGES_STATUS"] = "INITIALIZED"
        os.environ["BULK_ROOT_DIR"] = os.environ["PWD"] if "PWD" in os.environ else os.environ["HOME"] + "/bulkhours"

    colors.set_plt_style(plt_style)
    version = open(tools.abspath("bulkhours/__version__.py")).readlines()[0].split('"')[1]

    if tools.is_admin(cfg=cfg) and (ipp := IPython.get_ipython()):
        monitoring_link = "https://bulkhours.fr" if link is None else link
        IPython.display.display(IPython.display.Markdown(f"""
<table>
  <tr>
    <td><a href="{monitoring_link}"><figure><img src='https://huggingface.co/datasets/guydegnol/bulkhours/resolve/main/logo_green.png?download=true' width="60px" align="center" /></figure>
    </a>
</td><td>
<a href="{monitoring_link}">
<font color="#212121">Import BULK Helper cOURSe (</font><font color="#00A099">version='{version}'🚀, ⚠️ </font><font color="#F23030">in admin/teacher🎓 mode</font><font color="#212121">⚠️)</font><br/>
{info}
<font color="#294D9">Cliquer 👆 pour administrer ce notebook</font>
</a>
</td></tr></table>"""))
    if not tools.is_admin(cfg=cfg) and (ipp := IPython.get_ipython()):
        monitoring_link = "https://bulkhours.fr" if link is None else link
        IPython.display.display(IPython.display.Markdown(f"""
<table>
  <tr>
    <td><a href="{monitoring_link}"><figure><img src='https://huggingface.co/datasets/guydegnol/bulkhours/resolve/main/logo_green.png?download=true' width="35px" align="center" /></figure></a>
    </td>
    <td>
<font color="#212121">Import BULK Helper cOURSe (</font><font color="#00A099">version='{version}'</font><font color="#212121">🚀)</font><br/>
{info}</td></tr></table>"""))

    if ipp := IPython.get_ipython():
        ipp.run_cell(
            """import IPython
import ipywidgets
        """
        )

        if tools.get_platform() == "colab":
            ipp.run_cell("%cd -q /content")

    #if not tools.is_admin(cfg=cfg) and not quiet_mode:
    #    print("\n- session-info: " + info)

    if tools.get_value("openai_token") is not None or tools.get_value("huggingface_token") is not None:
        external_services = "- extra-services:\033[92m"
    if tools.get_value("openai_token") is not None:
        external_services += " openai 🤖, "
        if ipp := IPython.get_ipython() and False:  # Deactivate warning for the moment
            ipp.run_cell(
                """ try:
    import openai

    openai.api_key = "%s"
except ModuleNotFoundError:
    print("LOG import of openai failed 💥")
"""
                % tools.get_value("openai_token")
            )

    if tools.get_value("huggingface_token") is not None:
        import ipywidgets
        from .. import ml

        os.environ["BULK_HUGGINGFACE_TOKEN"] = tools.get_value("huggingface_token")
        external_services += "huggingface 🤗"

        with ipywidgets.Output():
            ml.PPOHugs()

    if not quiet_mode:
        if tools.get_value("openai_token") is not None or tools.get_value("huggingface_token") is not None:
            print(external_services + "\033[00m")
    contexts.generate_empty_context("student")
    contexts.generate_empty_context("teacher")
    os.environ["BULK_GLOBAL_STATUS"] = f"INITIALIZED"
    return cfg
