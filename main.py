from flask import Flask
from flask import redirect
from flask import abort
from flask import render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrapTemp = Bootstrap(app)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    if 'max' not in name:
        abort(404)
    return render_template('user.html', name=name)

@app.route('/google')
def google():
    return redirect('https://google.com')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404