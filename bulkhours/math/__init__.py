from .poly2r import Poly2dr
from .poly1r import Poly1dr
from .tools import md, html
from .math_table import MathTable
from . import td1
from . import td2
from .vector import Vector, VectorGrid
from .decision import get_wisc_results, get_wisc_saturations, get_grades

def display_warning(language = "fr"):
    if language == "fr":
        text1 = 'Cette page utilise BulkHours 🚀🏆🎯 (<i>package de support de cours</i>). Si vous appreciez ces pages, <br/>vous pouvez supporter le projet sur <a href="https://github.com/gtherin/bulkhours">github</a> en ajoutant des étoiles.'
    else:
        text1 = 'This page is using (<i>A Support course package</i>). If you like this approach🚀🏆🎯, <br/>please support the project on <a href="https://github.com/gtherin/bulkhours">github</a> with some stars.'

    text2 = """🚧🚧🚧🚧<b>Attention!</b> Cette page est un <font color="red"><b> brouillon de correction</b></font>:🚧🚧🚧🚧<ol>
  <li><b>Il y a donc beaucoup encore d'erreurs</b>. Je n'ai pas encore eu le temps de tout corriger.
Merci beaucoup de reporter les erreurs à <A HREF="mailto:guillaume.therin@ipsa.fr">guillaume.therin@ipsa.fr</A></li>
  <li>Quelques exercices n'ont pas encore une correction complete.</li>
  <li>La mise à jour doit encore etre ajustée.</li>
</ol>
"""

    html(
            f"""
<table style="opacity:0.8; margin:0; padding:0;">
    <tr style="background-color: white; margin:0; padding:0;">
      <td style="background-color: white;"><a href="https://github.com/gtherin/bulkhours"><img style="background-color: white;" src="https://github.com/gtherin/bulkhours/blob/ce2ce67a250b396b7341becf7deb09da961f2698/data/BulkHours.png?raw=true" width="100"></a></td>
      <td style="background-color: white; text-align:left; color:black">{text1}</td>
      <td style="background-color: white;"><a href="https://github.com/gtherin/bulkhours">
      <img style="background-color: white;" src="https://github.com/gtherin/bulkhours/blob/main/data/github.png?raw=true" width="30"></a></td>
      <td style="background-color: white; margin:0; padding:0;">
      <a href="https://github.com/gtherin/bulkhours">
      <img style="background-color: white;margin-top: 0.5em;" src="https://github.com/gtherin/bulkhours/blob/main/data/like.gif?raw=true" width="150">
      </a>      
      </td>
</tr>
    <tr style="margin:0; padding:0;">
      <td colspan="4" style="background-color: white; text-align:left; color:black">{text2}</td>
</tr>
</table>
<table style="opacity:0.8; margin:0; padding:0;">
    <tr style="margin:0; padding:0;">
      <td style="background-color: white; text-align:left; margin:0; padding:0;">⚠️Si vous voulez quand même continuer, allez dans l'onglet <b>"Execution"</b> et cliquez sur <b>"Tout exécuter"</b>, avant de pouvoir parcourir cette page.⚠️</td>
      <td colspan="3" style="background-color: white; text-align:left; color:black">
<img style="background-color: white; border: 5px solid #4F77AA; text-align: center;" src="https://github.com/gtherin/bulkhours/blob/main/data/passive_menu.png?raw=true" width="600">
      </td>
</tr>
</table>
"""
        )


def plot_month_temperatures(month, **kwargs):
    import geopandas
    import calendar
    from .. import data

    months_names = dict(zip([calendar.month_name[i] for i in range(1, 13)], range(1, 13)))

    if type(month) == str:
        if month not in months_names:
            print(f"Pick a month in the following list: {months_names[month]}")
            return 
        month = months_names[month]
        
    #cities_data = cities
    geo_data = data.get_data("climate.mapeuropemonthly", credit=False)
    ax = data.geo_plot(data=geo_data, timeopt="last", column=month, figsize=(10, 5), **kwargs)
    gdf = geopandas.GeoDataFrame(geo_data[["City"]], geometry=geopandas.points_from_xy(geo_data.Longitude, geo_data.Latitude)).dropna()
    gdf.plot(color="#00A099", ax=ax, alpha=0.4);
