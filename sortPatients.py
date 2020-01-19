from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, IntegerField, validators
from wtforms.validators import DataRequired

class SortPatients(FlaskForm):
    street = StringField('Street', validators=[DataRequired()])
    submit = SubmitField('Search patient')