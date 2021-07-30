from PyQt5.QtCore import QObject, QThread, pyqtSignal
from time import sleep
from datetime import datetime
import xlsxwriter
from Database.database import data
import Config
import os
import shutil

class TestResultExporter(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)
    def __init__(self,testsQuantity):
        super().__init__()
        self.testQuantity = testsQuantity

    def run(self):
        d = data()

        self.progress.emit(Config.RES_EXPORT_INIT_USB)

        os.popen("pumount /media/gga")
        usbFlashMounted = self.isUsbMounted()
        if not usbFlashMounted:
            req=os.popen('ls /dev/sd*').read()
            r= req.splitlines()
            
            if not r is None:
                s=str.format("pmount {} /media/gga",r[0])
                os.popen(s).read()
                
                while not usbFlashMounted:
                    sleep(1)
                    usbFlashMounted = self.isUsbMounted()


        if usbFlashMounted:
            dt = datetime.now()
            #cp /media/pi/DEE1-0D94/RaspberryData.json /home/pi/Documents/SmartHome/Data/
            fn = str.format('Export_{}.xlsx',dt.strftime('%d_%m_%Y_%H_%M'))
            cp = str.format('cp /home/gga/Pressure/Export/{} /media/gga/',fn)
            dl = str.format('rm -f Export/{}',fn)
            workbook = xlsxwriter.Workbook('Export/'+fn)
            worksheet = workbook.add_worksheet()

            channels = d.getChannels()
            channelsQty = len(channels)

            testRes = d.getTestResults(channelsQty*self.testQuantity)

            i = 0
            for col in range(len(Config.RES_COLUMN_NAMES)):
                worksheet.write(0,col,Config.RES_COLUMN_NAMES[col])

            for row in range(len(testRes)):
                for col in range(len(Config.RES_COLUMN_NAMES)):
                    worksheet.write(row+1,col,self.formatTestResultData(testRes[row],col))
                if row % channelsQty == 0:
                    self.progress.emit(str(i + 1))
                    i += 1


            workbook.close()
            os.popen(cp)
            #/home/gga/Pressure/Export/{} /media/gga/',fn
            #shutil.copyfile('/home/gga/Pressure/%s' % fn, '/media/gga/export/%s' %fn)
            #sleep(1)
            os.popen(dl)
            #sleep(1)
            os.popen("pumount /media/gga")
        self.finished.emit()

    def isUsbMounted(self):
        s='ls /media/gga'
        r=os.popen(s).read()
        return len(r)>0
    
    def formatTestResultData(self,tableData,column):
        res = tableData[column+1]
        if column==0:
            res = datetime.strptime(res,'%Y-%m-%d %H:%M:%S.%f').strftime('%d.%m.%y %H:%M:%S')
        if column in [4,10]:
            res = Config.RES_YES if res==1 else Config.RES_NO
        if column in [5,11]:
            res = Config.RES_TEST_OK if res==1 else Config.RES_TEST_FAILED
        
        if tableData[5]==0:
            if column in range(5,10):
                res = ''
        if tableData[11]==0:
            if column in range(11,23):
                res = ''
        if tableData[15]>tableData[16]:
            if column in range(16,23):
                res = ''
        return res