def colors(cmap):
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
        return ["#581845", "#C70039", "#FF5733", "#4F77AA", "black"]


g = lambda i: colors("d")[i % len(colors("d"))]
bg = lambda i: colors("b")[i % len(colors("b"))]
cg = lambda i: colors("c")[i % len(colors("c"))]
tg = lambda i: colors("t")[i % len(colors("t"))]
xg = lambda i: colors("x")[i % len(colors("x"))]


def set_style(object, style):
    import IPython
    import ipywidgets

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


def set_plt_style():
    import matplotlib.pyplot as plt

    background_color = "#F0FDFA11"  # cdcdcd
    axis_color = "#4F77AA"  # cdcdcd

    def get_color(discipline):
        colors = {"swimming": "#581845", "cycling": "#C70039", "running": "#FF5733", "axis": "#4F77AA"}
        return colors[discipline] if discipline in colors else "black"

    plt.rcParams["axes.grid"] = True
    plt.rcParams["axes.edgecolor"] = axis_color
    plt.rcParams["axes.labelcolor"] = axis_color
    plt.rcParams["axes.titlecolor"] = axis_color
    plt.rcParams["axes.facecolor"] = background_color
    plt.rcParams["figure.edgecolor"] = axis_color
    plt.rcParams["figure.facecolor"] = background_color
    plt.rcParams["grid.color"] = "white"
    plt.rcParams["legend.facecolor"] = background_color
    plt.rcParams["legend.edgecolor"] = background_color
    plt.rcParams["xtick.color"] = axis_color
    plt.rcParams["ytick.color"] = axis_color

    plt.rcParams["font.size"] = 14
    plt.rcParams["lines.linewidth"] = 4

    # ax.grid(True, axis="y", color="white")

    from cycler import cycler

    # mpl.rcParams['axes.prop_cycle'] = cycler(color='bgrcmyk')
    plt.rcParams["axes.prop_cycle"] = cycler(
        color=[get_color(c) for c in ["swimming", "cycling", "running", "The end"]]
    )


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

    html_buttons_styles = f"""<html><head>{get_html_buttons_styles_code()}</head></html>"""
    IPython.display.display(IPython.display.HTML(html_buttons_styles))
