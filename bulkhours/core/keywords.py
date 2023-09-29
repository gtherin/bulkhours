from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import random as rd
from PIL import Image

from . import tools
from .colors import caliases


def keywords():
    return {"edtech": 2, 
        "veille pédagogique": 2,
        "cas pratiques": 1,
        "génération d'énoncés'automatisés": 1, 
        "interactivité": 5, 
        "ML support": 4,
        "various data API": 4,
        "évaluations automatiques": 4,
        "fabrication de cours": 2, 
        "enseignement": 3, 
        "science des données": 3, 
        "plateforme dynamique": 1,
        "outils d'évaluation": 2, 
        "ocr": 2,
        "enseignement à distance": 3,
        "excellence pédagogique": 3,
        "apprentissage par renforcement": 1,
        "open source": 1,
        "mathsématiques": 1,
        "physique": 1,
        "statistiques": 1,
        "machine_learning": 1,
        "jupyter": 1,
        "python": 1,
        "C++": 1,
}


def get_keywords():
    rd.seed(42)

    words = []
    for k, v in keywords().items():
        words += [k] * v

    rd.shuffle(words)
    return words

def get_colors(word, font_size, position, orientation, random_state=None, **kwargs):
    return rd.choice(list(caliases.values()))


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

