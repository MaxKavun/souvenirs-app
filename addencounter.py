from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired
import sys

class AddEncounter(FlaskForm):
    def __init__(self,patients,therapists):
        super(AddEncounter,self).__init__()
        curPatients = []
        curTherapists = []
        for name in patients:
            curPatients.append((name[0],name[0]))
        for name in therapists:
            curTherapists.append((name[0],name[0]))
        self.patient.choices = curPatients
        self.therapist.choices = curTherapists
    date = DateField('Date format 1970-01-30', format='%Y-%m-%d', validators=[DataRequired()])
    reason = StringField('Reason', validators=[DataRequired()])
    patient = SelectField('Patient (First name, Last name)')
    therapist = SelectField('Therapist (First name, Last name, Speciality)')
    submit = SubmitField('Submit')