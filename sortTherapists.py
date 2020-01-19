from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, validators, RadioField
from wtforms.validators import DataRequired

class SortTherapists(FlaskForm):
    allShifts = [('Night', 'Night'), ('Day', 'Day'), ('Middle', 'Middle')]
    speciality = StringField('Speciality')
    shift = SelectField('Shift', choices=allShifts)
    sortBy = RadioField('Label', 
            choices=[('Speciality','Speciality'),('Shift','Shift')],
            validators=[DataRequired()])
    submit = SubmitField('Search therapist')