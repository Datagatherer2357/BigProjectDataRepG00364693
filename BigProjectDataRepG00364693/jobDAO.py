# DAO that facilitates interaction with SQL database

import mysql.connector
import dbconfig as cfg # import configurations
class JobDAO:
    db=""
    def __init__(self): 
        self.db = mysql.connector.connect(
         host=cfg.mysql['host'],
          user=cfg.mysql['user'],
          password=cfg.mysql['password'],
          database=cfg.mysql['database']
        )
    
            
    def create(self, values):
        cursor = self.db.cursor()
        sql="insert into job (location, jobTitle, company, salary) values (%s,%s,%s,%s)"
        cursor.execute(sql, values)

        self.db.commit()
        return cursor.lastrowid

    def getAll(self):
        cursor = self.db.cursor()
        sql="select * from job"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        print(results)
        for result in results:
            print(result)
            returnArray.append(self.convertToDictionary(result))

        return returnArray

    def findByID(self, id):
        cursor = self.db.cursor()
        sql="select * from job where id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        return self.convertToDictionary(result)

    def update(self, values):
        cursor = self.db.cursor()
        sql="update job set location= %s, jobTitle=%s, company=%s, salary=%s  where id = %s"
        cursor.execute(sql, values)
        self.db.commit()
    def delete(self, id):
        cursor = self.db.cursor()
        sql="delete from job where id = %s"
        values = (id,)

        cursor.execute(sql, values)

        self.db.commit()
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