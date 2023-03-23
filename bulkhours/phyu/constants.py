import numpy as np
import scipy.constants as sc
import pandas as pd


def md(data, size="+4", prefix="* "):
    import IPython

    IPython.display.display(IPython.display.Markdown(r"%s<font size='%s'>%s</font>" % (prefix, size, data)))


default_configs = {
    "albedo": {"c": "Albedo", "u": "Sans unité (entre 0 et 1)", "l": r"$A_{\mathrm{PAR}} = VAL$"},
    "serre": {"c": "Effet de serre", "u": "Sans unité (entre 0 et 1)", "l": r"$S_{\mathrm{PAR}} = VAL$"},
    "d_ua": {"c": "Distance au soleil", "u": "ua", "l": r"$d_{\mathrm{soleil} \mathrm{PAR}} = VALUNI$"},
    "R_km": {"c": "Rayon", "u": "km", "l": r"$R_{\mathrm{PAR}} = VALUNI$"},
    "d_solm": {"c": "Distance au soleil", "u": "m", "l": r"$d_{\mathrm{soleil} \mathrm{PAR}} = VALUNI$"},
    "M_kg": {"c": "Masse", "u": "kg", "l": r"$M_{\mathrm{PAR}} = VALUNI$"},
    "T_C": {"c": "Temperature moyenne", "u": "°C", "l": r"$T_{\mathrm{PAR}} = VALUNI$"},
    "L_W": {"c": "Luminosité", "u": "W", "l": r"$L_{\mathrm{PAR}} = VALUNI$"},
}


class Constant:
    def fv(self, latex=True):
        val = "%.3e" % self.v if np.abs(self.v) > 1e6 or np.abs(self.v) < 1e-6 else str(self.v)
        if "e" in val and latex:
            val = "%s \cdot 10^{%s}" % (val.split("e")[0], int(val.split("e")[1]))
        return val

    def fu(self):
        uni = str(self.u)
        if "." not in uni:
            return uni

        du = []
        for u in uni.split("."):
            if "-" in u:
                du.append(u.replace(u[-2:], "^{%s}" % u[-2:]))
            elif u[-1] in ["2", "3", "4"]:
                du.append(u.replace(u[-1], f"^{u[-1]}"))
            else:
                du.append(u)
        return "\cdot ".join(du)

    def __init__(self, v, l=r"$ID = VALUNI$", u="", c="", s=np.nan, i="", p="") -> None:
        self.v = v
        self.i = i
        latex = default_configs[c]["l"] if c in default_configs and "l" in default_configs[c] else l
        self.u = default_configs[c]["u"] if c in default_configs and "u" in default_configs[c] else u
        self.c = default_configs[c]["c"] if c in default_configs and "c" in default_configs[c] else c
        self.p = default_configs[c]["p"] if c in default_configs and "p" in default_configs[c] else p
        self.s = default_configs[c]["s"] if c in default_configs and "s" in default_configs[c] else s

        self.latex = latex.replace("ID", self.i).replace("VAL", self.fv()).replace("UNI", self.fu())
        self.latex = self.latex.replace("PAR", str(self.p)).replace("\mathrm{soleil}", "\odot")

    def help(self, size="+3", code=True, markdown=True):
        if markdown:
            md(self.c + ": " + self.latex, size=size)
        if code:
            print(f"consts.{self.i}={self.fv(latex=False)}  # {self.u}")

    def __repr__(self):
        self.help()
        return ""

    @property
    def l(self):
        md(self.latex)


