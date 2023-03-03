from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="scrapy-darksky-api", page_icon=":umbrella_with_rain_drops:"
)
_, center, _ = st.columns([2, 1, 2])
with center:
    st.image(
        "https://cdn3.iconfinder.com/data/icons/ballicons-reloaded-free/512/icon-59-512.png",
        use_column_width=True,
    )
st.title("scrapy-darksky-api")
st.caption("A scrapy app to crawl weather data from Dark Sky Api")

path = Path(".")
forecasts = sorted(path.glob("data/forecast_*.json"), reverse=True)
choices = [p.name for p in forecasts]

years = st.multiselect(
    f"Available Data ({len(choices)} years, multiple selectable)",
    ["all"] + choices,
)

if years:
    if "all" in years:
        years = choices

    years = sorted(years)
    if len(years) == 1:
        title_time = f"in {years[0].split('_')[1]}"
    else:
        title_years = [int(y.split("_")[1]) for y in years]
        if len(years) == max(title_years) - min(title_years) + 1:
            title_time = f"from {min(title_years)} to {max(title_years)}"
        else:
            title_time = f"in {', '.join([str(y) for y in title_years])}"

    df = pd.concat(map(pd.read_json, [f"data/{y}" for y in years]), ignore_index=True)
    df["time"] = df.apply(lambda r: datetime.fromtimestamp(r["time"]), axis=1)
    df = df.sort_values(["time"])

    st.caption(f"Temperature History of Calgary at 6 am {title_time}")
    fig = px.scatter(
        df,
        x="time",
        y="temperature",
        labels={
            "time": "Time",
            "temperature": "Temperature (Celsius)",
        },
    )
    fig

    st.markdown("---")

    path = Path("static")
    url = "https://raw.githubusercontent.com/zehengl/scrapy-darksky-api/main/static"

    st.caption(f"Jointplots")
    for f in sorted(list(path.glob("jointplot-*.png"))):
        st.markdown(f"![]({url}/{f.name})")

    st.caption(f"Time Series Analysis")
    st.markdown(f"![]({url}/time-series-analysis.png)")
