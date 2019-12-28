from flask import Flask
from flask import redirect
from flask import abort
from flask import render_template
from flask import session
from flask import url_for
from flask import flash
from flask_bootstrap import Bootstrap
from additem import AddItem

app = Flask(__name__)
app.config['SECRET_KEY'] = "my secret key"
bootstrapTemp = Bootstrap(app)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET','POST'])
def user():
    addItem = AddItem()
    if addItem.validate_on_submit():
        oldName = session.get('name')
        if oldName is not None and oldName != addItem.name.data:
            flash("Looks like you have changed item")
        session['name'] = addItem.name.data
        return redirect(url_for('user'))
    return render_template('user.html', form=addItem, name=session.get('name'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404