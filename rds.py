import pymysql
from os import environ

class DatabaseConnection():
    def createConnection(self):
        dbEndpoint = environ['dbEndpoint']
        dbPass = environ['mysqlpass']
        dbCon = pymysql.connect(dbEndpoint,'admin',dbPass,'mysql')
        dbCursor = dbCon.cursor()
        return dbCursor
    
class CreateEnvironment():
    def __init__(self,databaseName):
        self.databaseName = databaseName

    def createDatabase(self,dbCursor):
        try:
            queryDb = f"CREATE DATABASE {databaseName}"
            dbCursor.execute(queryDb)
        except:
            return "Error while creating database"
        return "Database successfully created"

    def createTables(self,dbCursor):
        try:
            dbCursor.execute(f"USE {self.databaseName}")
            queryArtifacts = "CREATE TABLE artifacts (\
                ID int PRIMARY KEY AUTO_INCREMENT,\
                Name varchar(255),\
                Price int,\
                YearOfMade int,\
                OwnerID int,\
                FOREIGN KEY (OwnerID) REFERENCES persons (ID)\
            )"
            queryOwnerCreds = "CREATE TABLE persons (\
                ID int PRIMARY KEY AUTO_INCREMENT,\
                Name varchar(255),\
                Country varchar(255)\
            )"
            dbCursor.execute(queryArtifacts)
            dbCursor.execute(queryOwnerCreds)
        except:
            return "Error while creating table"
        return "Table successfully created"

class GetInformationFromDB():
    def requestInformation(self,dbCursor):
        query = "SELECT * FROM artifacts"
        dbCursor.execute(query)

class AddNewInformationToDB():
    def addInformation(self,dbCursor):
        query = "INSERT INTO persons(FirstName,LastName) VALUES('John','Doe')"
        dbCursor.execute(query)