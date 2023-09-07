import pandas as pd


class MathTable:
    def __init__(self, rows, cols):
        self.rows, self.cols = rows, cols
        self.data = [["<font size = '2'>$e^0 =1$</font>"] * self.cols] * self.rows
        self.data = pd.DataFrame(self.data)
        self.crow, self.ccol = 0, -1

    def increment_cursor(self):
        self.ccol += 1
        if self.ccol >= self.cols - 1:
            self.crow += 1
            self.ccol = 0

    def push(self, val):
        self.increment_cursor()
        self.add(self.crow, self.ccol, val)

    def add(self, row, col, val):
        self.crow, self.ccol = row, col
        self.data.loc[row, col] = val

    def to_markdown(self, size=4, display=False):
        header = "|" * (self.cols + 1) + "\n" + (":---:".join(["|"] * (self.cols + 1)))

        md = "\n"

        for row in range(self.rows):
            md += "| "
            for col in range(self.cols):
                md += r"<font size = '%s'>$%s$</font> | " % (size, self.data.loc[row, col])
            md += "\n"

        md = "\n\n%s%s\n" % (header, md)

        import IPython

        if display:
            IPython.display.display(IPython.display.Markdown(md))
        else:
            return md

    def to_latex(self, size=4, display=False):
        sizes = {1: "\small", 2: "\normalsize", 3: "\large", 4: "\Large", 5: "\LARGE", 6: "\huge"}

        md = """{%s \displaystyle \\\\
  \\begin{array}{%s}
  \hline \\\\
""" % (
            sizes[size],
            "c".join(["|"] * (self.cols + 1)),
        )

        for row in range(self.rows):
            md += ""
            for col in range(self.cols):
                md += r"%s & " % (self.data.loc[row, col].replace("$", ""))
            md = md[:-2]
            md += " \\\\ \\\\ \hline  \n"

        md += "\end{array}\\\\ \n}"
        import IPython

        if display:
            IPython.display.display(IPython.display.Math(md))
        else:
            return md
