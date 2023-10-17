import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from .. import core


def cell_reset(source):
    """
# BKRESET.REMOVE:START
    # This code won't appear in the reset generation
    # It will appear on the solution though
# BKRESET.REMOVE:END

# BKRESET.PRINT:raw_std = gdf[f"ret_{i}"].ewm(20).std()
    # The previous line will be printed in the reset generation
    # The previous line won't be printed in the solution generation

    
print(models["fit1"].forecast(3)) # BKRESET.REMOVE:LINE
    # The previous line won't be printed in the reset generation
    # The previous line will be printed in the solution generation

    
df["noise"] = sp.stats.norm(loc=3, scale=0.3).rvs(n) # BKRESET.INIT:0

    """
    nsource = []

    keep_line = True

    for s in source:
        if "BKRESET." in s:
            l = s.split("BKRESET.")
            if "INIT:" in l[1]:
                s = s.split("=")[0] + " = " + l[1].replace("INIT:", "") + "  # ..."
            if "REMOVE" in l[1]:
                if "START" in l[1]:
                    keep_line = False
                elif "END" in l[1]:
                    keep_line = True
                    s = s.split("#")[0] + "# ..."
                else:
                    indentation = len(s) - len(s.lstrip())
                    s = (" " * indentation) + "# ..."
            if "REPLACE" in l[1]:
                indentation = len(s) - len(s.lstrip())
                s = (" " * indentation) + l[1].replace("REPLACE:", "") + "  # ..."
            if "PRINT" in l[1]:
                indentation = len(s) - len(s.lstrip())
                s = (" " * indentation) + l[1].replace("PRINT:", "")

        if keep_line:
            nsource.append(s)

    #print("\n".join(nsource))
    return "\n".join(nsource)

def cell_solution(source):
    nsource = []
    for s in source:
        if "BKRESET." in s:
            l = s.split("BKRESET.")
            if "INIT:" in l[1] or "REPLACE:" in l[1]:
                s = l[0][:l[0].rfind("#")]
            if "REMOVE" in l[1] or "PRINT" in l[1]:
                continue

        nsource.append(s)

    print("\n".join(nsource))
    return "\n".join(nsource)


def copy(email, drive_rdir, filename, default_student, reset=True):

    import IPython
    from subprocess import getoutput
    from google.colab import drive
    import nbformat

    def get_drive_filename(filename):
        from xattr import xattr
        return f"https://colab.research.google.com/drive/" + (xattr(filename).get('user.drive.id').decode())

    # Get student reference notebook
    cfg = core.tools.get_config(is_new_format=True)
    ofilename = f"{drive_rdir}/{filename}"
    cfilename = ofilename.replace('.', f'_{cfg.virtual_room}.')
    IPython.display.display(
        IPython.display.Markdown(f"## Notebook generation '`{cfilename.split('/')[-1]}`'"))    

    # Mount google drive
    drive.mount('/content/gdrive/')

    # Get token
    ntoken = cfg.tokens[cfg.virtual_room]

    # Parse notebook
    to_pop, nb = [], nbformat.read(ofilename, nbformat.NO_CONVERT).copy()
    for idx, cell in enumerate(nb.cells):
        if cell["cell_type"] == "code":

            source = cell["source"].split("\n")

            # Change the initialization cell
            if "\ndatabase" in cell["source"]:
                nsource = []
                for s in source:
                    if s.startswith('database'):
                        s = f'database = "{ntoken}"'
                    if s.startswith('email'):
                        s = s.replace(email, default_student)
                    nsource.append(s)
                cell["source"] = "\n".join(nsource)
                cell["outputs"][0]["text"] = ""
            # Remove cells with admin code
            elif "[admin]" in source[0] or "bulkhours.admin" in cell["source"]:
                to_pop.append(idx)
            # Remove cells with solution
            elif " -u solution" in source[0]:
                to_pop.append(idx)
            # Format cells with reset info
            elif " -u reset" in source[0]:
                cell["source"] = cell["source"].replace(" -u reset", "")
            elif source[0].startswith('"%%evaluation_cell_id "'):
                cell["source"] = cell_reset(source) if reset else cell_solution(source)
                cell["outputs"][0]["text"] = ""
        if cell["cell_type"] == "markdown":
            source = cell["source"].split("\n")
            # Remove markdown cells with [admin in the first line]
            if "[admin]" in source[0]:
                to_pop.append(idx)
        #print(idx, cell.keys(), cell["metadata"])

    # Remove listed cells
    print("Pop the following cells: ", to_pop)
    for i in to_pop[::-1]:
        nb.cells.pop(i)

    # Create the new notebook
    nbformat.write(nb, cfilename:=ofilename.replace('.', f'_{cfg.virtual_room}.'), version=nbformat.NO_CONVERT)

    dfilename = get_drive_filename(cfilename)
    IPython.display.display(IPython.display.Markdown(f"""* 🌍 {dfilename}\n* 📁 '`{cfilename}`'\n"""))    
    return dfilename


def prepare_mail(default_student="john.doe@bulkhours.eu", signature="The bulkHours team", generate_file=True, 
                 notebook_file=None, drive_rdir=None):

    notebook_info = notebook_file.split('.')[0]
    if generate_file:
        notebook_file = copy(signature, drive_rdir, notebook_file, default_student, reset=True)

    if "@" in signature:
        signature = signature.split("@")[0].replace(".", " ").title()

    import IPython
    cfg = core.tools.get_config(is_new_format=True)

    title = f"Notebook of the day: {notebook_info}"
    intro = f"Dear all,<br/><br/>Here is the practical course of the day. Remember to write your email address to replace"
    end = f"Best regards"

    if cfg.language == "fr":
        title = f"Notebook du jour: {notebook_info}"
        intro = f"Bonjour à toutes et à tous,<br/><br/>Voici le lien vers le cours du jour.<br/>💡Rappelez-vous bien de mettre votre adresse mail à la place de"
        end = f"Cordialement"

    students = cfg.g[cfg.virtual_room].replace(default_student+";", "")

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

    <ul><li><a href="{notebook_file}" style="font-size: 18px; margin: 4px 0;background-color: white; color: #4F77AA; padding: 5px 9px; text-align: center; text-decoration: none; display: inline-block;">Course of the day</a></li></ul>

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
