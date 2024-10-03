import bulkhours


def check_format(argv):
    argv = argv.split()
    print(argv)
    print(opts := bulkhours.core.line_parser.format_opts(argv))
    print([bulkhours.core.tools.format_opt(v, raw2norm=False) for v in opts])


def test_line_parser():
    check_format("-i cell_id -c Salut les gars")
    check_format("-i kinit")

    """This function merges arguments together
Example:
-i cell_d -c Salut les gars
"""

    cell_content = """%%evaluation_cell_id -i synthetic

# 5. Comment
"""
    # Remove xtra functions

    cinfo = bulkhours.core.LineParser(cell_content.split("\n")[0], cell_content)
    print(cinfo.cell_id)

