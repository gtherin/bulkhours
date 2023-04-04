import numpy as np
import scipy.constants as sc
import pandas as pd


def md(data, size="+4", prefix="* "):
    import IPython

    IPython.display.display(IPython.display.Markdown(r"%s<font size='%s'>%s</font>" % (prefix, size, data)))


default_configs = {
    "Albedo": {"c": "Albedo", "u": "Sans unité (entre 0 et 1)", "l": r"$A_{\mathrm{PAR}} = VAL$", "r": 2},
    "Serre": {"c": "Effet de serre", "u": "Sans unité (entre 0 et 1)", "l": r"$S_{\mathrm{PAR}} = VAL$"},
    "d_ua": {"c": "Distance au soleil", "u": "ua", "l": r"$d_{\mathrm{soleil} \mathrm{PAR}} = VALUNI$"},
    "R_km": {"c": "Rayon", "u": "km", "l": r"$R_{\mathrm{PAR}} = VALUNI$", "r": 0},
    "d_solm": {"c": "Distance au soleil", "u": "m", "l": r"$d_{\mathrm{soleil} \mathrm{PAR}} = VALUNI$", "r": 2},
    "M_kg": {"c": "Masse", "u": "kg", "l": r"$M_{\mathrm{PAR}} = VALUNI$"},
    "T_C": {"c": "Temperature moyenne", "u": "°C", "l": r"$T_{\mathrm{PAR}} = VALUNI$", "r": 1},
    "L_W": {"c": "Luminosité", "u": "W", "l": r"$L_{\mathrm{PAR}} = VALUNI$"},
}


class Constant:
    def fv(self, latex=True):
        if self.v == 0:
            return "0"
        elif np.abs(self.v) > 1e5 or np.abs(self.v) < 1e-5:
            val = "%.{0}e".format(self.r) % self.v
            return "%s \cdot 10^{%s}" % (val.split("e")[0], int(val.split("e")[1])) if latex else val
        else:
            return "%.{0}f".format(self.r) % self.v

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

    def __init__(self, v, l=r"$ID = VALUNI$", u="", c="", s=np.nan, i="", p="", r=3, a=[], title=None) -> None:
        self.v, self.i, self.r, self.a = v, i, r, a
        self.latex = default_configs[c]["l"] if c in default_configs and "l" in default_configs[c] else l
        self.u = default_configs[c]["u"] if c in default_configs and "u" in default_configs[c] else u
        self.c = default_configs[c]["c"] if c in default_configs and "c" in default_configs[c] else c
        self.p = default_configs[c]["p"] if c in default_configs and "p" in default_configs[c] else p
        self.s = default_configs[c]["s"] if c in default_configs and "s" in default_configs[c] else s
        self.r = default_configs[c]["r"] if c in default_configs and "r" in default_configs[c] else r

        if title and title == "mathrm":
            self.latex = self.latex.replace("ID", "\mathrm{%s}" % self.i)
        elif title:
            self.latex = self.latex.replace("ID", title)
        self.latex = self.latex.replace("ID", self.i).replace("VAL", self.fv()).replace("UNI", self.fu())
        self.latex = self.latex.replace("PAR", str(self.p)).replace("\mathrm{soleil}", "\odot")

    def help(self, size="+3", code=True, markdown=True):
        if markdown:
            text = (
                self.c + ": " + self.latex + f"   [{self.s}{self.u}]"
                if self.s == self.s
                else self.c + ": " + self.latex
            )
            md(text, size=size)
        if code:
            for ai in [self.i] + self.a:
                print(f"consts.{ai}={self.fv(latex=False)}  # {self.u}")

    def __repr__(self):
        self.help()
        return ""

    @property
    def l(self):
        md(self.latex)


