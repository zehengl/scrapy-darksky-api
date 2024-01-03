from pathlib import Path

from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField
from wtforms.validators import DataRequired

path = Path(".")
forecast = sorted(path.glob("data/forecast_*.json"), reverse=True)
choices = [(p, p) for p in forecast]


class YearSelectForm(FlaskForm):
    year = SelectMultipleField(
        f"Available Data ({len(choices)} years, multiple selectable)",
        choices=choices,
        validators=[DataRequired()],
    )
    submit = SubmitField("Make Plot")
