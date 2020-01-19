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
from addencounter import AddEncounter as AddEncounterForm
from sort import SortData as SortDataForm
#from dynamodb import Artifacts
import database
import sys

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
        dbRemovePatients = database.DeleteInfo(databaseName)
        dbRemovePatients.removePatientsOlder20Years()
        flash("Patients with visits older than 20 years were deleted")
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

@app.route('/add/encounter', methods=['GET','POST'])
def encounter():
    dbConn = database.GetInformationFromDB(databaseName)
    getAllPatients = dbConn.requestPatients()
    getAllTherapists = dbConn.requestTherapists()
    addEncounter = AddEncounterForm(getAllPatients,getAllTherapists)
    if addEncounter.validate_on_submit():
        date = addEncounter.date.data.strftime('%Y-%m-%d')
        reason = addEncounter.reason.data
        patient = addEncounter.patient.data.split(' ')
        therapist = addEncounter.therapist.data.split(' ')
        dbConn = database.AddNewInformationToDB(databaseName)
        dbConn.addEncounter(date,reason,patient,therapist)
        return redirect(url_for('encounter'))

    return render_template('add_encounter.html', form=addEncounter)

@app.route('/show/therapists', methods=['GET','POST'])
def getTherapist():
    dbConn = database.GetInformationFromDB(databaseName)
    getAllPatients = dbConn.requestPatients()
    getAllTherapists = dbConn.requestTherapists()
    addEncounter = AddEncounterForm(getAllPatients,getAllTherapists)
    if addEncounter.validate_on_submit():
        date = addEncounter.date.data.strftime('%Y-%m-%d')
        reason = addEncounter.reason.data
        patient = addEncounter.patient.data.split(' ')
        therapist = addEncounter.therapist.data.split(' ')
        dbConn = database.AddNewInformationToDB(databaseName)
        dbConn.addEncounter(date,reason,patient,therapist)
        return redirect(url_for('getTherapist'))

    return render_template('therapists.html', form=addEncounter)

@app.route('/show/patients', methods=['GET','POST'])
def getPatient():
    dbConn = database.GetInformationFromDB(databaseName)
    getAllPatients = dbConn.requestPatients()
    getAllTherapists = dbConn.requestTherapists()
    addEncounter = AddEncounterForm(getAllPatients,getAllTherapists)
    if addEncounter.validate_on_submit():
        date = addEncounter.date.data.strftime('%Y-%m-%d')
        reason = addEncounter.reason.data
        patient = addEncounter.patient.data.split(' ')
        therapist = addEncounter.therapist.data.split(' ')
        dbConn = database.AddNewInformationToDB(databaseName)
        dbConn.addEncounter(date,reason,patient,therapist)
        return redirect(url_for('getTherapist'))

    return render_template('patients.html', form=addEncounter)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404