class Units:
    def add_constant(self, k, v, c="", p="", a=[], **kwargs) -> None:
        self.csts[k] = Constant(v, i=k, c=c, p=p, a=a, **kwargs)
        for ia in a:
            self.acsts[ia] = self.csts[k]
        if c not in self.csts2d:
            self.csts2d[c] = {}
        self.csts2d[c][p] = self.csts[k]

    def __init__(self) -> None:
        # See: https://docs.scipy.org/doc/scipy/reference/constants.html#rc437f0a4090e-codata2018
        self.acsts, self.csts, self.csts2d = {}, {}, {}

        self.add_constant(
            "c2k", sc.zero_Celsius, l=r"$VAL°K=0°C$", u="K.C-1", c="Celsius en Kelvin", r=2, a=["kelvin"]
        )
        self.add_constant("c", 300_000, u="m.s-1", c="Celerité de la lumière", r=0, a=["vitesse_lumiere"])
        self.add_constant(
            "al",
            sc.light_year,
            u="m",
            c="Distance parcourue par la lumière en 1an",
            a=["annee_lumiere"],
        )
        self.add_constant(
            "parsec",
            sc.parsec,
            u="m.pc-1",
            c="Une Unité astrononique faisant un angle d'une seconde d'arc (déprécié)",
            l=r"$1pc \equiv \frac{180\cdot60\cdot60}{\pi} = VALm = 3.26al$",
        )

        self.add_constant("G", 6.67e-11, u="N.m2.kg-2", c="Constante de la gravitation", s=sc.G, r=2)
        self.add_constant("g", 9.8, u="m.s-2", c="Acceleration standard de la gravitation", s=sc.g, r=1)
        self.add_constant("h", 6.626e-34, u="J.s", c="Constante de Planck", s=sc.h)
        self.add_constant("hbar", sc.hbar, l=r"$\bar{h} = \frac{h}{2\pi}$", u="J.s")
        self.add_constant(
            "N_A",
            sc.N_A,
            c="Nombre d'Avogadro",
            l=r"$N_\mathcal{A} = VALUNI$ (Carbone: $12g\Leftrightarrow 1mol$)",
            u="mol-1",
            r=2,
            a=["A"],
        )
        self.add_constant(
            "sigma",
            sc.sigma,
            c="Constante de Stefan-Boltzmann",
            u="W.m-2.K-4",
            l=r"$\sigma = VAL UNI$",
            r=2,
            a=["stefan"],
        )
        self.add_constant(
            "Wien",
            2.9e-3,
            c="Constante de Wien",
            l=r"$\lambda_{\text{max}} \cdot T = VALUNI$",
            s=sc.Wien,
            u="m.K",
            a=["wien", "lambda_max"],
        )
        self.add_constant(
            "Rydberg",
            sc.Rydberg,
            c="Constante de Rydberg",
            l=r"$R_H({\text{Hydrogene}}) = VALUNI$",
            u="m-1",
            r=1,
            a=["rydberg", "R_H"],
        )

        self.add_constant(
            "eV",
            1.6e-19,
            u="J.eV-1",
            s=sc.electron_volt,
            c="Energie cinetique e sous 1Volt",
            r=1,
            a=["ev"],
            title="mathrm",
        )
        self.add_constant("m_e", 9.109e-31, c="Masse electron", u="kg", s=sc.electron_mass)
        self.add_constant("r_bohr", 5.3e-11, l=r"$a = 5.3 \cdot 10^{-11} m$", c="Rayon de Bohr", u="m", a=["a"])

        self.add_constant("m_p", 1.6726e-27, c="Masse proton", u="kg", s=sc.proton_mass)
        self.add_constant(
            "m_puma",
            1.007276,
            c="Masse proton",
            u="uma",
            l=r"$m_p = VALUNI$ ($1uma \equiv \frac{M(^{12}C)}{12}$)",
            s=sc.physical_constants["proton relative atomic mass"][0],
            r=6,
        )
        self.add_constant(
            "m_numa",
            1.008663,
            c="Masse neutron",
            u="uma",
            l=r"$m_n = VALUNI$ ($1uma \equiv \frac{M(^{12}C)}{12}$)",
            s=sc.physical_constants["neutron relative atomic mass"][0],
            r=6,
        )
        self.add_constant(
            "uma",
            1.6605e-27,
            c="Unité de Masse Atomique",
            u="kg.uma-1",
            s=sc.physical_constants["unified atomic mass unit"][0],
            l=r"$m_{nuc} = VALUNI$ ($1uma \equiv \frac{M(^{12}C)}{12}$)",
        )
        self.add_constant(
            "uma_mev",
            931.5,
            c="Unité de Masse Atomique (MeV)",
            u="MeV.uma-1",
            l=r"$m_{nuc} = VALUNI$ ($1uma \equiv \frac{M(^{12}C)}{12}$)",
        )

        self.add_constant("M_mercure", 3.301e23, c="M_kg", p="mercure")
        self.add_constant("d_mercure", 0.47, c="d_ua", p="mercure")
        self.add_constant("R_mercure", 2439, c="R_km", p="mercure")
        self.add_constant("A_mercure", 0.088, c="Albedo", p="mercure")
        self.add_constant("S_mercure", 0.000, c="Serre", p="mercure")
        self.add_constant("T_mercure", 167, c="T_C", p="mercure")

        self.add_constant("M_venus", 4.867e24, c="M_kg", p="venus")
        self.add_constant("d_venus", 0.72, c="d_ua", p="venus")
        self.add_constant("R_venus", 3390, c="R_km", p="venus")
        self.add_constant("A_venus", 0.770, c="Albedo", p="venus")
        self.add_constant("S_venus", 0.991, c="Serre", p="venus")
        self.add_constant("T_venus", 464, c="T_C", p="venus")

        self.add_constant("M_terre", 5.972e24, c="M_kg", p="terre")
        self.add_constant("d_terre", 1.00, c="d_ua", p="terre")
        self.add_constant("R_terre", 6371, c="R_km", p="terre")
        self.add_constant("A_terre", 0.300, c="Albedo", p="terre")
        self.add_constant("S_terre", 0.394, c="Serre", p="terre")
        self.add_constant("T_terre", 15, c="T_C", p="terre")
        self.add_constant(
            "d_terre_solm",
            150e9,
            c="Distance au soleil",
            p="terre",
            s=sc.au,
            u="m",
            l=r"$d_{\mathrm{soleil} \mathrm{PAR}} = 1ua = VALUNI$",
            a=["d_terresoleil"],
        )

        self.add_constant("M_mars", 6.417e23, c="M_kg", p="mars")
        self.add_constant("d_mars", 1.52, c="d_ua", p="mars")
        self.add_constant("R_mars", 3390, c="R_km", p="mars")
        self.add_constant("A_mars", 0.250, c="Albedo", p="mars")
        self.add_constant("S_mars", 0.010, c="Serre", p="mars")
        self.add_constant("T_mars", -62.8, c="T_C", p="mars")

        self.add_constant("M_soleil", 1.988 * 10**30, c="M_kg", p="soleil")
        self.add_constant("R_soleil", 696_000, c="R_km", p="soleil")
        self.add_constant("L_soleil", 3.83 * 10**26, c="L_W", p="soleil", r=2)
        self.add_constant("T_soleil", 5800, c="T_C", p="soleil")

        self.add_constant("A_lune", 0.11, c="Albedo", p="lune")
        self.add_constant("d_lune", 1.00, c="d_ua", p="lune")
        self.add_constant("pi", np.pi, r=6)

    def __getattr__(self, name: str):
        if name in self.csts:
            return self.csts[name].v
        if name in self.acsts:
            return self.acsts[name].v
        return np.nan

    def help(self, label=None, size="+2", code=True, markdown=True) -> None:
        if not label:
            print(self.csts.keys())
        elif label in self.csts:
            self.csts[label].help(size=size, code=code, markdown=markdown)
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
