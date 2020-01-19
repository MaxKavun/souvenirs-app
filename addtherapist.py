from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class AddTherapist(FlaskForm):
    allShifts = [('Night', 'Night'), ('Day', 'Day'), ('Middle', 'Middle')]
    firstName = StringField('First name', validators=[DataRequired()])
    lastName = StringField('Last name', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    shift = SelectField('Shift', choices=allShifts)
    submit = SubmitField('Submit')