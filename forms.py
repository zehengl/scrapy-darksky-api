from pathlib import Path
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField
from wtforms.validators import DataRequired

path = Path(".")
forcast = sorted(path.glob("data/forcast_*.json"), reverse=True)
choices = [(p, p) for p in forcast]


class YearSelectForm(FlaskForm):
    year = SelectMultipleField(
        f"Available Data ({len(choices)} years, multiple selectable)",
        choices=choices,
        validators=[DataRequired()],
    )
    submit = SubmitField("Make Plot")
