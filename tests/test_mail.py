import bulkhours


# Test the get_data functions
def test_mail():
    bulkhours.admin.send_mail(
        "contact@bulkhours.fr, no-reply@bulkhours.fr",
        message="""
Bonjour,<br/><br/>

Voici le premier email automatique de bulkhours.
Vos adresses mails:

<ul>
  <li>jean-sebastien@bulkhours.fr</li>
  <li>sylvia@bulkhours.fr</li>
</ul>

ont encore besoin d'etre configurées.<br/><br/>

🐗Guillaume
""",
    )
