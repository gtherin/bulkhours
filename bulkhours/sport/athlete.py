import pandas as pd
import numpy as np


class Athlete:
    def __init__(self, *, is_female=True, age=46, hr_max=None, vo2_max, weight=80):
        self.is_female = is_female
        self.hr_max = hr_max if hr_max is not None else 220-age   # bpm
        self.hr_rest = 48   # bpm
        self.weight = weight
        
        self.zones = [0.0, 0.6, 0.7, 0.8, 0.9, 1.05]
        self.vo2_max = 52 # ml /kg / min
        self.ftp = 210 # Watts
        self.vma = self.vo2_max / 3.5
        self.css = 450/(12*60 + 55 - 4*60-12) # m/s
        self.v_max = 3.6 * 100 / 13 # km/h
        self.ASR = self.v_max - self.vma

        self.trimp_a, self.trimp_b = (0.86, 1.67) if is_female else (0.64, 1.92)


    def get_hr_zone_ts(self, hr):
        return pd.cut(hr, bins=self.zones, labels=["Z1", "Z2", "Z3", "Z4", "Z5"], right=False)

    def calculate_trimp(self, t_min, hr_mean):
        IFC = (hr_mean-self.HRrest) / (self.hr_max-self.hr_rest)
        k = self.trimp_a * np.exp(self.trimp_b * IFC)
        return k * t_min * IFC

    def plot_hr_zone(self, ax):
        # Karvonen formula
        hr = lambda x: x * (hr_max - HRrest) + HRrest
        for i, name, color in zip(range(5),
                                  ["Z1 – Very light", "Z2 – Light", "Z3 – Moderate", "Z4 – Hard", "Z5 – Maximum"],
                                  ["#dddddd", "#b5d6ea", "#7fd47f", "#f0b04a", "#e05b4f"]):
            ax.axhspan(hr(self.zones[i]), hr(self.zones[i+1]), facecolor=color, alpha=0.6, label=name)
