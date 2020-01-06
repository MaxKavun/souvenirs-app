from flask import Flask
from flask import redirect
from flask import abort
from flask import render_template
from flask import session
from flask import url_for
from flask import flash
from flask_bootstrap import Bootstrap
from additem import AddItem as AddItemForm
from addproducer import AddProducer as AddProducerForm
#from dynamodb import Artifacts
import rds

app = Flask(__name__)
app.config['SECRET_KEY'] = "my secret key"
databaseName = 'souvenirs'
rdsEnvironment = rds.CreateEnvironment(databaseName)
bootstrapTemp = Bootstrap(app)
@app.route('/')
def index():
    rdsGetInfo = rds.GetInformationFromDB(databaseName)
    rdsData = rdsGetInfo.requestInformation()
    return render_template('index.html', souvenirs=rdsData)

@app.route('/add/souvenir', methods=['GET','POST'])
def user():
    rdsGetInfo = rds.GetInformationFromDB(databaseName)
    rdsGetInfoProducers = rdsGetInfo.requestProducers()
    addItem = AddItemForm(rdsGetInfoProducers)
    if addItem.validate_on_submit():
        souvenirName = addItem.name.data
        souvenirPrice = addItem.price.data
        souvenirYear = addItem.year.data
        souvenirProducer = addItem.madeIn.data
        rdsAddSouvenir = rds.AddNewInformationToDB(databaseName)
        rdsAddSouvenir.addSouvenir(souvenirName,souvenirPrice,souvenirYear,souvenirProducer)

        return redirect(url_for('user'))
    return render_template('add_item.html', form=addItem)

@app.route('/add/producer', methods=['GET','POST'])
def producer():
    addProducer = AddProducerForm()
    if addProducer.validate_on_submit():
        nameProducer = addProducer.name.data
        countryProducer = addProducer.country.data
        rdsAddProducer = rds.AddNewInformationToDB(databaseName)
        rdsAddProducer.addPerson(nameProducer,countryProducer)

    return render_template('add_producer.html', form=addProducer)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404