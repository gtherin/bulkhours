import os
import json
import ipywidgets
import IPython
from argparse import Namespace
from .config import Config


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


def html2(label, display=True, style="raw"):
    import IPython

    if style == "title":
        data = IPython.display.HTML(f"<b><font face='FiraCode Nerd Font' size=6 color='black'>{label}<font></b>")
    else:
        data = IPython.display.HTML(label)
    if display:
        IPython.display.display(data)


def html(label, size="4", color="black", layout=None):
    return ipywidgets.HTML(
        value=f"<b><font face='FiraCode Nerd Font' size={size} color='{color}'>{label}<font></b>",
        layout=ipywidgets.Layout(height="auto", width="auto") if layout is None else layout,
    )


def md(mdbody=None, header=None, rawbody=None, codebody=None, hc="red", bc="black", icon="📚"):
    print("")
    if header:
        IPython.display.display(html(header + "" + icon, size="4", color=hc))

    if mdbody and (type(mdbody) in [int, float] or len(mdbody) > 1):
        IPython.display.display(html(mdbody, size="4", color=bc))
    if rawbody and len(rawbody) > 1:
        print(rawbody)
    if codebody and len(codebody) > 1:
        if "g++" in codebody:
            language = "cpp"
        if "nvcc" in codebody:
            language = "cuda"
        else:
            language = "python"
        IPython.display.display(IPython.display.Code(codebody, language=language))


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
