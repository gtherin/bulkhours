import matplotlib.pyplot as plt
import numpy as np
import scipy.constants as sc


def md(data, prefix="* ", size="+3"):
    import IPython

    IPython.display.display(IPython.display.Markdown(r"%s<font size='%s'>%s</font>" % (prefix, size, data)))


class Formulas:
    def __init__(self) -> None:
        pass

    @property
    def Shrodinger1D(self):
        md(r"$H\Psi(x) = E\Psi(x)$")
        md(r"$\frac{-\hbar}{2m} \frac{d^2\Psi(x)}{dx^2} + U(x)\Psi(x) = E\Psi(x)$")

    @property
    def Stefan(self):
        md(r"$F = \sigma \cdot T^4$")
        md(r"$F$ Flux rayonné (en $W.m^{-2}$)")
        md(r"$T$ Température du corps (en K)")
        md(r"Constante de Stefan-Boltzmann $\sigma = 5.67 \cdot 10^{-8} W.m^{-2}.K^{-4}$")

    @property
    def Wien(self):
        md(r"$\lambda_{\text{max}} \cdot T = 2.9 \cdot 10^{-3} m . K$")
        md(r"$\lambda_{\text{max}}$ Longueur d'onde du maximum d'émission (en m)")

    @property
    def Ritz(self):
        md(r"$\frac{1}{\lambda} = R_H (\frac{1}{n^2} - \frac{1}{m^2})$ avec $m > n$, $λ > 0$")
        md(r"$\lambda$ Longueur d'onde de la raie (cm)")
        md(r"$R_H({\text{Hydrogene}}) = 110 000 \text{ cm}^{-1}$")
        md(r"$R_H$ Constante de Rydberg (${\text{Hydrogene}} = 110 000 \text{ cm}^{-1}$)")

    @property
    def Eclairement(self):
        md(r"$e = \frac{L}{4\pi d^2}$")
        md(r"**Luminosité** L: quantité de lumiere émise, puissance lumineuse (W)")
        md(r"**Eclairement** e: quantité de lumiere reçue, puissance par unité de surface ($W . m^{-2}$)")
        md(
            r"Cette puissance étant émise à priori dans toutes les directions, elle se répartit sur une sphère dont le rayon est la **distance** d, qui nous sépare de la course",
            size="+2",
        )

    @property
    def ForcageRadiatif(self):
        md(r"Forcage radiatif: $F = S\cdot \sigma \cdot T^4$")

    @property
    def EquilibreThermique(self):
        md(r"Equilibre thermique: $(1-A)\frac{ L_\odot R^2}{4 d^2} \equiv (1-S) 4 \pi R^2 \sigma T^4$")

    def help(self, label=None, size="+2") -> None:
        if not label:
            for k in ["Stefan", "Wien", "Ritz", "Eclairement", "EquilibreThermique"]:
                md(k, prefix="")
                getattr(self, k)
        elif hasattr(self, label):
            getattr(self, label)


formulas = Formulas()
