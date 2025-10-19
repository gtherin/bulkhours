import pandas as pd
import IPython


class MathTable:
    def __init__(self, header=None, col_width=15):
        self.header = header
        if type(header) == list:
            self.cols = len(header)
            self.has_header = True
        elif type(header) == int:
            self.cols = header
            self.has_header = False
        else:
            raise ValueError("header must be a list or an integer")

        self.col_width = col_width
        self.index, self.header = -1, header
        self.data = pd.DataFrame([["$e^0 =1$"] * self.cols])

    def push(self, val):
        self.index += 1
        col = self.index % self.cols
        row = self.index // self.cols
        self.data.loc[row, col] = val

    def to_markdown(self, size=3, display=False):
        header = ""
        for col in range(self.cols):
            label = self.header[col] if type(self.header) == list else ""
            xtra_col_width = (
                " &nbsp; " * self.col_width[col] if type(self.col_width) == list else " &nbsp; " * self.col_width
            )
            header += "|%s %s" % (label, xtra_col_width)
        header += "|\n" + ":---:".join(["|"] * (self.cols + 1))
        md = "\n"

        for row in range(len(self.data)):
            md += "| "
            for col in range(self.cols):
                md += r"<font size = '%s'>$%s$</font> | " % (size, self.data.loc[row, col])
            md += "\n"

        md = "\n\n%s%s\n" % (header, md)

        if display:
            IPython.display.display(IPython.display.Markdown(md))
        else:
            return md

    def to_latex(self, size=4, display=False):
        sizes = {1: r"\small", 2: r"\normalsize", 3: r"\large", 4: r"\Large", 5: r"\LARGE", 6: r"\huge"}

        md = r"""{%s \displaystyle \\
  \begin{array}{%s}
  \hline \\
""" % (
            sizes[size],
            "c".join(["|"] * (self.cols + 1)),
        )

        if self.header is not None:
            for col in range(self.cols):
                md += r"%s & " % (self.header[col])
            md = md[:-2]
            md += r" \\ \hline  " + "\n"

        for row in range(len(self.data)):
            md += ""
            for col in range(self.cols):
                md += r"%s & " % (self.data.loc[row, col].replace("$", ""))
            md = md[:-2]
            md += r" \\ \hline  " + "\n"

        md += r"\end{array}\\ " + "\n}"

        if display:
            IPython.display.display(IPython.display.Math(md))
        else:
            return md
