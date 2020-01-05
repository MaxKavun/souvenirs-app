from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired

class AddItem(FlaskForm):
    def __init__(self,producers):
        super(AddItem,self).__init__()
        allProducers = []
        for name in producers:
            allProducers.append((name[0],name[0]))
        self.madeIn.choices = allProducers
    name = StringField('Name', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    madeIn = SelectField('Producer')
    submit = SubmitField('Submit')