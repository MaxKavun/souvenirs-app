from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField 
from wtforms.validators import DataRequired

class AddItem(FlaskForm):
    type = StringField('Type of souvenir', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    madeIn = StringField('Where souvenir created', validators=[DataRequired()])
    submit = SubmitField('Submit')