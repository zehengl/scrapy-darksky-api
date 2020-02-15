#%%
from datetime import datetime
from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

data = Path("data")
result = Path("result")
static = Path("static")
result.mkdir(exist_ok=True)

df = pd.concat(map(pd.read_json, data.glob("forecast_*.json")), ignore_index=True)

df["time"] = df.apply(lambda r: datetime.fromtimestamp(r["time"]), axis=1)
df["precip_type"] = df.apply(lambda r: r["precip_type"] or "none", axis=1)

cat_attrs = ["icon", "precip_type"]
num_attrs = [
    "cloud_cover",
    "dew_point",
    "humidity",
    "precip_accumulation",
    "precip_intensity",
    "precip_probability",
    "pressure",
    "temperature",
    "visibility",
    "wind_bearing",
    "wind_gust",
    "wind_speed",
]


#%%
for x in cat_attrs:
    plt.clf()
    ax = sns.countplot(x=x, data=df)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
    for p in ax.patches:
        height = p.get_height()
        ax.text(
            p.get_x() + p.get_width() / 2.0,
            height,
            f"{height/ df.shape[0] * 100:.2f}%",
            ha="center",
        )
    ax.get_figure().savefig(result / f"countplot-{x}.png", bbox_inches="tight")


#%%
for y in num_attrs + cat_attrs:
    plt.clf()
    ax = sns.scatterplot(x="time", y=y, s=4, data=df)
    ax.set(xlim=(min(df["time"]), max(df["time"])))
    num_ticks = len(ax.get_xticklabels())
    date_range = pd.date_range(min(df["time"]), max(df["time"]), num_ticks + 2)
    xtick_labels = [d.strftime("%y-%m-%d") for d in date_range[1:-1]]
    ax.set_xticklabels(xtick_labels, rotation=40, ha="right", fontsize=7)
    ax.get_figure().savefig(
        result / f"scatterplot-{y}-over-time.png", bbox_inches="tight"
    )


#%%
for x, y in combinations(num_attrs, 2):
    plt.clf()
    ax = sns.jointplot(x=x, y=y, kind="hex", data=df)
    ax.fig.savefig(result / f"jointplot-{x}-{y}.png")
    if "temperature" in [x, y]:
        ax.fig.savefig(static / f"jointplot-{x}-{y}.png")


#%%
plt.clf()
ax = sns.pairplot(vars=num_attrs, plot_kws={"s": 4}, data=df)
ax.fig.savefig(result / "pairplot.png")
