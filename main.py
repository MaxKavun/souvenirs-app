from flask import Flask
from flask import redirect
from flask import abort
from flask import render_template
from flask import session
from flask import url_for
from flask import flash
from flask_bootstrap import Bootstrap
from addpatient import AddPatient as AddPatientForm
from addtherapist import AddTherapist as AddTherapistForm
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
    dbGetInfo = database.GetInformationFromDB(databaseName)
    allVisits = dbGetInfo.getAllVisits()
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
    return render_template('index.html', visits=allVisits, form=sortForm)

@app.route('/add/patient', methods=['GET','POST'])
def patient():
    addPatient = AddPatientForm()
    if addPatient.validate_on_submit():
        firstName = addPatient.firstName.data
        lastName = addPatient.lastName.data
        street = addPatient.street.data
        dbAddPatient = database.AddNewInformationToDB(databaseName)
        dbAddPatient.addPatient(firstName,lastName,street)
        return redirect(url_for('patient'))

    return render_template('add_patient.html', form=addPatient)

@app.route('/add/therapist', methods=['GET','POST'])
def therapist():
    addTherapist = AddTherapistForm()
    if addTherapist.validate_on_submit():
        firstName = addTherapist.firstName.data
        lastName = addTherapist.lastName.data
        speciality = addTherapist.speciality.data
        shift = addTherapist.shift.data
        dbAddTherapist = database.AddNewInformationToDB(databaseName)
        dbAddTherapist.addTherapist(firstName,lastName,speciality,shift)
        return redirect(url_for('therapist'))

    return render_template('add_therapist.html', form=addTherapist)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404