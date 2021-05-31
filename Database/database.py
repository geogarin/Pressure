import sqlite3
from datetime import datetime

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from Config import DATABASE_PATH,DATABASE_NAME


class data():
    def __init__(self):   
        self.connection = sqlite3.connect(DATABASE_PATH+DATABASE_NAME)
        self.connection.row_factory = sqlite3.Row
        self.connection.isolation_level = None
        self.cursor = self.connection.cursor()

    def getChannels(self):
        msgs = self.cursor.execute('select * from Channels where Enabled=1').fetchall()
        #return [list(row) for row in msgs]
        return msgs

    def getSensorParameters(self,sensorType):
        r = self.cursor.execute('select * from SensorType where Type = ?',(sensorType,)).fetchone()
        return r

    def getSetup(self):
        r = self.cursor.execute('select * from Setup where Entry = 0').fetchone()
        return r
    
    def saveSetup(self,fieldName,fieldValue):
        r = self.cursor.execute('update Setup set '+fieldName+' = ? where Entry = 0',(fieldValue,))

    def getReceipt(self,name):
        r = self.cursor.execute('select * from Receipts where Name=?',(name,)).fetchone()
        return r

    def saveReceipt(self,receipt):
        r = self.cursor.execute('select * from Receipts where Name=?',(receipt["Name"],)).fetchone()
        if r is None:
            self.cursor.execute('insert into Receipts (Name) values (?)',(receipt["Name"],))
        #print(receipt)
        self.cursor.execute('''update Receipts set
              Enabled = ?,
              ConnectionDuration = ?,
              InflatingDuration = ?,
              StabilizationDuration = ?,
              StrengthTestPressure = ?,
              StrengthTestDuration = ?,
              SealedTestPressure = ?,
              SealedTestDuration = ?
              where Name=?
        ''',
        (receipt["Enabled"],
         receipt["ConnectionDuration"],
         receipt["InflatingDuration"],
         receipt["StabilizationDuration"],
         receipt["StrengthTestPressure"],
         receipt["StrengthTestDuration"],
         receipt["SealedTestPressure"],
         receipt["SealedTestDuration"],
         receipt["Name"])
        )
        self.connection.commit()

    def deleteReceipt(self,name):
        self.cursor.execute('delete from Receipts where Name=?',(name,))
        self.connection.commit()

    def getReceipts(self):
        r = self.cursor.execute('select * from Receipts').fetchall()
        return r

    def getEnabledReceipts(self):
        r = self.cursor.execute('select * from Receipts where Enabled=1').fetchall()
        return r
    
    def saveReceipts(self,receiptName,fieldName,fieldValue):
        r = self.cursor.execute('update Receipts set '+ fieldName+'=? where Name=?',(fieldValue,receiptName))


    def __del__(self):
        self.connection.close() 
"""            
    def new_user(self,user_id: int,username: str):
        self.cursor.execute('SELECT * FROM users WHERE user_id = ?',(user_id,))
        if self.cursor.fetchone() is None:
            self.cursor.execute('INSERT INTO users VALUES(?,?,?,?)',(user_id,username,'main',1))
        else:
            pass
"""

if __name__ == '__main__':
    d = data()

    p=d.getActiveReceipts()
    print(f'receipts={len(p)} val0={p[0]["Name"]}')



    p=d.getChannels()
    print(len(p))
    print(p)
    for r in p:
        print (r['Name'])
        print (r)

