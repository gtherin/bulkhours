import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from .. import core


def copy(drive_rdir, filename):

    from subprocess import getoutput
    from google.colab import drive

    def get_drive_filename(filename):
        from xattr import xattr
        return f"https://colab.research.google.com/drive/" + (xattr(filename).get('user.drive.id').decode())

    # Get student reference notebook
    drive.mount('/content/gdrive/')
    ofilename = f"{drive_rdir}/{filename}"

    cfg = core.tools.get_config(is_new_format=True)
    ntoken = cfg.tokens[cfg.virtual_room]
    cfilename = ofilename.replace('.', f'_{cfg.virtual_room}.')

    import nbformat as nbf
    ntbk = nbf.read(ofilename, nbf.NO_CONVERT).copy()
    new_ntbk = ntbk
    new_ntbk.cells = [cell for cell in ntbk.cells]

    for indx, cell in enumerate(ntbk.cells):
        if cell["cell_type"] == "code" and "\ndatabase" in cell["source"]:
            source = cell["source"].split("\n")
            nsource = [f'database = "{ntoken}"' if s.startswith('database') else s for s in source]
            cell["source"] ="\n".join(nsource)

    nbf.write(new_ntbk, cfilename, version=nbf.NO_CONVERT)
    dfilename = get_drive_filename(cfilename)
    print(f"File {cfilename} is accessible via: {dfilename}")
    return dfilename



def prepare_mail(default_student="john.doe@bulkhours.eu", signature="The bulkHours team", generate_file=True, 
                 notebook_file=None, drive_rdir=None):

    if generate_file:
        notebook_file = copy(drive_rdir, notebook_file)

    import IPython
    cfg = core.tools.get_config(is_new_format=True)

    intro = f"Dear all,<br/><br/>Here is the practical course of the day. Remember to write your email address to replace"
    end = f"Best regards"

    if cfg.language == "fr":
        intro = f"Bonjour à toutes et à tous,<br/><br/>Voici le lien vers le cours du jour.<br/>💡Rappelez-vous bien de mettre votre adresse mail à la place de"
        end = f"Cordialement"

    if link is None:
        link = cfg[cfg.notebook_id]['page']

    html = f"""
<html>
<head>
    <style> 
    table, th, td {{ border: 1px solid black; border-collapse: collapse; }} th, td {{ padding: 5px; }}
    </style>
</head>
<body>
    <h2>Mail to {cfg.virtual_room} students (in CCI)</h2>
    <p>{cfg.g[cfg.virtual_room]}</p>
    <h2>Title of the mail:</h2><br/>
    <p>TP du jour</p>
    <h2>Content of the mail:</h2><br/>
    <p>{intro} <b>'{default_student}'</b>:</p>

    <ul><li><a href="{link}" style="font-size: 18px; margin: 4px 0;background-color: white; color: #4F77AA; padding: 5px 9px; text-align: center; text-decoration: none; display: inline-block;">Course of the day</a></li></ul>

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
