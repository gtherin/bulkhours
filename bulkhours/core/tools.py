import os
import json


def md(mdbody=None, header=None, rawbody=None, codebody=None, hc="red", bc="black", icon="📚"):
    import IPython

    print("")
    if header:
        IPython.display.display(
            IPython.display.Markdown(
                f"<b><font face='FiraCode Nerd Font' size=4 color='{hc}'>{header} {icon}:<font></b>"
            )
        )

    if mdbody and (type(mdbody) in [int, float] or len(mdbody) > 1):
        IPython.display.display(
            IPython.display.Markdown(f"<font face='FiraCode Nerd Font' size=4 color='{bc}'>{mdbody}<font>")
        )
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


def get_config():
    jsonfile = os.path.dirname(__file__) + "/../../.safe"
    if os.path.exists(jsonfile):
        with open(jsonfile) as json_file:
            return json.load(json_file)

    return {}


def get_value(key):
    return get_config().get(key)


def is_premium(mtoken="NO_TOKEN", verbose=False):
    if mtoken == "NO_TOKEN":
        return False
    try:
        import bulkhours_premium

        return True
    except ImportError:
        if verbose:
            print("bulkhours_premium not installed")
        return False