class Units:
    def add_constant(self, k, v, c="", p="", **kwargs) -> None:
        self.csts[k] = Constant(v, i=k, c=c, p=p, **kwargs)
        if c not in self.csts2d:
            self.csts2d[c] = {}
        self.csts2d[c][p] = self.csts[k]

    def __init__(self) -> None:
        # See: https://docs.scipy.org/doc/scipy/reference/constants.html#rc437f0a4090e-codata2018
        self.csts, self.csts2d = {}, {}

        self.add_constant("c2k", sc.zero_Celsius, l=r"$VAL°K=0°C$", u="K.C-1", c="Celsius en Kelvin")
        self.add_constant("c", 300_000, l=r"$c = 3 \cdot 10^{8} ms^{-1}$", u="m.s-1", c="Celerité de la lumière")
        self.add_constant("annee_lumiere", sc.light_year, u="m.al-1", c="Distance parcourue par la lumière en 1an")
        self.add_constant(
            "parsec",
            sc.parsec,
            u="m.pc-1",
            c="Unité astrononique sous-tend un angle d'une seconde d'arc",
            l=r"$1pc \equiv \frac{180\cdot60\cdot60}{\pi} = VALm = 3.26al$",
        )

        self.add_constant("G", 6.67e-11, l=r"$G=VALUNI$", u="N.m2.kg-2", c="Constante de la gravitation", s=sc.G)
        self.add_constant("h", 6.626e-34, l=r"$h=VALUNI$", u="J.s", c="Constante de Planck", s=sc.h)
        self.add_constant("hbar", sc.hbar, l=r"$\bar{h} = \frac{h}{2\pi}$", u="J.s")
        self.add_constant(
            "N_A",
            sc.N_A,
            c="Nombre d'Avogadro:",
            l=r"$N_\mathcal{A} = 6.02 \cdot 10^{23} mol^{-1}$ ($12g(\mathrm{Carbone})\equiv 1mol$)",
            u="mol-1",
        )
        self.add_constant("sigma", sc.sigma, c="Constante de Stefan-Boltzmann", u="W.m-2.K-4", l=r"$\sigma = VAL UNI$")
        self.add_constant("Wien", sc.Wien, c="Constante de Wien")
        self.add_constant("Rydberg", sc.Rydberg, c="Constante de Rydberg")

        self.add_constant("ev", 1.6e-19, u="J.eV-1", s=sc.electron_volt, c="Energie cinetique e sous 1Volt")
        self.add_constant("m_e", 9.109e-31, c="Masse electron", u="kg", s=sc.electron_mass)
        self.add_constant("r_bohr", 5.3e-11, l=r"$a = 5.3 \cdot 10^{-11} m$", c="Rayon de Bohr", u="m")

        self.add_constant("M_mercure", 3.301e23, c="M_kg", p="mercure")
        self.add_constant("d_mercure", 0.47, c="d_ua", p="mercure")
        self.add_constant("R_mercure", 2439, c="R_km", p="mercure")
        self.add_constant("A_mercure", 0.088, c="albedo", p="mercure")
        self.add_constant("S_mercure", 0.000, c="serre", p="mercure")
        self.add_constant("T_mercure", 167, c="T_C", p="mercure")

        self.add_constant("M_venus", 4.867e24, c="M_kg", p="venus")
        self.add_constant("d_venus", 0.72, c="d_ua", p="venus")
        self.add_constant("R_venus", 3390, c="R_km", p="venus")
        self.add_constant("A_venus", 0.770, c="albedo", p="venus")
        self.add_constant("S_venus", 0.991, c="serre", p="venus")
        self.add_constant("T_venus", 464, c="T_C", p="venus")

        self.add_constant("M_terre", 5.972e24, c="M_kg", p="terre")
        self.add_constant("d_terre", 1.00, c="d_ua", p="terre")
        self.add_constant("R_terre", 6371, c="R_km", p="terre")
        self.add_constant("A_terre", 0.300, c="albedo", p="terre")
        self.add_constant("S_terre", 0.394, c="serre", p="terre")
        self.add_constant("T_terre", 15, c="T_C", p="terre")
        self.add_constant(
            "d_terre_solm",
            150e9,
            c="Distance au soleil",
            p="terre",
            s=sc.au,
            u="m",
            l=r"$d_{\mathrm{soleil} \mathrm{PAR}} = 1ua = VALm$",
        )

        self.add_constant("M_mars", 6.417e23, c="M_kg", p="mars")
        self.add_constant("d_mars", 1.52, c="d_ua", p="mars")
        self.add_constant("R_mars", 3390, c="R_km", p="mars")
        self.add_constant("A_mars", 0.250, c="albedo", p="mars")
        self.add_constant("S_mars", 0.010, c="serre", p="mars")
        self.add_constant("T_mars", -62.8, c="T_C", p="mars")

        self.add_constant("M_soleil", 1.988 * 10**30, c="M_kg", p="soleil")
        self.add_constant("L_soleil", 3.83 * 10**26, c="L_W", p="soleil")

        self.add_constant("A_lune", 0.11, c="albedo", p="lune")
        self.add_constant("d_lune", 1.00, c="d_ua", p="lune")

    def __getattr__(self, name: str):
        return self.csts[name].v

    def help(self, label=None, size="+2", code=True, markdown=True) -> None:
        if not label:
            print(self.csts.keys())
        elif label in self.csts:
            print(self.csts[label].help(size=size, code=code, markdown=markdown))
        else:
            md(label, prefix="")
            print(f"from bulkhours import constants as consts")
            for k, v in self.csts.items():
                if label.lower() in k.lower() or label.lower() in ["all"]:
                    v.help(size=size, code=code, markdown=markdown)

    def DataFrame(self, index=[], columns=[]) -> pd.DataFrame:
        if index[0] in self.csts2d:
            data = pd.DataFrame(index=columns)
            for c in index:
                data[c] = [self.csts2d[c][p].v for p in columns]
            data = data.T
        else:
            data = pd.DataFrame(index=index)
            for c in columns:
                data[c] = [self.csts2d[c][p].v for p in index]

        return data


constants = Units()
