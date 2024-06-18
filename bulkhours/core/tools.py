import os
import json
import ipywidgets
import IPython
from pathlib import Path
from argparse import Namespace
from .config import Config

REF_USER = "solution@bulkhours.fr"


def safe(ext=False):

    # TODO: Create a unique key with email and notebookid, to avoid usage collisions
    # Might be solved by a unique token per notebook
    #data = "tester@bulkhours.fr_flops"
    #ukey = b64e(zlib.compress(data.encode("utf-8"), 1)).decode("utf-8")

    ukey = ""

    filename = f".safe{ukey}.pyc" if ext else f".safe{ukey}"
    return abspath(filename)


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
        Path(directory).mkdir(parents=True, exist_ok=True)

    return os.path.abspath(rdir + filename)


def update_config(cfg):
    data = cfg.data if hasattr(cfg, "data") else cfg

    with open(safe(), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return cfg


def html(
    label,
    size="4",
    color="black",
    use_ipywidgets=False,
    display=False,
    style="raw",
    font="FiraCode Nerd Font",
):
    if style in ["header", "title"]:
        html_code = (
            f"<b><font face='{font}' size=4 color='{color}'>{label}<font></b><br/>"
        )
    elif style == "rheader":
        html_code = f"<b><font face='{font}' size=4 color='red'>{label}<font></b><br/>"
    elif style == "bheader":
        html_code = (
            f"<b><font face='{font}' size=4 color='black'>{label}<font></b><br/>"
        )
    elif style == "raw":
        html_code = label
    else:
        html_code = (
            f"<b><font face='{font}' size={size} color='{color}'>{label}<font></b><br/>"
        )

    # TODO: ipywidgets.HTML DISPLAY is BUGGY, use IPython.display.HTML when possible
    w = (
        ipywidgets.HTML(value=html_code)
        if use_ipywidgets
        else IPython.display.HTML(html_code)
    )
    if display:
        print(" ", end="")
        IPython.display.display(w)
    else:
        return w


def code(codebody, raw=False, display=False, style=None):
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
        if style is not None:
            import pygments

            available_styles = list(pygments.styles.get_all_styles())

            if style not in available_styles:
                print(f"Style is unknown. Available styles: {available_styles}")
            w = IPython.display.HTML(
                pygments.highlight(
                    codebody,
                    pygments.lexers.PythonLexer(),
                    pygments.formatters.HtmlFormatter(full=True, style=style),
                )
            )
        if display:
            IPython.display.display(w)
        else:
            return w


def dmd(*args, **kwargs):
    import IPython

    if IPython.get_ipython():
        IPython.display.display(IPython.display.Markdown(*args, **kwargs))
    else:
        print(args[0])


def md(
    mdbody=None,
    header=None,
    rawbody=None,
    codebody=None,
    hc="red",
    bc="black",
    icon="📚",
):
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


def get_config(config=None, is_new_format=False, **kwargs):
    if config is None:
        if os.path.exists(jsonfile := safe()):
            with open(jsonfile) as json_file:
                return Config(json.load(json_file))

    return config


def get_value(key, config=None):
    if config is None:
        config = get_config()
    if key is None:
        return None
    if key in config:
        return config.get(key)
    if type(config) == dict:
        return config["global"].get(key)
    else:
        return config.g.get(key)


def is_admin(cfg=None):
    if cfg is None:
        cfg = get_config(is_new_format=True)
    if cfg is None:
        return False
    
    data = cfg if type(cfg) == dict else cfg.data
    return "global" in data and "admins" in data["global"] and data["email"] in data["global"]["admins"]


def format_opt(label, raw2norm=True):
    rr = {"-": "__minus__", "@": "__at__", " ": "__space__", "/": "__slash__"}
    if type(label) == str and len(label) > 0 and label[0] != "-":
        for k, v in rr.items():
            label = label.replace(k, v) if raw2norm else label.replace(v, k)
    return label


def install_if_needed(package):
    try:
        import importlib

        return importlib.import_module(package)

    except ModuleNotFoundError:

        if package == "mariadb":
            os.system("sudo apt-get install -y libmariadb3 libmariadb-dev > /dev/null 2>&1")

        os.system(f"pip install {package} > /dev/null 2>&1")
        print(f"\x1b[37mpip install {package}\x1b[0m")
        import importlib

        return importlib.import_module(package)


def black_format_str(code, line_length=500):
    black = install_if_needed("black")
    if code.startswith("%%evaluation_cell_id"):
        code = code[code.find("\n") :]

    try:
        return black.format_str(code, mode=black.Mode(line_length=line_length))
    except:
        return code
