import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from .. import core


def prepare_mail(label=None, default_student="john.doe@bulkhours.eu", signature="The bulkHours team"):
    import IPython
    cfg = core.tools.get_config(is_new_format=True)

    intro = f"Dear all,<br/><br/>Here is the practical course of the day. Remember to write your email address to replace"
    end = f"Best regards"

    if cfg.language == "fr":
        intro = f"Bonjour à toutes et à tous,<br/><br/>Voici le lien vers le cours du jour.<br/>💡Rappelez-vous bien de mettre votre adresse mail à la place de"
        end = f"Cordialement"

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
    <h2>Content of the mail:</h2><br/>
    <p>{intro} <b>'{default_student}'</b>:</p>

    <ul><li><a href="{cfg[cfg.notebook_id]['page']}" style="font-size: 18px; margin: 4px 0;background-color: white; color: #4F77AA; padding: 5px 9px; text-align: center; text-decoration: none; display: inline-block;">Course of the day</a></li></ul>

{end},<br/><br/>

{signature}</b>
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
