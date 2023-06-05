import os
import json
import ipywidgets


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


def is_french(in_french=None):
    if in_french is None:
        return "fr" == os.environ["BLK_LANGUAGE"]

    return "fr" == in_french


def get_config():
    jsonfile = os.path.dirname(__file__) + "/../../.safe"
    if os.path.exists(jsonfile):
        with open(jsonfile) as json_file:
            return json.load(json_file)

    return {}


def get_value(key):
    return get_config().get(key)


def is_premium(premium_token="NO_TOKEN"):
    import bulkhours_premium

    return True
    if premium_token == "NO_TOKEN" and get_value("premium_token") is None:
        return False

    try:
        import bulkhours_premium

        return True
    except ImportError:
        return False


def is_admin(admin_token="NO_TOKEN"):
    import bulkhours_admin

    return True
    if admin_token == "NO_TOKEN" and get_value("admin_token") is None:
        return False

    try:
        import bulkhours_admin

        return True
    except ImportError:
        return False
