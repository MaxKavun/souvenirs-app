from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired

class AddItem(FlaskForm):
    type = StringField('Type of souvenir', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    madeIn = SelectField('Where its made', choices=[('Belarus', 'Belarus')])
    submit = SubmitField('Submit')