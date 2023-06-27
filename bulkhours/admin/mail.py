import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def send_mail(me="guydegnol@gmail.com", you="guillaume.therin@guydegnol.net"):
    """Example:
    admin.send_mail(me="guydegnol@gmail.com", you="sylvia.rdzzo@gmail.com") # sylvia.rdzzo@gmail.com guillaume.therin@gmail.com
    """

    html = """
    <html>
    <head>
        <style> 
        table, th, td {{ border: 1px solid black; border-collapse: collapse; }} th, td {{ padding: 5px; }}
        </style>
    </head>
    <body><p>Salut bébé.</p>
        <p>Ca boome ?</p>
    P.S.: tu te fais draguer par un robot 🍆.
    </body>
    </html> """

    import os

    ImgFileName = "capture.png"
    with open(ImgFileName, "rb") as f:
        img_data = f.read()
    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))

    emailmultipart = MIMEMultipart()
    emailmultipart["From"] = me
    emailmultipart["To"] = you
    emailmultipart["Subject"] = "Yo poupée"
    emailmultipart.attach(MIMEText(html, "html"))
    emailmultipart.attach(image)

    server = "smtp.gmail.com:587" if 1 else "smtpauth.online.net:2525"
    server = smtplib.SMTP(server)
    server.ehlo()
    server.starttls()
    server.login("guydegnol@gmail.com", "urkemorlctmiovzt")
    server.send_message(emailmultipart)
    server.quit()
