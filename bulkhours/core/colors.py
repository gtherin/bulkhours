import matplotlib.colors as mcolors


def colors(cmap):
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
