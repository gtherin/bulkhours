import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from . import tools
from .. import core


def get_abs_filename(filename):
    if "/content/gdrive" not in filename:
        return filename

    try:
        from xattr import xattr

    except ModuleNotFoundError:
        os.system("apt install xattr > /dev/null 2>&1")
        print("\x1b[37mapt install xattr\x1b[0m")
        from xattr import xattr

    return f"https://colab.research.google.com/drive/" + (
        xattr(filename).get("user.drive.id").decode()
    )


def mount_directory(mdir):
    # Mount google drive if needed
    if "/content/gdrive" in mdir:
        from google.colab import drive

        if not os.path.exists("/content/gdrive/"):
            drive.mount("/content/gdrive/")

    if not os.path.exists(mdir):
        os.system(f"mkdir -p {mdir}")


def copy4students(email, drive_rdir, filename, cfg=None, **kwargs):
    import IPython

    if cfg is None:
        cfg = core.tools.get_config(is_new_format=True)
    files = {}
    students_list = tools.get_users_list(cfg=cfg)

    IPython.display.display(
        IPython.display.Markdown(
            f"## Notebook generation '`{filename.split('/')[-1]}`'"
        )
    )

    for _, student in students_list.iterrows():
        if student["mail"] == "solution":
            continue
        cfilename = f"{drive_rdir}/{cfg.virtual_room}/{filename}".replace(
            ".", f"_%s." % student["auser"].lower()
        )
        files[student["mail"]] = copy(
            email,
            drive_rdir,
            filename,
            student["mail"],
            cfilename=cfilename,
            cfg=cfg,
            verbose=False,
            **kwargs,
        )
        icon = "❌" if "/local" in files[student["mail"]] else "🌍"
        core.tools.dmd(f"""* {icon} {student['auser']}, {files[student['mail']]}""")

    with open(
        cfilename := f"{drive_rdir}/{cfg.virtual_room}/notebooks.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(files, f, ensure_ascii=False, indent=4)

    # Get the summary file if in google drive
    dfilename = get_abs_filename(cfilename)
    core.tools.dmd(f"""### 🎓 Summary file: {cfilename}, {dfilename}""")

    return files


def copy(
    email,
    drive_rdir,
    filename,
    student,
    reset=True,
    debug=False,
    cfg=None,
    verbose=True,
    cfilename=None,
):
    import IPython
    import nbformat

    # Get student reference notebook
    if cfg is None:
        cfg = core.tools.get_config(is_new_format=True)
    ofilename = f"{drive_rdir}/{filename}"
    if cfilename is None:
        cfilename = f"{drive_rdir}/{cfg.virtual_room}/{filename}".replace(
            ".", f"_{cfg.virtual_room}." if reset else "_solution."
        )

    if verbose:
        IPython.display.display(
            IPython.display.Markdown(
                f"## Notebook generation '`{cfilename.split('/')[-1]}`'"
            )
        )

    # Mount directories
    mount_directory(drive_rdir)
    mount_directory(os.path.dirname(cfilename))

    # Get token
    ntoken = cfg.tokens[cfg.virtual_room]

    # Parse notebook
    to_pop, nb = [], nbformat.read(ofilename, nbformat.NO_CONVERT).copy()
    for idx, cell in enumerate(nb.cells):
        if cell["cell_type"] == "code":
            source = cell["source"].split("\n")
            is_it_an_evaluation_cell = source[0].startswith(
                "%%evaluation_cell_id "
            ) or source[0].startswith("%evaluation_cell_id ")

            # Change the initialization cell
            if "\ndatabase" in cell["source"] and not is_it_an_evaluation_cell:
                nsource = []
                for s in source:
                    if s.startswith("database"):
                        s = f'database = "{ntoken}"'
                    if s.startswith("email"):
                        s = s.replace(email, student)
                    nsource.append(s)
                cell["source"] = "\n".join(nsource)
                if "outputs" in cell and len(cell["outputs"]) > 0:
                    cell["outputs"][0]["text"] = ""
            # Remove cells with admin code
            elif "[admin]" in source[0]:
                to_pop.append(idx)
            # Remove cells with solution
            elif " -u solution" in source[0]:
                if reset:
                    to_pop.append(idx)
                else:  # is_solution
                    cell["source"] = cell["source"].replace(" -u solution", "")
            # Format cells with reset info
            elif " -u reset" in source[0]:
                if reset:
                    cell["source"] = cell["source"].replace(" -u reset", "")
                else:  # is_solution
                    to_pop.append(idx)
            elif is_it_an_evaluation_cell:
                cinfo = core.LineParser(source[0], cell["source"])
                parsed_cell = core.cell_parser.CellParser.crunch_data(
                    cinfo=cinfo, user=core.tools.REF_USER, data=cell["source"]
                )
                cell["source"] = (
                    parsed_cell.get_reset() if reset else parsed_cell.get_solution()
                )
                # cell["source"] = cell_reset(cell["source"]) if reset else cell_solution(cell["source"])
                if debug:
                    print(cell["outputs"])
                if reset:
                    cell["outputs"] = []
        if cell["cell_type"] == "markdown":
            source = cell["source"].split("\n")
            # Remove markdown cells with [admin in the first line]
            if "[admin]" in source[0]:
                to_pop.append(idx)

    # Remove listed cells
    if verbose:
        print("Pop the following cells: ", to_pop)
        for i in to_pop[::-1]:
            nb.cells.pop(i)

    # Create the new notebook
    nbformat.write(nb, cfilename, version=nbformat.NO_CONVERT)

    # Get the filename if in google drive
    dfilename = get_abs_filename(cfilename)

    # Print info
    if verbose:
        if "/local" in dfilename:
            core.tools.dmd(
                f"""* 🌍 ❌<b><font color="red">File has not been yet mounted on the cloud. Please rerun🔄</font></b>❌\n* 📁 '`{cfilename}`'\n
            """
            )
        else:
            core.tools.dmd(f"""* 🌍 {dfilename}\n* 📁 '`{cfilename}`'\n""")
    return dfilename


def prepare_mail(
    default_student="john.doe@bulkhours.eu",
    signature="The bulkHours team",
    generate_file=True,
    generate_solution=True,
    notebook_file=None,
    drive_rdir=None,
    cfg=None,
    debug=False,
):
    notebook_info = notebook_file.split(".")[0]
    if cfg is None:
        cfg = core.tools.get_config(is_new_format=True)

    if generate_solution:
        copy(
            signature,
            drive_rdir,
            notebook_file,
            default_student,
            reset=False,
            cfg=cfg,
            debug=debug,
        )

    if generate_file:
        dnotebook_file = copy(
            signature,
            drive_rdir,
            notebook_file,
            default_student,
            reset=True,
            cfg=cfg,
            debug=debug,
        )
    else:
        dnotebook_file = get_abs_filename(
            f"{drive_rdir}/{notebook_file}".replace(".", f"_{cfg.virtual_room}.")
        )

    if "/local" in dnotebook_file:
        return

    if "@" in signature:
        signature = signature.split("@")[0].replace(".", " ").title()

    import IPython

    title = f"Notebook of the day: {notebook_info}"
    intro = f"Dear all,<br/><br/>Here is the practical course of the day. Remember to write your email address to replace"
    end = f"Best regards"

    if cfg.language == "fr":
        title = f"Notebook du jour: {notebook_info}"
        intro = f"Bonjour à toutes et à tous,<br/><br/>Voici le lien vers le cours du jour.<br/>💡Rappelez-vous bien de mettre votre adresse mail à la place de"
        end = f"Cordialement"

    students = cfg.g[cfg.virtual_room].replace(default_student + ";", "")

    html = f"""
<html>
<head>
    <style> 
    table, th, td {{ border: 1px solid black; border-collapse: collapse; }} th, td {{ padding: 5px; }}
    </style>
</head>
<body>
    <h2>Mail to {cfg.virtual_room} students (in CCI)</h2>
    <p>{students}</p>
    <h2>Title of the mail:</h2><br/>
    <p>{title}</p>
    <h2>Content of the mail:</h2><br/>
    <p>{intro} <b>'{default_student}'</b>:</p>

    <ul><li><a href="{dnotebook_file}" style="font-size: 18px; margin: 4px 0;background-color: white; color: #4F77AA; padding: 5px 9px; text-align: center; text-decoration: none; display: inline-block;">Course of the day</a></li></ul>

{end},<br/><br/>

{signature}<br/>
<img alt="" src="https://raw.githubusercontent.com/guydegnol/bulkhours/main/data/BulkHours.png" width=100 />

</body>
</html>
"""

    IPython.display.display(IPython.display.HTML(html))


def send_mail(me="g*@gmail.com", you="contact@bulkhours.eu"):
    """Example:
    admin.send_mail(me="g*@gmail.com", you="s*@gmail.com")
    """

    html = """
    <html>
    <head>
        <style> 
        table, th, td {{ border: 1px solid black; border-collapse: collapse; }} th, td {{ padding: 5px; }}
        </style>
    </head>
    <body><p>Hello</p>
    </body>
    </html> """

    ImgFileName = "capture.png"
    with open(ImgFileName, "rb") as f:
        img_data = f.read()
    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))

    emailmultipart = MIMEMultipart()
    emailmultipart["From"] = me
    emailmultipart["To"] = you
    emailmultipart["Subject"] = "Subject"
    emailmultipart.attach(MIMEText(html, "html"))
    emailmultipart.attach(image)

    server = "smtp.gmail.com:587" if 1 else "smtpauth.online.net:2525"
    server = smtplib.SMTP(server)
    server.ehlo()
    server.starttls()
    server.login("g*@gmail.com", "****")
    server.send_message(emailmultipart)
    server.quit()
