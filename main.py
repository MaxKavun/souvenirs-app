from flask import Flask
from flask import redirect
from flask import abort
from flask import render_template
from flask import session
from flask import url_for
from flask import flash
from flask_bootstrap import Bootstrap
from additem import AddItem as AddItemForm
from dynamodb import Artifacts

app = Flask(__name__)
app.config['SECRET_KEY'] = "my secret key"
bootstrapTemp = Bootstrap(app)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET','POST'])
def user():
    addItem = AddItemForm()
    artifactsTable = Artifacts()
    if addItem.validate_on_submit():
        nameOfItem = artifactsTable.getItem(addItem.type.data,addItem.name.data)
        if nameOfItem is None:
            artifactsTable.addItem(addItem.type.data,addItem.name.data)
            flash("Looks like you have added a new item")
        else:
            session['name'] = addItem.name.data
        return redirect(url_for('user'))
    return render_template('add_item.html', form=addItem, name=session.get('name'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404