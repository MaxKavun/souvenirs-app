import pymysql
from os import environ

class DatabaseConnection():
    def createConnection(self):
        dbPass = environ['mysqlpass']
        dbCon = pymysql.connect('souvenirs.cjmiwftdk7qy.eu-north-1.rds.amazonaws.com',
                                'admin',dbPass,'mysql')
        return dbCon
    
class CreateEnvironment():
    def createDatabase(self,dbCon):
        print("Creating database...")

    def createTables(self,dbCon):
        print("Creating tables...")

class GetInformationFromDB():
    def requestInformation(self,dbCon):
        print("Getting information...")

class AddNewInformationToDB():
    def addInformation(self,dbCon):
        print("Adding new information...")