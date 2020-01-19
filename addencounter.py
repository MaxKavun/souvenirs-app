from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class AddProducer(FlaskForm):
    allCountries = [('Belarus', 'Belarus'), ('Russia', 'Russia'), ('USA', 'USA')]
    name = StringField('Name of producer', validators=[DataRequired()])
    #country = StringField('Country', validators=[DataRequired()])
    country = SelectField('Country', choices=allCountries)
    submit = SubmitField('Submit')