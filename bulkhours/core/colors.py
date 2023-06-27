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
    IPython.display.display(ipywidgets.HTML(style))
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
