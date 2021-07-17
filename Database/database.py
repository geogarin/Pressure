import sqlite3
from datetime import datetime
import usb

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
              Volume = ?,
              ConnectionDuration = ?,
              InflatingDuration = ?,
              StabilizationDuration = ?,
              StrengthTestPressure = ?,
              StrengthTestDuration = ?,
              SealedTestPressure = ?,
              SealedTestDeltaThreshold = ?,
              SealedTestDuration = ?
              where Name=?
        ''',
        (receipt["Enabled"],
         receipt["Volume"],
         receipt["ConnectionDuration"],
         receipt["InflatingDuration"],
         receipt["StabilizationDuration"],
         receipt["StrengthTestPressure"],
         receipt["StrengthTestDuration"],
         receipt["SealedTestPressure"],
         receipt["SealedTestDeltaThreshold"],
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

    def getUsbDevices(self):
        return [device.serial_number for device in usb.core.find(find_all=True) if (device.bDeviceClass==0)]
    
    def getSetupDriveList(self):
        return(self.cursor.execute('select Serial from FlashDrives where Setup=1'))

    def getMasterDriveList(self):
        return(self.cursor.execute('select Serial from FlashDrives where Master=1'))

    def isSetupFlashInstalled(self):
        usbs = self.getUsbDevices()    
        s = [usbDev for usbDev in usbs if usbDev in [rec['Serial'] for rec in self.getSetupDriveList()]]
        return s!=[]
    
    def isMasterFlashInstalled(self):
        usbs = self.getUsbDevices()    
        s = [usbDev for usbDev in usbs if usbDev in [rec['Serial'] for rec in self.getMasterDriveList()]]
        return s!=[]

    def addFlashDrive(self,serial,setup=0,master=0):
        rec = self.cursor.execute('select * from FlashDrives where Serial=?',(serial,)).fetchone()
        if rec is None:
            self.cursor.execute('insert into FlashDrives (Serial,Setup,Master) values (?,?,?)',(serial,setup,master))
        
        #self.cursor.execute('update FlashDrives set Setup=?,Master=? where Serial=?',(setup,master,serial))
        self.connection.commit()
    
    def addSetupFlashDrive(self):
        usbs = self.getUsbDevices()
        for usbDev in usbs:
            self.addFlashDrive(usbDev,1)

    def __del__(self):
        self.connection.close() 

if __name__ == '__main__':
    d = data()

    #p=d.getActiveReceipts()
    #print(f'receipts={len(p)} val0={p[0]["Name"]}')

    t=d.getUsbDevices()
    print(t)
    """
    for usbDev in t:
        d.addFlashDrive(usbDev,1) # setup
        #d.addFlashDrive(usbDev,0,1) # master
    """
    si = d.isSetupFlashInstalled()
    mi = d.isMasterFlashInstalled()
    print(f'isSetup={si} isMaster={mi}')     

    #d.addFlashDrive(t[0])
    """
    #p=d.getChannels()
    #print(len(p))
    #print(p)
    for r in p:
        print (r['Name'])
        print (r)
    """

