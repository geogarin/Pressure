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
        r = self.cursor.execute('SELECT * FROM SensorType WHERE Type = ?',(sensorType,)).fetchone()
        return r

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
    p=d.getChannels()
    print(len(p))
    print(p)
    for r in p:
        print (r['Name'])
        print (r)

