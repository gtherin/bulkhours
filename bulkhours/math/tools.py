import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fractions import Fraction


def md(data, style="raw"):
    import IPython

    if style == "header":
        data = r"<font size='+3'>%s</font>" % (data)

    IPython.display.display(IPython.display.Markdown(r"%s" % data))

def html(data):
    import IPython
    IPython.display.display(IPython.display.HTML(r"%s" % data))
