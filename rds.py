import pymysql
from os import environ

class DatabaseConnection():
    def createConnection(self):
        dbEndpoint = environ['dbEndpoint']
        dbPass = environ['mysqlpass']
        dbCon = pymysql.connect(dbEndpoint,'admin',dbPass,'mysql')
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
            self.dbCursor.execute(queryOwnerCreds)
            self.dbCursor.execute(queryArtifacts)
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

    def requestInformation(self):
        query = "SELECT art.Name,art.Price,art.YearOfMade,ps.Name,ps.Country \
                FROM artifacts as art\
                JOIN persons as ps ON ps.ID = art.OwnerID\
                WHERE 1=1"
        self.dbCursor.execute(query)
        data = self.dbCursor.fetchall()
        self.dbCon.close()
        return data

    def requestProducers(self):
        query = "SELECT Name FROM persons"
        self.dbCursor.execute(query)
        data = self.dbCursor.fetchall()
        self.dbCon.close()
        return data

    def requestProducer(self,producer):
        query = f"SELECT ID FROM persons WHERE Name = '{producer}' LIMIT 1"
        self.dbCursor.execute(query)
        data = self.dbCursor.fetchone()
        self.dbCon.close()
        return data

class AddNewInformationToDB():
    def __init__(self,databaseName):
        self.dbConnection = DatabaseConnection()
        self.dbCon = self.dbConnection.createConnection()
        self.dbCursor = self.dbCon.cursor()
        self.databaseName = databaseName
        self.dbCursor.execute(f"USE {self.databaseName}")

    def addPerson(self,name,country):
        query = f"INSERT INTO persons(Name,Country) VALUES('{name}','{country}')"
        try:
            self.dbCursor.execute(query)
            self.dbCon.commit()
        except:
            self.dbCon.rollback()
        self.dbCon.close()

    def addSouvenir(self,name,price,year,producer):
        getInfo = GetInformationFromDB(self.databaseName)
        idOfProducer = getInfo.requestProducer(producer)
        query = f"INSERT INTO artifacts(Name,Price,YearOfMade,OwnerID) \
                VALUES('{name}',{price},{year},{idOfProducer[0]})"
        try:
            self.dbCursor.execute(query)
            self.dbCon.commit()
        except:
            self.dbCon.rollback()
        self.dbCon.close()
