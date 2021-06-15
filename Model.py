import sys
from PyQt5 import QtCore
from PyQt5.QtCore import Qt,QObject,pyqtSignal,QTimer
import Config
from Database.database import data
from ReceiptModel import ReceiptModel
from PressureSensor import PressureSensor



class ChannelModel(QObject):
    absValueChanged = pyqtSignal(str)
    difValueChanged = pyqtSignal(str)
    durationValueChanged = pyqtSignal(float)
    modelUpdated = pyqtSignal()

    def __init__(self,channelName,pinAbs,pinDiff):
        super().__init__()
        self.channelName = channelName
        
        self.pinAbs = pinAbs
        self.pinDiff = pinDiff

        self.absPressureSensor = PressureSensor(PressureSensor.absSensorAlias,self.pinAbs)
        self.difPressureSensor = PressureSensor(PressureSensor.difSensorAlias,self.pinDiff)

        self.testNameModel = ReceiptModel(enabledReceipts=1)

        self.initSensorValues()

        self.minDurationValue = 0
        self.maxDurationValue = 5 + Config.SENSORS_INIT_PERIOD/1000
        self.curDurationValue = 0
        self.durationTimerStep = 0.1    
        self.durationTimer = QTimer()
        self.durationTimer.timeout.connect(self.durationTimerUpdate)
        self.durationTimerStarted = False
    
    def initSensorValues(self):
        self.absPressureSensor.zeroSensor()
        self.difPressureSensor.zeroSensor()
        self._curValAbs = 0       
        self._curValDif = 0
        

    def updateModel(self):
        print(f'update channel {self.channelName}')
        self.testNameModel.layoutChanged.emit()

        self.modelUpdated.emit()
           
    @property
    def valueAbs(self):
        print('abs value getter')
        return(PressureSensor.DISPLAY_RATIO[PressureSensor.absSensorAlias]*self._curValAbs)
          
    @valueAbs.setter
    def valueAbs(self,value):
        self._curValAbs = value
        #str.format("{:.{}f}",value,Config.ABS_PRESSURE_ROUNDING_PRECISION)
        v = PressureSensor.DISPLAY_RATIO[PressureSensor.absSensorAlias]*self._curValAbs
        vr = round(v,Config.ABS_PRESSURE_ROUNDING_PRECISION)
        if (abs(vr)<1/pow(10,Config.ABS_PRESSURE_ROUNDING_PRECISION)): 
            vr = 0
        self.absValueChanged.emit(str.format("{:.{}f}",vr,Config.ABS_PRESSURE_ROUNDING_PRECISION))
   
    @property
    def valueDif(self):
        print('dif value getter')
        return(PressureSensor.DISPLAY_RATIO[PressureSensor.difSensorAlias]*self._curValDif)

    @valueDif.setter
    def valueDif(self,value):
        self._curValDif = value
        #str.format("{:.{}f}",value,Config.DIF_PRESSURE_ROUNDING_PRECISION)
        v = PressureSensor.DISPLAY_RATIO[PressureSensor.difSensorAlias]*self._curValDif
        vr = round(v,Config.DIF_PRESSURE_ROUNDING_PRECISION)
        if (abs(vr)<1/pow(10,Config.DIF_PRESSURE_ROUNDING_PRECISION)): 
            vr = 0
        self.difValueChanged.emit(str.format("{:.{}f}",vr,Config.DIF_PRESSURE_ROUNDING_PRECISION)) 
       

    def startDurationTimer(self,start):
        if (start):
            self.curDurationValue = 0
            self.durationTimer.start(self.durationTimerStep*1000)
            self.durationTimerStarted = True
        else:
            self.durationTimer.stop()

    def durationTimerUpdate(self):
        if (self.durationTimerStarted):
            self.curDurationValue += self.durationTimerStep
            if (self.curDurationValue>self.maxDurationValue):
                self.curDurationValue = self.maxDurationValue
                self.durationTimerStarted = False
            self.durationValueChanged.emit(self.curDurationValue)

    def readSensor(self,sensorType):
        if (sensorType == PressureSensor.absSensorAlias):
            if (self.absPressureSensor.zeroed):
                self.valueAbs = self.absPressureSensor.getFilteredValue()
        else:
            if (self.difPressureSensor.zeroed):
                self.valueDif = self.difPressureSensor.getFilteredValue()
        
        """
        print(f'Sensor data {res}')
        print('Decoded:')


        print(f'status bits={status_bits:02b}')
        print(f'Pressure={pressure} mbar (in counts {output})')
        print(f'Temperature={temperature} (in counts {output_t})')
        
        #print(f'Датчик {sensorPin}: давление={pressure:.5f}; температура={temperature:.2f}')
        return [sensorPin,pressure,temperature]
        """


if __name__ == '__main__':
    print(f'm = {PressureSensor.PRESSURE_MAX["DIF"]}')
    k = 1/pow(10,2)
    print(f'{k}')