from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, IntegerField, validators
from wtforms.validators import DataRequired

class SortData(FlaskForm):
    submit = SubmitField('Delete all patients with date of visit > 20 years')