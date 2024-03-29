
import numpy as np
import matplotlib.pyplot as plt
from .poly1r import Poly1dr
from .math_table import MathTable
from .. import core

def solution_exo1(f, title, xmin, xmax, fprime, titleprime, 
                  ymin=None, ymax=None, xy_eqscale=False, show_line=False, show_tangent=False, show_fprime=False,
                  is_exo1=True, tanx=1, color="blue", return_ax=False):
    x = np.linspace(xmin, xmax, 100)

    color = core.c.get(color)

    fig, ax = plt.subplots()#figsize=(5, 5))
    ax.plot(x, f(x), label=title, color=color)

    if is_exo1:
        A, B = [1, f(1)], [2, f(2)]
        d = Poly1dr.from_points(A[0], A[1], B[0], B[1], numbers="fraction")
        if show_line:
            ax.plot(x, d.f(x), label=r"Droite$_{AB}(x)=%.2f x + %.2f$" % (d.a, d.b))
        ax.plot([1], [f(1)], "X", markersize=15, label="$A(1, %.2f)$" % f(1))
        ax.plot([2], [f(2)], "X", markersize=15, label="$B(2, %.2f)$" % f(2))


    if ymax is not None:
      ax.set_ylim([ymin, ymax])

    ymin, ymax = ax.get_ylim()
    ymin, ymax = np.round(ymin), np.round(ymax)

    if show_tangent:
        ax.set_title("%s (%s)" % (title, titleprime))
        if show_fprime:
            ax.plot(x, fprime(x), label=titleprime)
        t = Poly1dr.from_tangent(tanx, f(tanx), fprime, numbers="fraction")
        ax.plot(x, t.f(x), label=r"Tangente$_{A}(x)=%.2f x + %.2f$" % (t.a, t.b), ls="dotted")
    else:
        ax.set_title(title)

    ax.set_xticks(np.arange(xmin, xmax, 1))
    ax.set_yticks(np.arange(ymin, ymax, 1))
    if xy_eqscale:
        ax.set_aspect('equal', adjustable='box')
    ax.legend()

    if return_ax:
        return ax


def solution_table1(light=True, hide=None):
    if light:
        mt = MathTable(header=[r"Fonction $f(x)$", "Dérivée $f'(x)$"])

        def push_row(r, func, dfunc, defi="∀x", der="\mathbb{R}"):
            mt.push("$%s$" % func)
            if hide < r+1:
                mt.push("$(%s)'=?$" % (func))
            else:
                mt.push("$(%s)'=%s$" % (func, dfunc))
    else:
        mt = MathTable(header=[r"Fonction $f(x)$", "Définition", "Dérivabilité", "Dérivée $f'(x)$", "Notation différentielle", "Différentielle"],
                                    col_width=[1, 1, 1, 1, 10, 10])

        def push_row(r, func, dfunc, defi="∀x", der="\mathbb{R}"):
            mt.push("$%s$" % func)
            if hide < r+1:
                mt.push("?")
                mt.push("?")
                mt.push("$(%s)'=?$" % (func))
                mt.push("$\\frac{d(%s)}{dx}=?$" % (func))
                mt.push("$d(%s)=?$" % (func))
            else:
                mt.push("$%s$" % defi)
                mt.push("$%s$" % der)
                mt.push("$(%s)'=%s$" % (func, dfunc))
                mt.push("$\\frac{d(%s)}{dx}=%s$" % (func, dfunc))
                mt.push("$d(%s)=%s \cdot dx$" % (func, dfunc))


    push_row(0, "k", "0")
    push_row(1, "x", "1")
    push_row(2, "x^2", "2x")
    push_row(3, "x^n", "nx^{n-1}", defi="∀x, n\in\mathbb{R}", der="\mathbb{R}^{+*}")
    push_row(4, "\sqrt{x}", "\\frac{1}{2\sqrt{x}}", defi="x ≥ 0", der="\mathbb{R}^{+}")
    push_row(5, "\\frac{1}{x}", "-\\frac{1}{x^2}", defi="x \\neq 0", der="\mathbb{R}^{*}")
    push_row(6, "e^x", "e^x")
    push_row(7, "\\ln(x)", "\\frac{1}{x}", defi="x > 0", der="\mathbb{R}^{+*}")
    push_row(8, "\cos(x)", "-\sin(x)")
    push_row(9, "\sin(x)", "\cos(x)")

    mt.to_markdown(display=True)


def solution_table2(light=True, hide=None):

    if light:
        mt = MathTable(header=[r"Fonction $f(x)$", "Dérivée $f'(x)$"])

        def push_row(r, func, dfunc):
            mt.push("$%s$" % func)
            if hide < r+1:
                mt.push("$(%s)'=?$" % (func))
            else:
                mt.push("$(%s)'=%s$" % (func, dfunc))
    else:
        mt = MathTable(header=[r"Fonction $f(x)$", "Dérivée $f'(x)$", "Notation différentielle", "Différentielle"], col_width=15)

        def push_row(r, func, dfunc):
            mt.push("$%s$" % func)
            if hide < r+1:
                mt.push("$(%s)'=?$" % (func))
                mt.push("$\\frac{d(%s)}{dx}=?$" % (func))
                mt.push("$d(%s)=?$" % (func))
            else:
                mt.push("$(%s)'=%s$" % (func, dfunc))
                mt.push("$\\frac{d(%s)}{dx}=%s$" % (func, dfunc))
                mt.push("$d(%s)=(%s) \cdot dx$" % (func, dfunc))


    push_row(0, "k\cdot u", "k\cdot u'")
    push_row(1, "u+v", "u'+v'")
    push_row(2, "u\cdot v", "u'\cdot v + u\cdot v'")
    push_row(3, "\\frac{u}{v}", "\\frac{u'\cdot v - u\cdot v'}{v^2}")
    push_row(4, "u^n", "nu'u^{n-1}")

    mt.to_markdown(display=True)


def solution_table3(light=True, hide=None):

    if light:
        mt = MathTable(header=[r"Fonction $f(x)$", "Dérivée $f'(x)$"])

        def push_row(r, func, dfunc):
            mt.push("$%s$" % func)
            if hide < r+1:
                mt.push("$(%s)'=?$" % (func))
            else:
                mt.push("$(%s)'=%s$" % (func, dfunc))
    else:
        mt = MathTable(header=[r"Fonction composée", "Dérivée", "Notation différentielle"], col_width=15)

        def push_row(r, func, dfunc):
            mt.push("$%s$" % func)
            if hide < r+1:
                mt.push("$(%s)'=?$" % (func))
                mt.push("$\\frac{d(%s)}{dx}=?$" % (func))
            else:
                mt.push("$(%s)'=%s$" % (func, dfunc))
                mt.push("$\\frac{d(%s)}{dx}=%s$" % (func, dfunc))


    push_row(0, "f \circ u(x)", "(f' \circ u(x)) \cdot u'(x))")
    push_row(1, "\cos(u(x))", "-u'\sin(u)")
    push_row(2, "\sin(u(x))", "u'\cos(u)")
    push_row(3, "e^{u(x)}", "u'e^{u}")
    push_row(4, "\ln(u(x))", "\\frac{u'}{u}")
    push_row(5, "f(g(h(x)))", "f'(g(h(x))) \cdot g'(h(x)) \cdot h'(x)")

    mt.to_markdown(display=True)


