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
from sort import SortData as SortDataForm
#from dynamodb import Artifacts
import database

app = Flask(__name__)
app.config['SECRET_KEY'] = "my secret key"
databaseName = 'hospital'
rdsEnvironment = database.CreateEnvironment(databaseName)
bootstrapTemp = Bootstrap(app)
@app.route('/', methods=['GET','POST'])
def index():
    sortForm = SortDataForm()
    rdsGetInfo = database.GetInformationFromDB(databaseName)
    rdsData = rdsGetInfo.requestInformation()
    if sortForm.validate_on_submit():
        nameOfSouvenir = sortForm.souvenir.data
        producer = sortForm.producer.data
        country = sortForm.country.data
        price = sortForm.price.data
        year = sortForm.year.data
        radioBtn = sortForm.sortBy.data
        tmpRdsData = []
        if radioBtn == "Producer" and len(producer) > 0:
            for x in rdsData:
                if x[3] == producer:
                    tmpRdsData.append(x)
            rdsData = tmpRdsData
            flash(radioBtn)
        if radioBtn == "Country" and len(country) > 0:
            for x in rdsData:
                if x[4] == country:
                    tmpRdsData.append(x)
            rdsData = tmpRdsData
            flash(radioBtn)
        if radioBtn == "Price less" and price is not None: 
            for x in rdsData:
                if x[1] < price:
                    tmpRdsData.append(x)
            rdsData = tmpRdsData
            flash(radioBtn)
        if radioBtn == "Year and Producer" and len(nameOfSouvenir) > 0 and year is not None:
            for x in rdsData:
                if x[0] == nameOfSouvenir and x[2] == year:
                    tmpRdsData.append(x)
            rdsData = tmpRdsData
            flash(radioBtn)
        if radioBtn == "Delete producer" and len(producer) > 0:
            rdsRemove = database.DeleteInfo(databaseName)
            rdsRemove.removeProducer(producer)
            flash("Producer with souvenirs was deleted")
            return redirect(url_for('index'))
    return render_template('index.html', souvenirs=rdsData, form=sortForm)

@app.route('/add/souvenir', methods=['GET','POST'])
def user():
    rdsGetInfo = database.GetInformationFromDB(databaseName)
    rdsGetInfoProducers = rdsGetInfo.requestProducers()
    addItem = AddItemForm(rdsGetInfoProducers)
    if addItem.validate_on_submit():
        souvenirName = addItem.name.data
        souvenirPrice = addItem.price.data
        souvenirYear = addItem.year.data
        souvenirProducer = addItem.madeIn.data
        rdsAddSouvenir = database.AddNewInformationToDB(databaseName)
        rdsAddSouvenir.addSouvenir(souvenirName,souvenirPrice,souvenirYear,souvenirProducer)

        return redirect(url_for('user'))
    return render_template('add_item.html', form=addItem)

@app.route('/add/producer', methods=['GET','POST'])
def producer():
    addProducer = AddProducerForm()
    if addProducer.validate_on_submit():
        nameProducer = addProducer.name.data
        countryProducer = addProducer.country.data
        rdsAddProducer = database.AddNewInformationToDB(databaseName)
        rdsAddProducer.addPerson(nameProducer,countryProducer)

    return render_template('add_producer.html', form=addProducer)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404