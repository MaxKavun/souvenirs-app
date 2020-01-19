import pymysql
from os import environ
import sys

class DatabaseConnection():
    def createConnection(self):
        #dbEndpoint = environ['dbEndpoint']
        dbEndpoint = '13.48.86.228'
        dbPass = environ['mysqlpass']
        dbCon = pymysql.connect(dbEndpoint,'admin',dbPass,'mysql',3306)
        return dbCon
    
class CreateEnvironment():
    def __init__(self,databaseName):
        self.dbConnection = DatabaseConnection()
        self.dbCon = self.dbConnection.createConnection()
        self.dbCursor = self.dbCon.cursor()
        self.databaseName = databaseName
        self.createDatabase()
        self.createTables()

    def createDatabase(self):
        try:
            queryDb = f"CREATE DATABASE {self.databaseName}"
            self.dbCursor.execute(queryDb)
        except:
            return "Error while creating database"
        return "Database successfully created"

    def createTables(self):
        try:
            self.dbCursor.execute(f"USE {self.databaseName}")
            queryTherapists = "CREATE TABLE therapists (\
                ID int PRIMARY KEY AUTO_INCREMENT,\
                FirstName varchar(255),\
                LastName varchar(255),\
                Speciality varchar(255),\
                Shift varchar(255)\
            )"
            self.dbCursor.execute(queryTherapists)
            queryPatients = "CREATE TABLE patients (\
                ID int PRIMARY KEY AUTO_INCREMENT,\
                FirstName varchar(255),\
                LastName varchar(255),\
                Street varchar(255)\
            )"
            self.dbCursor.execute(queryPatients)
            queryVisits = "CREATE TABLE visits (\
                ID int PRIMARY KEY AUTO_INCREMENT,\
                Date DATE,\
                Reason varchar(255),\
                PatientID int,\
                TherapistID int,\
                FOREIGN KEY (PatientID) REFERENCES patients (ID),\
                FOREIGN KEY (TherapistID) REFERENCES therapists (ID)\
            )"
            self.dbCursor.execute(queryVisits)
        except:
            return "Error while creating table"
        self.dbCon.close()
        return "Table successfully created"

class GetInformationFromDB():
    def __init__(self,databaseName):
        self.dbConnection = DatabaseConnection()
        self.databaseName = databaseName
        self.dbCon = self.dbConnection.createConnection()
        self.dbCursor = self.dbCon.cursor()
        self.dbCursor.execute(f"USE {self.databaseName}")

    def getAllVisits(self):
        query = "SELECT vst.Date, vst.Reason, CONCAT(pt.FirstName,' ',pt.LastName), \
                CONCAT(tr.FirstName,' ',tr.LastName)\
                FROM visits as vst\
                JOIN patients as pt ON pt.ID = vst.PatientID\
                JOIN therapists as tr ON tr.ID = vst.TherapistID"
        self.dbCursor.execute(query)
        data = self.dbCursor.fetchall()
        self.dbCon.close()
        return data

    def requestPatients(self,allInformation=False):
        if allInformation==False:
            query = "SELECT CONCAT(FirstName,' ',LastName) FROM patients"
        else:
            query = "SELECT FirstName,LastName,Street FROM patients"
        self.dbCursor.execute(query)
        data = self.dbCursor.fetchall()
        return data

    def requestPatient(self,patient):
        query = f"SELECT ID FROM patients \
        WHERE FirstName='{patient[0]}' AND LastName='{patient[1]}'"
        self.dbCursor.execute(query)
        data = self.dbCursor.fetchone()
        return data

    def requestTherapists(self,allInformation=False):
        if allInformation==False:
            query = "SELECT CONCAT(FirstName,' ',LastName,' ',Speciality) FROM therapists"
        else:
            query = "SELECT FirstName,LastName,Speciality,Shift FROM therapists"
        self.dbCursor.execute(query)
        data = self.dbCursor.fetchall()
        self.dbCon.close()
        print(data, file=sys.stdout)
        return data

class AddNewInformationToDB():
    def __init__(self,databaseName):
        self.dbConnection = DatabaseConnection()
        self.dbCon = self.dbConnection.createConnection()
        self.dbCursor = self.dbCon.cursor()
        self.databaseName = databaseName
        self.dbCursor.execute(f"USE {self.databaseName}")

    def addTherapist(self,firstName,lastName,speciality,shift):
        query = f"INSERT INTO therapists(firstName,lastName,speciality,shift) \
        VALUES('{firstName}','{lastName}','{speciality}','{shift}')"
        try:
            self.dbCursor.execute(query)
            self.dbCon.commit()
        except:
            self.dbCon.rollback()
        self.dbCon.close()

    def addPatient(self,firstName,lastName,street):
        query = f"INSERT INTO patients(FirstName,LastName,Street) VALUES('{firstName}','{lastName}','{street}')"
        try:
            self.dbCursor.execute(query)
            self.dbCon.commit()
        except:
            self.dbCon.rollback()
        self.dbCon.close()


    def addEncounter(self,date,reason,patient,therapist):
        getPatientID = GetInformationFromDB(self.databaseName)
        patientID = getPatientID.requestPatient(patient)
        query = f"INSERT INTO visits(Date,Reason,PatientID,TherapistID)\
                  SELECT '{date}','{reason}',{patientID[0]},ID FROM therapists\
                  WHERE FirstName='{therapist[0]}' and LastName='{therapist[1]}' \
                  and Speciality='{therapist[2]}'"
        try:
            self.dbCursor.execute(query)
            self.dbCon.commit()
        except:
            self.dbCon.rollback()
        self.dbCon.close()

class DeleteInfo():
    def __init__(self,databaseName):
        self.dbConnection = DatabaseConnection()
        self.dbCon = self.dbConnection.createConnection()
        self.dbCursor = self.dbCon.cursor()
        self.databaseName = databaseName
        self.dbCursor.execute(f"USE {self.databaseName}")

    def removePatientsOlder20Years(self):
        queryGetPatients = f"SELECT PatientID FROM visits \
        WHERE visits.Date < DATE_SUB(NOW(), INTERVAL 20 YEAR)"
        self.dbCursor.execute(queryGetPatients)
        patients = self.dbCursor.fetchall()
        for patient in patients:
            queryCheckPatient = f"SELECT ID FROM visits \
                                where PatientID = {patient[0]} AND \
                                Date > DATE_SUB(NOW(), INTERVAL 20 YEAR)"
            self.dbCursor.execute(queryCheckPatient)
            result = self.dbCursor.fetchall()
            if len(result) > 0:
                continue
            queryPatients = f"DELETE FROM visits WHERE \
                            PatientID = {patient[0]}"
            self.dbCursor.execute(queryPatients)
            queryDeletePatient = f"DELETE FROM patients WHERE ID = {patient[0]}"
            self.dbCursor.execute(queryDeletePatient)
        self.dbCon.commit()
        self.dbCon.close()
        return self.dbCursor.fetchone()