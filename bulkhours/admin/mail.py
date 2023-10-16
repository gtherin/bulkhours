import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from .. import core


def copy(email, drive_rdir, filename, default_student):

    from subprocess import getoutput
    from google.colab import drive
    import nbformat

    def get_drive_filename(filename):
        from xattr import xattr
        return f"https://colab.research.google.com/drive/" + (xattr(filename).get('user.drive.id').decode())

    # Get student reference notebook
    drive.mount('/content/gdrive/')
    ofilename = f"{drive_rdir}/{filename}"

    # Get token
    cfg = core.tools.get_config(is_new_format=True)
    ntoken = cfg.tokens[cfg.virtual_room]

    # Parse notebook
    to_pop, nb = [], nbformat.read(ofilename, nbformat.NO_CONVERT).copy()
    for idx, cell in enumerate(nb.cells):
        if cell["cell_type"] == "code":
            # Change the initialization cell
            if "\ndatabase" in cell["source"]:
                source = cell["source"].split("\n")
                nsource = []
                for s in source:
                    if s.startswith('database'):
                        s = f'database = "{ntoken}"'
                    if s.startswith('email'):
                        s = s.replace(email, default_student)
                    nsource.append(s)
                cell["source"] ="\n".join(nsource)
                cell["outputs"][0]["text"] = ""
            # Remove cells with admin code
            elif "[admin]" in cell["source"] or "bulkhours.admin" in cell["source"]:
                to_pop.append(idx)
            # Remove cells with solution
            elif " -u solution" in cell["source"]:
                to_pop.append(idx)
            # Format cells with reset info
            elif " -u reset" in cell["source"]:
                cell["source"] = cell["source"].replace(" -u reset", "")
        #print(idx, cell.keys(), cell["metadata"])

    # Remove listed cells
    print("Pop the following cells: ", to_pop)
    for i in to_pop[::-1]:
        nb.cells.pop(i)

    # Create the new notebook
    nbformat.write(nb, cfilename:=ofilename.replace('.', f'_{cfg.virtual_room}.'), version=nbformat.NO_CONVERT)
    dfilename = get_drive_filename(cfilename)
    print(f"File {cfilename} is accessible via: {dfilename}")
    return dfilename



def prepare_mail(default_student="john.doe@bulkhours.eu", signature="The bulkHours team", generate_file=True, 
                 notebook_file=None, drive_rdir=None):

    if generate_file:
        notebook_file = copy(signature, drive_rdir, notebook_file, default_student)

    if "@" in signature:
        signature = signature.split("@")[0].replace(".", " ").title()

    import IPython
    cfg = core.tools.get_config(is_new_format=True)

    title = f"Notebook of the day: {notebook_file.split('.')[0]}"
    intro = f"Dear all,<br/><br/>Here is the practical course of the day. Remember to write your email address to replace"
    end = f"Best regards"

    if cfg.language == "fr":
        title = f"Notebook du jour: {notebook_file.split('.')[0]}"
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
