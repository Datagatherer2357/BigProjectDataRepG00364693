# Connection pooling DAO that facilitates increased traffic SQL database

import mysql.connector
import dbconfig as cfg # import configurations

class JobDAO:
    db=""
    def initConnectToDB(self):
        db = mysql.connector.connect(
            host=       cfg.mysql['host'],
            user=       cfg.mysql['user'],
            password=   cfg.mysql['password'],
            database=   cfg.mysql['database'],
            pool_name='my_connection_pool',
            pool_size=10
        )
        return db
    
    def getConnection(self):
        db = mysql.connector.connect(
            pool_name= 'my_connection_pool' # open up connection
        )
        return db

    def __init__(self): # initial connection
        db=self.initConnectToDB()
        db.close()
       
            
    def create(self, values):
        db = self.getConnection()
        cursor = db.cursor()
        sql="insert into job (location, jobTitle, company, salary) values (%s,%s,%s,%s)"
        cursor.execute(sql, values)
        self.db.commit()
        lastRowId=cursor.lastrowid
        db.close
        return lastRowId

    def getAll(self):
        db = self.getConnection()
        cursor = db.cursor()
        sql="select * from job"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
     #  print(results)
        for result in results:
            print(result)
            returnArray.append(self.convertToDictionary(result))
        db.close
        return returnArray

    def findByID(self, id):
        db = self.getConnection()
        cursor = db.cursor()
        sql="select * from job where id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        job=self.convertToDictionary(result)
        db.close()
        return job

    def update(self, values):
        db = self.getConnection()
        cursor = db.cursor()
        sql="update job set location= %s, jobTitle=%s, company=%s, salary=%s  where id = %s"
        cursor.execute(sql, values)
        self.db.commit()
        db.close()

    def delete(self, id):
        db = self.getConnection()
        cursor = db.cursor()
        sql="delete from job where id = %s"
        values = (id,)
        cursor.execute(sql, values)
        self.db.commit()
        db.close()
     #  print("delete done")

    def convertToDictionary(self, result):
        colnames=['id','location','jobTitle', 'company', 'salary']
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item
        
jobDAO = JobDAO()