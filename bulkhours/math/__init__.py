from .poly2r import Poly2dr
from .poly1r import Poly1dr
from .tools import md, html
from .math_table import MathTable
from . import td1
from . import td2
from .vector import Vector, VectorGrid

def display_warning(language = "fr"):
    if language == "fr":
        text1 = 'Cette page utilise (<i>Package de support de cours interactif</i>). Si vous aimez cette approche🚀🏆🎯, <br/>vous pouvez supporter le projet sur <a href="https://github.com/guydegnol/bulkhours">github</a> en donnant quelques etoiles.'
    else:
        text1 = 'This page is using (<i>A Support course package</i>). If you like this approach🚀🏆🎯, <br/>please support the project on <a href="https://github.com/guydegnol/bulkhours">github</a> with some stars.'

    text2 = """🚧🚧🚧🚧<b>Attention!</b> Cette page est un <font color="red"><b> brouillon de correction</b></font>:🚧🚧🚧🚧<ol>
<li><b>Il y a donc beaucoup encore d'erreurs</b>. Je n'ai pas encore eu le temps de tout corriger.
Merci beaucoup de reporter les erreurs à <A HREF="mailto:guillaume.therin@ipsa.fr">guillaume.therin@ipsa.fr</A></li>
<li>Quelques exercices n'ont pas du tout de correction.</li>
<li>La mise à jour doit encore etre ajustée.</li>
</ol>
⚠️Si vous voulez quand même continuer, allez dans l'onglet <b>"Execution"</b> et cliquez sur <b>"Redémarrer et tout exécuter"</b>⚠️
"""

    html(
            f"""
<table style="opacity:0.8;">
    <tr>
      <td style="background-color: white;"><a href="https://github.com/guydegnol/bulkhours"><img style="background-color: white;" src="https://github.com/guydegnol/bulkhours/blob/ce2ce67a250b396b7341becf7deb09da961f2698/data/BulkHours.png?raw=true" width="100"></a></td>
      <td style="background-color: white; text-align:left; color:black">{text1}</td>
      <td style="background-color: white;"><a href="https://github.com/guydegnol/bulkhours">
      <img style="background-color: white;" src="https://github.com/guydegnol/bulkhours/blob/main/data/github.png?raw=true" width="30"></a></td>
      <td style="background-color: white;">
      <a href="https://github.com/guydegnol/bulkhours">
      <img style="background-color: white;margin-top: 0.5em;" src="https://github.com/guydegnol/bulkhours/blob/main/data/like.gif?raw=true" width="150">
      </a>      
      </td>
</tr>
    <tr>
      <td colspan="4"style="background-color: white; text-align:left; color:black">{text2}</td>
</tr>
</table>
"""
        )
