# DAO that facilitates interaction with SQL database

import mysql.connector
import dbconfig as cfg # import configurations
class JobDAO:
    db=""
    def connectToDB(self):
        self.db = mysql.connector.connect(
            host=       cfg.mysql['host'],
            user=       cfg.mysql['user'],
            password=   cfg.mysql['password'],
            database=   cfg.mysql['database']
        )
    def __init__(self): 
        self.connectToDB()
     
    
    def getCursor(self):
        if not self.db.is_connected():
            self.connectToDB()
        return self.db.cursor()
    
            
    def create(self, values):
        cursor = self.getCursor()
        sql="insert into job (location, jobTitle, company, salary) values (%s,%s,%s,%s)"
        cursor.execute(sql, values)
        db.commit()
        lastRowId=cursor.lastrowid
        cursor.close
        return lastRowId

    def getAll(self):
        cursor = self.getCursor()
        sql="select * from job"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
     #  print(results)
        for result in results:
            print(result)
            returnArray.append(self.convertToDictionary(result))
        cursor.close
        return returnArray

    def findByID(self, id):
        cursor = self.getCursor()
        sql="select * from job where id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        job=self.convertToDictionary(result)
        cursor.close()
        return job

    def update(self, values):
        cursor = self.getCursor()
        sql="update job set location= %s, jobTitle=%s, company=%s, salary=%s  where id = %s"
        cursor.execute(sql, values)
        db.commit()
        cursor.close()

    def delete(self, id):
        cursor = self.getCursor()
        sql="delete from job where id = %s"
        values = (id,)

        cursor.execute(sql, values)

        db.commit()
        cursor.close()
        print("delete done")

    def convertToDictionary(self, result):
        colnames=['id','location','jobTitle', 'company', 'salary']
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item
        
jobDAO = JobDAO()