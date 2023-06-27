import os
import json
import ipywidgets
import IPython


def abspath(filename=""):
    rdir = os.path.dirname(__file__) + f"/../../../bulkhours"
    for f in ["", rdir + "/"]:
        if os.path.exists(f + filename):
            return os.path.abspath(f + filename)


def update_config(data):
    with open(abspath(".safe"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


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


def copy_config(e="", config={}, do_update=False, from_scratch=False, is_namespace=False, **kwargs):
    from argparse import Namespace

    """Important to copy the config"""
    if config == {}:
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

    return config


def get_config(*kargs, **kwargs):
    return copy_config(*kargs, **kwargs)


def get_value(key, e=""):
    return get_config(e=e).get(key)


def is_admin(config=None):
    if config is None:
        config = get_config()
    return (
        "admin_token" in config["global"]
        and "admins" in config["global"]
        and config["email"] in config["global"]["admins"]
    )
