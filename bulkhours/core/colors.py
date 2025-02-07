purple = "#581845"
red = "#C70039"
orange = "#FF5733"
blue = "#0097B2"
green = "#52DE97"
yellow = "#FBE555"
dblue = "#053061"
lpink = "#FAACB5"
black = "black"
dpink = "#924A5F"

bmaps = [
    ["purple", "red", "orange", "blue", "green", "yellow", "dblue", "lpink", "black", "dpink"],
    [purple, red, orange, blue, green, yellow, dblue, lpink, black, dpink]
]

caliases = dict(zip(bmaps[0], bmaps[1]))


def get(color):
    if type(color) == str:
        return caliases[color] if color in caliases else color
    if type(color)==int:
        return bmaps[1][color%len(bmaps)-1]
    raise Exception("Type is not taken in charge")


def get_mpf_style():
    import mplfinance as mpf
    return mpf.make_mpf_style(
        marketcolors=mpf.make_marketcolors(
            up=green, down=red, edge='inherit', wick='black', volume='in', ohlc='i', inherit=True
            ), mavcolors=[purple, orange, blue, lpink, dpink], base_mpf_style='charles')


def vizualize(colors=None, ncols=4):
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    import math

    if colors is None:
        colors = caliases
    cell_width, cell_height, swatch_width, margin, dpi = 212, 22, 48, 12, 72
    nrows = math.ceil(len(colors) / ncols)
    width, height = cell_width * 4 + 2 * margin, cell_height * nrows + 2 * margin

    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)
    fig.subplots_adjust(
        margin / width,
        margin / height,
        (width - margin) / width,
        (height - margin) / height,
    )
    ax.set_xlim(0, cell_width * 4)
    ax.set_ylim(cell_height * (nrows - 0.5), -cell_height / 2.0)
    ax.set_axis_off()

    for i, name in enumerate(list(caliases.keys())):
        row, col = i % nrows, i // nrows
        ax.text(cell_width * col + swatch_width + 7, row * cell_height, name)
        ax.add_patch(
            Rectangle(
                xy=(cell_width * col, row * cell_height - 9),
                width=swatch_width,
                height=18,
                facecolor=colors[name],
            )
        )


def color_maps(cmap):
    import matplotlib.colors as mcolors

    if cmap == "b":
        return list(mcolors.BASE_COLORS.values())
    elif cmap == "c":
        return list(mcolors.CSS4_COLORS.values())
    elif cmap == "t":
        return list(mcolors.TABLEAU_COLORS.values())
    elif cmap == "x":
        return list(mcolors.XKCD_COLORS.values())
    else:
        return list(caliases.values())


# Define shortcuts to color maps
# example bulkhours.c.x gives you xkcd colors wheel
g = lambda i: color_maps("d")[i % len(color_maps("d"))]
bg = lambda i: color_maps("b")[i % len(color_maps("b"))]
cg = lambda i: color_maps("c")[i % len(color_maps("c"))]
tg = lambda i: color_maps("t")[i % len(color_maps("t"))]
xg = lambda i: color_maps("x")[i % len(color_maps("x"))]


def set_style(object, style):
    import IPython

    style = """<style>
            .sol_background {background-color:#f7d1d1}
            .cell_background {background-color:#F7F7F7}
            .cell_border {background-color:#CFCFCF}

buttonb {
   border: none;
   color: red;
   font-weight: bolder;
   padding: 20px;
   font-size: 18px;
   cursor: pointer;
   border-radius: 6px;
}
.button3 {background-color:#eaeaea}
.button1 {background-color:#eaeaea ; color:red ; font-size:100% ; border: 1px solid #eaeaea}
.button2 {background-color:#eaeaea ; color:red}
        </style>
    """
    IPython.display.display(IPython.display.HTML(style))
    object.add_class(style)


#    vvvv vvvv-- the code from above
BORANGE = "\x1b[33m\x1b[1m"
BDGRAY = "\x1b[30m\x1b[1m"
HSTYLE = BDGRAY
NC = "\x1b[m"  # No Color
st = lambda x: f"{HSTYLE}{x}{NC}"


