import os
import json
import ipywidgets
import IPython
from argparse import Namespace
from .config import Config


def get_platform():
    if os.path.exists("/content"):
        return "colab"
    elif os.path.exists("/home/studio-lab-user"):
        return "sagemaker"
    elif os.path.exists("/kaggle/working"):
        return "kaggle"
    else:
        return "local"


def abspath(filename="", rdir=None, create_dir=True):
    if rdir is None:
        rdir = os.path.dirname(__file__) + f"/../../../bulkhours/"

    if create_dir and not os.path.exists(directory := os.path.dirname(rdir + filename)):
        os.system(f"mkdir -p {directory}")

    return os.path.abspath(rdir + filename)


def update_config(config):
    data = config.data if hasattr(config, "data") else config

    with open(abspath(".safe"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return config


def html(label, size="4", color="black", use_ipywidgets=False, display=False, style="raw", font="FiraCode Nerd Font"):
    if style in ["header", "title"]:
        html_code = f"<b><font face='{font}' size=4 color='{color}'>{label}<font></b><br/>"
    elif style == "rheader":
        html_code = f"<b><font face='{font}' size=4 color='red'>{label}<font></b><br/>"
    elif style == "bheader":
        html_code = f"<b><font face='{font}' size=4 color='black'>{label}<font></b><br/>"
    elif style == "raw":
        html_code = label
    else:
        html_code = f"<b><font face='{font}' size={size} color='{color}'>{label}<font></b><br/>"

    # TODO: ipywidgets.HTML DISPLAY is BUGGY, use IPython.display.HTML when possible
    w = ipywidgets.HTML(value=html_code) if use_ipywidgets else IPython.display.HTML(html_code)
    if display:
        print(" ", end="")
        IPython.display.display(w)
    else:
        return w


def code(codebody, raw=False, display=False):
    if raw:
        print(codebody)
    elif codebody and len(codebody) > 1:
        if "g++" in codebody:
            language = "cpp"
        if "nvcc" in codebody:
            language = "cuda"
        else:
            language = "python"
        w = IPython.display.Code(codebody, language=language)
        if display:
            IPython.display.display(w)
        else:
            return w


def md(mdbody=None, header=None, rawbody=None, codebody=None, hc="red", bc="black", icon="📚"):
    if header:
        html(header + "" + icon, size="4", color=hc, display=True)

    if mdbody and (type(mdbody) in [int, float, str] or len(mdbody) > 1):
        html(mdbody, size="4", color=bc, display=True)
    if rawbody and len(rawbody) > 1:
        code(rawbody, raw=True, display=True)

    if codebody and len(codebody) > 1:
        code(codebody, raw=False, display=True)


def eval_code(code):
    try:
        from IPython import get_ipython

        return get_ipython().run_cell(code)

    except ImportError:
        return exec(code)
    except AttributeError:
        return exec(code)


def get_config(config=None, do_update=False, from_scratch=False, is_namespace=False, is_new_format=False, **kwargs):
    """Important to copy the config"""
    if config is None:
        config = {}  # Config()
        if os.path.exists(jsonfile := abspath(".safe")) and not from_scratch:
            with open(jsonfile) as json_file:
                config.update(json.load(json_file))

    # Convert from Namespace
    if type(config) != dict:
        config = vars(config)

    config.update(kwargs)
    if "email" in config:
        config["email"] = config["email"].lower()

    if do_update:
        with open(abspath(".safe"), "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)

    if is_namespace:
        return Namespace(**config)
    if is_new_format:
        return Config(config)

    return config


def get_value(key, config=None):
    if config is None:
        config = get_config()
    # return config.get(key)
    if key in config:
        return config.get(key)
    return config["global"].get(key)


def is_admin(config=None):
    if config is None:
        config = get_config()

    if "is_demo_admin" in config and config["is_demo_admin"]:
        return True
    return (
        "admin_token" in config["global"]
        and "admins" in config["global"]
        and config["email"] in config["global"]["admins"]
    )
