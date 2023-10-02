from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import random as rd
from PIL import Image

from . import tools


def get_caliases():
    from .colors import caliases
    ccaliases = caliases
    #ccaliases["courses"] = "#585858"
    return ccaliases


def keywords():
    return {"edtech": [2, None], 
        "veille pédagogique": [2, None],
        "cas pratiques": [1, None],
        "génération d'énoncés automatisés": [1, None],
        "interactivité": [5, None], 
        "fournisseurs de données": [4, None],
        "évaluations automatiques": [4, None],
        "fabrication de cours": [2, None], 
        "inovation pédagogique": [2, None],
        "enseignement": [3, None],
        "science des données": [3, None],
        "plateforme réactive": [1, None],
        "outils d'évaluation": [2, None],
        "ocr": [2, None],
        "enseignement à distance": [3, None],
        "excellence pédagogique": [3, None],
        "apprentissage par renforcement": [1, None],
        "open source": [1, None],
        "mathématiques": [1, None],
        "physique": [1, None],
        "statistiques": [1, None],
        "machine learning": [4, None],
        "jupyter": [1, None],
        "automatisation": [1, None],
        "robotique": [1, "courses"],
        "python": [1, "courses"],
        "c++": [1, "courses"],
        "c": [1, "courses"],
        "cuda": [1, "courses"],
}



def get_keywords():
    rd.seed(42)

    words = []
    for k, v in keywords().items():
        words += [k] * v[0]

    rd.shuffle(words)
    return words

def get_colors(word, font_size, position, orientation, random_state=None, **kwargs):
    wparams = keywords()[word]

    if wparams[1] is not None and wparams[1] in get_caliases():
        return get_caliases()[wparams[1]]
    return rd.choice(list(get_caliases().values()))


def get_wordscloud(default="brain"):

    # bulkhours.core.get_wordscloud()
    from wordcloud import WordCloud
    words = get_keywords()
    mask = np.array(Image.open("cerveau.jpg"))
    wc = WordCloud(background_color="#FFFFFF", repeat=False, mask=mask, contour_width=0)
    wc.generate_from_frequencies(Counter(words))
    plt.axis("off")
    rd.seed(42)
    plt.imshow(wc.recolor(color_func=get_colors), interpolation="bilinear")
    plt.savefig(tools.abspath('data/keywords.png'))



def get_workcloud_archive():
    mask = np.array(Image.open("B.png"))
    wc = WordCloud(background_color="#0097B2", 
                repeat=True, 
                mask=mask, contour_width=0, #contour_color="#C70039", 
                color_func=lambda *args, **kwargs: "#FF5733"
                )
    wc.generate(" ".join(words))
    filename = "Bf.png"
    if filename:
        print(f"Write in {filename}")
        wc.to_file(filename)

    plt.axis("off")
    plt.imshow(wc, interpolation="bilinear")
    #plt.imshow(Image.open("B2.png"), interpolation="bilinear")
    #plt.savefig('Bff.png')
    from cairosvg import svg2png

    if 1:
        svg2png(bytestring=f"""<svg xmlns="http://www.w3.org/2000/svg" width="250" height="300">\n
        <style>.Rrrrr {{font: bold 200px serif; fill: #FFFFFF; }}</style>
        <text x="45" y="230" class="Rrrrr">B</text>
        </svg>""", write_to="B2.png")

    if 0:
        svg2png(bytestring=f"""<svg xmlns="http://www.w3.org/2000/svg" width="250" height="300">\n
        <style>.Rrrrr {{font: bold 200px serif; fill: #FFFFFF}}</style>
        <rect x="0" width="250" height="300" rx="100" style="fill:#000000;stroke-width:3;stroke:#000000" />
        <text x="45" y="230" class="Rrrrr">B</text>
        </svg>""", write_to="B.png")

    if 0:
        svg2png(bytestring=f"""<svg xmlns="http://www.w3.org/2000/svg" width="250" height="300">\n
        <style>.Rrrrr {{font: bold 200px serif; color=#FFFF00}}</style>
        <rect x="0" width="250" height="300" rx="100" style="fill:#FFFF00;stroke-width:3;stroke:#FFFF00" />
        </svg>""", write_to="B.png")