def set_plt_style(style="default", cmap="default"):
    import matplotlib.pyplot as plt
    from cycler import cycler

    background_color = "#F0FDFA11"

    if style == "math":
        axis_color = caliases["orange"]
        plt.rcParams["grid.color"] = axis_color
        plt.rcParams["grid.linestyle"] = ":"
        plt.rcParams["grid.linewidth"] = 0.8
        plt.rcParams["lines.linewidth"] = 3
        plt.rcParams["font.size"] = 10
    elif style == "zeer":
        axis_color = "white"
    else:
        axis_color = caliases["blue"]
        plt.rcParams["grid.color"] = "white"
        plt.rcParams["lines.linewidth"] = 4
        plt.rcParams["font.size"] = 14

    plt.rcParams["axes.grid"] = True
    plt.rcParams["axes.edgecolor"] = axis_color
    plt.rcParams["axes.labelcolor"] = axis_color
    plt.rcParams["axes.titlecolor"] = axis_color
    plt.rcParams["figure.edgecolor"] = axis_color
    plt.rcParams["xtick.color"] = axis_color
    plt.rcParams["ytick.color"] = axis_color

    plt.rcParams["axes.facecolor"] = background_color
    plt.rcParams["figure.facecolor"] = background_color
    plt.rcParams["legend.facecolor"] = background_color
    plt.rcParams["legend.edgecolor"] = background_color

    plt.rcParams["axes.prop_cycle"] = cycler(color=color_maps(cmap))


def get_html_buttons_styles_code():
    return """
    <style>
    body {
    .button {
    align-items: flex-start;
    appearance: button;
    border-bottom-color: rgb(255, 255, 255);
    border-bottom-style: none;
    border-bottom-width: 0px
    border-image-outset: 0;
    border-image-repeat: stretch;
    border-image-slice: 100%;
    border-image-source: none;
    border-image-width: 1;
    border-left-color: rgb(255, 255, 255);
    border-left-style: none;
    border-left-width: 0px;
    border-right-color: rgb(255, 255, 255);
    border-right-style: none;
    border-right-width: 0px;
    border-top-color: rgb(255, 255, 255);
    border-top-style: none;
    border-top-width: 0px;
    box-shadow: none;
    box-sizing: border-box;
    color: rgb(255, 255, 255);
    cursor: pointer;
    display: inline-block;
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-feature-settings: normal;
    font-kerning: auto;
    font-optical-sizing: auto;
    font-size: 13px;
    font-stretch: 100%;
    font-style: normal;
    font-variant-alternates: normal;
    font-variant-caps: normal;
    font-variant-east-asian: normal;
    font-variant-ligatures: normal;
    font-variant-numeric: normal;
    font-variation-settings: normal;
    font-weight: 400;
    height: 28px;
    letter-spacing: normal;
    line-height: 28px;
    margin-bottom: 2px;
    margin-left: 2px;
    margin-right: 2px;
    margin-top: 2px;
    overflow-x: hidden;
    overflow-y: hidden;
    padding-block-end: 0px;
    padding-block-start: 0px;
    padding-bottom: 0px;
    padding-inline-end: 10px;
    padding-inline-start: 10px;
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 0px;
    position: relative;
    text-align: center;
    text-indent: 0px;
    text-overflow: ellipsis;
    text-rendering: auto;
    text-shadow: none;
    text-size-adjust: 100%;
    text-transform: none;
    text-wrap: nowrap;
    user-select: none;
    white-space-collapse: collapse;
    width: 148px;
    word-spacing: 0px;
    writing-mode: horizontal-tb;
    -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
    -webkit-border-image: none;
    }

    .button.bk_primary{
    background-color: rgb(33, 150, 243);
    }
    .button.bk_secondary{
    background-color:#6C757D;
    }
    .button.bk_success{
    background-color:#28A745;
    }
    .button.bk_danger{
    background-color:#DC3545;
    }
    .button.bk_warning{
    background-color:#FFC107;
    color: #212529;
    }
    .button.bk_info{
    background-color:#17A2B8;
    }
    .button.bk_light{
    background-color:#F8F9FA;
    color: #212529;
    }
    .button.bk_dark{
    background-color:#343A40;
    }
    .button.bk_link{
    background-color:#FFFFFF;
    color: #1D8AFF;
    }
    </style>"""


def set_html_buttons_styles():
    import IPython

    html_buttons_styles = (
        f"""<html><head>{get_html_buttons_styles_code()}</head></html>"""
    )
    IPython.display.display(IPython.display.HTML(html_buttons_styles))


def get_mpf_style(base_mpf_style='charles'):
    import mplfinance as mpf
    
    return mpf.make_mpf_style(
        marketcolors=mpf.make_marketcolors(
            up='#52DE97',down='#C70039', edge='inherit', wick='black', volume='in', ohlc='i', inherit=True
            ), mavcolors=['#581845', '#FF5733', '#0097B2', "#FAACB5", "#924A5F"], base_mpf_style=base_mpf_style)
