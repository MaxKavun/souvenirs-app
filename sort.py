from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, IntegerField, validators
from wtforms.validators import DataRequired

class SortData(FlaskForm):
    souvenir = StringField('Souvenir', validators=[])
    producer = StringField('Producer', validators=[])
    country = StringField('Country', validators=[])
    price = IntegerField('Price', validators=[validators.optional()])
    year = IntegerField('Year', validators=[validators.optional()])
    sortBy = RadioField('Label', 
            choices=[('Producer','Producer'),('Country','Country'),
            ('Price less', 'Price less'),('Year and Producer','Year and Souvenir'),
            ('Delete producer','Delete producer')], 
            validators=[DataRequired()])
    submit = SubmitField('Submit')