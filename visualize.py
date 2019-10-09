#%%
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

path = Path(".")
result = Path("result")
result.mkdir(exist_ok=True)

df = pd.concat(map(pd.read_json, path.glob("forcast_*.json")), ignore_index=True)

df["time"] = df.apply(lambda r: datetime.fromtimestamp(r["time"]), axis=1)


#%%
plt.clf()
ax = sns.countplot(x="icon", data=df)
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
for p in ax.patches:
    height = p.get_height()
    ax.text(
        p.get_x() + p.get_width() / 2.0,
        height,
        f"{height/ df.shape[0] * 100:.2f}%",
        ha="center",
    )
ax.get_figure().savefig(result / "icon-countplot.png")


#%%
plt.clf()
ax = sns.scatterplot(x="time", y="temperature", s=2, data=df)
ax.set(xlim=(min(df["time"]), max(df["time"])))
print(ax.get_xticklabels())
ax.get_figure().savefig(result / "temperature-scatterplot.png")


#%%
plt.clf()
ax = sns.scatterplot(x="time", y="pressure", s=2, data=df)
ax.set(xlim=(min(df["time"]), max(df["time"])))
ax.get_figure().savefig(result / "pressure-scatterplot.png")

#%%
plt.clf()
ax = sns.jointplot(x="temperature", y="pressure", kind="hex", data=df)

ax.fig.savefig(result / "temperature-pressure-jointplot.png")


#%%
plt.clf()
ax = sns.pairplot(
    vars=["wind_speed", "wind_gust", "humidity", "pressure", "temperature"],
    plot_kws={"s": 2},
    data=df,
)
ax.fig.savefig(result / "pairplot.png")
