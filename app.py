from datetime import datetime

import pandas as pd
import plotly
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from whitenoise import WhiteNoise

from forms import YearSelectForm

app = Flask(__name__)
Bootstrap(app)
app.wsgi_app = WhiteNoise(app.wsgi_app, root="static/")
app.config["SECRET_KEY"] = "aaaa"


def make_plot(years):
    if years:
        df = pd.concat(map(pd.read_json, years), ignore_index=True)
        df["time"] = df.apply(lambda r: datetime.fromtimestamp(r["time"]), axis=1)
        df = df.sort_values(["time"])

        if len(years) == 1:
            title_time = f"in {years[0].split('_')[1]}"
        else:
            title_years = [int(y.split("_")[1]) for y in years]
            if len(years) == max(title_years) - min(title_years) + 1:
                title_time = f"from {min(title_years)} to {max(title_years)}"
            else:
                title_time = f"in {', '.join([str(y) for y in title_years])}"

        return plotly.offline.plot(
            {
                "data": [
                    plotly.graph_objs.Scatter(
                        x=df.time, y=df.temperature, mode="markers", marker=dict(size=4)
                    )
                ],
                "layout": {
                    "title": f"Temperature History of Calgary at 6 am {title_time}",
                    "xaxis": {"title": "Time"},
                    "yaxis": {"title": "Temperature (Celsius)"},
                },
            },
            auto_open=False,
            output_type="div",
        )
    return None


@app.route("/", methods=["get", "post"])
def index():
    form = YearSelectForm(request.form)
    plot = make_plot(form.year.data)

    return render_template("index.html", form=form, plot=plot)


if __name__ == "__main__":
    app.run(debug=True)
