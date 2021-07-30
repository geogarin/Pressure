from PyQt5.QtCore import QObject, QThread, pyqtSignal
from time import sleep
from datetime import datetime
import xlsxwriter
from Database.database import data
import Config
import os

class TestResultExporter(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    def __init__(self,testsQuantity):
        super().__init__()
        self.testQuantity = testsQuantity

    def run(self):
        d = data()


        s=os.popen('ls /dev/sd*').read()
        usb = s.splitlines()
        s=str.format("pmount {} /media/gga",usb[0])
        os.popen(s)

        """
        ff = open('/media/gga/fff.txt','w')
        ff.write('asdasdasd')
        ff.close()
        """
        dt = datetime.now()
        #cp /media/pi/DEE1-0D94/RaspberryData.json /home/pi/Documents/SmartHome/Data/
        fn = str.format('Export/Export_{}.xlsx',dt.strftime('%d_%m_%Y_%H_%M'))
        cp = str.format('cp /home/gga/Pressure/Export/{} /media/gga/',fn)
        dl = str.format('rm -f {}',fn)
        workbook = xlsxwriter.Workbook(fn)
        worksheet = workbook.add_worksheet()

        channels = d.getChannels()
        channelsQty = len(channels)

        testRes = d.getTestResults(channelsQty*self.testQuantity)

        i = 0

        for col in range(len(Config.RES_COLUMN_NAMES)):
            worksheet.write(1,col+1,Config.RES_COLUMN_NAMES[col])

        for row in range(len(testRes)):
            if row % channelsQty == 0:
                i += 1
                self.progress.emit(i + 1)

        workbook.close()
        os.popen(cp)
        sleep(1)
        #os.popen(dl)
        sleep(1)
        os.popen("pumount /media/gga")
        self.finished.emit()