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

    def to_markdown(self, size=4):
        md = "|" * (self.cols + 1)
        md += "\n"
        md += (
            ":-------------------------------------------------------------------------------------------------".join(
                ["|"] * (self.cols + 1)
            )
        )
        md += "\n"

        for col in range(self.cols):
            md += "| "
            for row in range(self.rows):
                md += r"<font size = '%s'>%s</font> | " % (size, self.data.loc[row, col])
            md += "\n"

        return "\n\n%s\n" % (md)
