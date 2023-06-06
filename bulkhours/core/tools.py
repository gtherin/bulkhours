import os
import json
import ipywidgets
from argparse import Namespace

DEFAULT_TOKEN = "NO_TOKEN"


def html(label, size="4", color="black"):
    return ipywidgets.HTML(
        value=f"<b><font face='FiraCode Nerd Font' size={size} color='{color}'>{label}<font></b>",
        layout=ipywidgets.Layout(height="auto", width="auto"),
    )


def md(mdbody=None, header=None, rawbody=None, codebody=None, hc="red", bc="black", icon="📚"):
    import IPython

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
            language = None
        IPython.display.display(IPython.display.Code(codebody, language=language))


def get_json_file(e):
    return os.path.dirname(__file__) + f"/../../.safe{e}"


def get_config(e="", do_update=False, is_namespace=False, **kwargs):
    config = {}
    if e == "":
        config.update(get_config(e="p"))

    if os.path.exists(jsonfile := get_json_file(e)):
        with open(jsonfile) as json_file:
            config.update(json.load(json_file))

    config.update(kwargs)
    if "email" in config:
        config["email"] = config["email"].lower()

    if do_update:
        with open(jsonfile, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)

    if is_namespace:
        return Namespace(**config)

    return config


def get_value(key, e=""):
    return get_config(e=e).get(key)


def is_premium(debug=True):
    token = get_value("premium_token", e="p")

    if token is None:
        return False

    if debug:
        print("import bulkhours_premium")
        import bulkhours_premium

    try:
        import bulkhours_premium

        return True
    except ImportError:
        return False


def is_admin(debug=False):
    token = get_value("admin_token", e="p")
    if token is None:
        return False

    if debug:
        print("import bulkhours_admin")
        import bulkhours_admin

    try:
        import bulkhours_admin

        return True
    except ImportError:
        return False
