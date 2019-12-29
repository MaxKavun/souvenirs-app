from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField 
from wtforms.validators import DataRequired

class AddItem(FlaskForm):
    type = StringField('Type of your item', validators=[DataRequired()])
    name = StringField('What is your item?', validators=[DataRequired()])
    submit = SubmitField('Submit')