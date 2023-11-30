import os
from .. import core


def mount_gdrive():
    # Mount google drive if needed
    if os.path.exists("/content/gdrive"):
        return

    from google.colab import drive

    drive.mount("/content/gdrive/")


def nevaluate(filename, force=False, fake=False):
    import IPython
    from subprocess import getoutput
    import nbformat

    # Get student reference notebook

    # Mount google drive if needed
    if "/content/gdrive" in filename:
        mount_gdrive()

    email, notebook_id, database = None, None, None
    # Parse notebook
    nb = nbformat.read(filename, nbformat.NO_CONVERT).copy()
    for idx, cell in enumerate(nb.cells):
        if cell["cell_type"] != "code":
            continue
        source = cell["source"].split("\n")
        is_it_an_evaluation_cell = source[0].startswith(
            "%%evaluation_cell_id "
        ) or source[0].startswith("%evaluation_cell_id ")

        # Parameters search
        psearch = cell["source"].replace(" ", "")

        # Change the initialization cell
        if "email=" in psearch or "notebook_id=" in psearch:
            for s in psearch.split("\n"):
                if "email=" in s and email is None:
                    email = s[s.find("email=") :].replace("'", '"').split('"')[1]
                if "notebook_id=" in s and notebook_id is None:
                    notebook_id = (
                        s[s.find("notebook_id=") :].replace("'", '"').split('"')[1]
                    )
                if "database=" in s and notebook_id is None:
                    database = s[s.find("database=") :].replace("'", '"').split('"')[1]
                    info = core.installer.get_tokens(database)

            IPython.display.display(
                IPython.display.Markdown(
                    f"""#### Parsing '`{filename.split('/')[-1]}`': '`{info['virtual_room']}/{notebook_id}/{email}`'"""
                )
            )

        if not is_it_an_evaluation_cell:
            continue

        cinfo = core.LineParser(source[0], cell["source"])

        cinfo.user, cinfo.notebook_id, cinfo.virtual_room = (
            email,
            notebook_id,
            info["virtual_room"],
        )
        parsed_cell = core.cell_parser.CellParser.crunch_data(
            cinfo=cinfo, user=email, data=cell["source"]
        )

        answer = core.firebase.get_solution_from_corrector(
            cinfo.cell_id, corrector=email, cinfo=cinfo
        )
        if answer is None or force:
            core.firebase.send_answer_to_corrector(
                cinfo,
                force=True,
                fake=fake,
                last_version="teacher",
                **parsed_cell.get_dbcell_decomposition(),
            )
