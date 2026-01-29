import pandas as pd
import numpy as np


class Athlete:
    def __init__(self, *, is_female=True, age=30, css=1.0, hr_max=None, vo2_max=50, weight=70, hr_rest=50, ftp=200, v_max=20):
        # Basic
        self.is_female = is_female
        self.hr_max = hr_max if hr_max is not None else 220-age   # bpm
        self.hr_rest = hr_rest          # bpm
        self.weight = weight            # kg
        # Performance
        self.vo2_max = vo2_max           # ml /kg / min
        self.ftp = ftp                   # Watts
        self.vma = self.vo2_max / 3.5    # km/h
        self.css = css                   # m/s
        self.v_max = v_max               # km/h
        self.ASR = self.v_max - self.vma # km/h
        # Zones and efforts
        self.zones = [0.0, 0.6, 0.7, 0.8, 0.9, 1.05]
        self.trimp_a, self.trimp_b = (0.86, 1.67) if self.is_male else (0.64, 1.92)

    @property
    def is_male(self):
        return not self.is_female

    def trimp_from_df(self, df):
        df["IFC"] = (df["avg_hr"]-self.hr_rest) / (self.hr_max-self.hr_rest)
        df["k"] = self.trimp_a * np.exp(self.trimp_b * df["IFC"])
        return df["elapsed_s"] / 60 * df["k"] * df["IFC"]

    def trimp(self, t_min, hr_mean):
        IFC = (hr_mean - self.hr_rest) / (self.hr_max - self.hr_rest)
        k = self.trimp_a * np.exp(self.trimp_b * IFC)
        return k * t_min * IFC

    def get_hr_zone_ts(self, hr):
        return pd.cut(hr, bins=self.zones, labels=["Z1", "Z2", "Z3", "Z4", "Z5"], right=False)

    def plot_hr_zone(self, athlete, df):
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(14, 5))
        # Karvonen formula
        hr = lambda x: x * (self.hr_max - self.hr_rest) + self.hr_rest
        for i, name, color in zip(range(5),
                                  ["Z1 - Very light", "Z2 - Light", "Z3 - Moderate", "Z4 - Hard", "Z5 - Maximum"],
                                  ["#dddddd", "#b5d6ea", "#7fd47f", "#f0b04a", "#e05b4f"]):
            ax.axhspan(hr(self.zones[i]), hr(self.zones[i+1]), facecolor=color, alpha=0.6, label=name)
        # HR time-series
        avg_hr = df["heart_rate"].mean()
        trimp = athlete.trimp(df.index[-1], avg_hr)
        ax.plot(df.index, df["heart_rate"], color="red", linewidth=1.4, label=f"Heart rate (Avg HR = {avg_hr:.1f} trimp={trimp:.0f})")
        ax.axhline(avg_hr, color="purple", linestyle="--", linewidth=1, alpha=0.8)
        # Formatting
        ax.set_title("Heart Rate with Training Zones", fontsize=16)
        ax.set_ylabel("HR (bpm)")
        ax.set_xlabel("Time")
        ax.set_ylim(0, athlete.hr_max * 1.05)
        ax.legend()

