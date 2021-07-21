import sys
from PyQt5 import QtCore
from PyQt5.QtCore import Qt,QObject,pyqtSignal,pyqtSlot,QTimer
import Config
from Database.database import data
from ReceiptModel import ReceiptModel
from PressureSensor import PressureSensor
from CommonControl import CommonControl
from pyiArduinoI2Crelay import *

class ChannelModel(QObject):
    absValueChanged = pyqtSignal(str)
    difValueChanged = pyqtSignal(str)
    durationValueChanged = pyqtSignal(float)
    modelUpdated = pyqtSignal()
    valveStateChanged = pyqtSignal(int)

    def __init__(self,channelName,pinAbs,pinDiff,i2cAddress,fittingValve):
        super().__init__()
        self.channelName = channelName
        
        self.pinAbs = pinAbs
        self.pinDiff = pinDiff
        self.i2cAddress = i2cAddress
        self.fittingValve = fittingValve

        self.channelRelay = pyiArduinoI2Crelay(self.i2cAddress)
        self.fittingRelay = pyiArduinoI2Crelay(Config.FITTING_MODULE_ADDRESS)
        self.initChannelRelay()
        
        self.absPressureSensor = PressureSensor(PressureSensor.absSensorAlias,self.pinAbs)
        self.difPressureSensor = PressureSensor(PressureSensor.difSensorAlias,self.pinDiff)

        self.testNameModel = ReceiptModel(enabledReceipts=1)
        self.initRoundingPrecision()

        self.minDurationValue = 0
        self.maxDurationValue = 5 + Config.SENSORS_INIT_PERIOD/1000
        self.curDurationValue = 0
        self.durationTimerStep = 0.1    
        self.durationTimer = QTimer()
        self.durationTimer.timeout.connect(self.durationTimerUpdate)
        self.durationTimerStarted = False

        self.sensorRequestTimer = QTimer()
        self.sensorRequestTimer.timeout.connect(self.onSensorRequest)
        
        self.absPressureSensor.sensorZeroed.connect(self.onSensorZeroed)
        self.difPressureSensor.sensorZeroed.connect(self.onSensorZeroed)
        self.zeroedSensorsQuantity = 0

    def setMasterMode(self,enabled):
        if (enabled):
            self.initRoundingPrecision(Config.ABS_MASTER_MODE_PRESSURE_ROUNDING_PRECISION,Config.DIF_MASTER_MODE_PRESSURE_ROUNDING_PRECISION)
        else:
            self.initRoundingPrecision()

        self.sensorRequest(enabled)
        self.initChannelRelay()
    
    def initChannelRelay(self):
        #self.channelRelay.digitalWrite(ALL_CHANNEL,LOW)
        self.isOpenValve1 = False
        self.isOpenValve2 = True
        self.isOpenValve3 = False
        self.isOpenValve4 = False
        self.isFittingClosed = False

    def sensorRequest(self,enabled):
        if (enabled):
            self.sensorRequestTimer.start(Config.SENSORS_REQUEST_PERIOD)
        else:
            self.sensorRequestTimer.stop()

    def initRoundingPrecision(self,absRoundingPrecision=Config.ABS_PRESSURE_ROUNDING_PRECISION,difRoundingPrecision=Config.DIF_PRESSURE_ROUNDING_PRECISION):
        self.absRoundingPrecision = absRoundingPrecision
        self.difRoundingPrecision = difRoundingPrecision

    def initSensorValues(self):
        self.zeroSensors()
        self._curValAbs = 0       
        self._curValDif = 0
        
    def updateModel(self):
        print(f'update channel {self.channelName}')
        self.testNameModel.layoutChanged.emit()

        self.modelUpdated.emit()
           
    @property
    def valueAbs(self):
        return(PressureSensor.DISPLAY_RATIO[PressureSensor.absSensorAlias]*self._curValAbs)
          
    @valueAbs.setter
    def valueAbs(self,value):
        self._curValAbs = value
        v = PressureSensor.DISPLAY_RATIO[PressureSensor.absSensorAlias]*self._curValAbs
        vr = round(v,self.absRoundingPrecision)
        if (abs(vr)<1/pow(10,self.absRoundingPrecision)): 
            vr = 0
        self.absValueChanged.emit(str.format("{:.{}f}",vr,self.absRoundingPrecision))
    
    @property
    def valueDif(self):
        return(PressureSensor.DISPLAY_RATIO[PressureSensor.difSensorAlias]*self._curValDif)
    
    @valueDif.setter
    def valueDif(self,value):
        self._curValDif = value
        v = PressureSensor.DISPLAY_RATIO[PressureSensor.difSensorAlias]*self._curValDif
        vr = round(v,self.difRoundingPrecision)
        if (abs(vr)<1/pow(10,self.difRoundingPrecision)): 
            vr = 0
        if (vr>Config.MAX_PRESSURE_VALVE2_CLOSED) or (vr<-Config.MAX_PRESSURE_VALVE2_CLOSED): self.isOpenValve2 = True

        self.difValueChanged.emit(str.format("{:.{}f}",vr,self.difRoundingPrecision)) 
       

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

    def onSensorRequest(self):
        self.readSensor(PressureSensor.absSensorAlias)
        self.readSensor(PressureSensor.difSensorAlias)

    def readSensor(self,sensorType):
        if (sensorType == PressureSensor.absSensorAlias):
            if (self.absPressureSensor.zeroed):
                self.valueAbs = self.absPressureSensor.getFilteredValue()
        else:
            if (self.difPressureSensor.zeroed):
                self.valueDif = self.difPressureSensor.getFilteredValue()
        
        
    def inverseValve(self,valveNumber):
        if (valveNumber==1): self.isOpenValve1 = not self.isOpenValve1
        if (valveNumber==2): self.isOpenValve2 = not self.isOpenValve2
        if (valveNumber==3): self.isOpenValve3 = not self.isOpenValve3
        if (valveNumber==4): self.isOpenValve4 = not self.isOpenValve4
        if (valveNumber==5): self.isFittingClosed = not self.isFittingClosed

    @property
    def isOpenValve1(self):
        return self._isOpenValve1

    @isOpenValve1.setter
    def isOpenValve1(self,value):
        self._isOpenValve1 = value
        
        if (self.isOpenValve1):
            if (not self.isOpenValve2):
                self.isOpenValve2 = True
        self.valveStateChanged.emit(1)

        state = HIGH if self.isOpenValve1 else LOW
        self.channelRelay.digitalWrite(1,state)

    @property
    def isOpenValve2(self):
        return self._isOpenValve2
        
    @isOpenValve2.setter
    def isOpenValve2(self,value):
        self._isOpenValve2 = value        
        self.valveStateChanged.emit(2)
        state = LOW if self.isOpenValve2 else HIGH
        self.channelRelay.digitalWrite(2,state)

    @property
    def isOpenValve3(self):
        return self._isOpenValve3

    @isOpenValve3.setter
    def isOpenValve3(self,value):
        self._isOpenValve3 = value
        self.valveStateChanged.emit(3)
        state = HIGH if self.isOpenValve3 else LOW
        self.channelRelay.digitalWrite(3,state)

    @property
    def isOpenValve4(self):
        return self._isOpenValve4

    @isOpenValve4.setter
    def isOpenValve4(self,value):
        self._isOpenValve4 = value
        
        if (self.isOpenValve4):
            if (not self.isOpenValve2):
                self.isOpenValve2 = True
        self.valveStateChanged.emit(4)
        state = HIGH if self.isOpenValve4 else LOW
        self.channelRelay.digitalWrite(4,state)

    @property
    def isEnabledValve2(self):
        return not(self.isOpenValve1 or self.isOpenValve4)

    @property
    def isFittingClosed(self):
        return self._isFittingClosed
        
    @isFittingClosed.setter
    def isFittingClosed(self,value):
        self._isFittingClosed = value        
        self.valveStateChanged.emit(5)
        state = HIGH if self.isFittingClosed else LOW
        self.fittingRelay.digitalWrite(self.fittingValve,state)


    def zeroSensors(self):
        self.zeroedSensorsQuantity = 0
        self.valve4State = self.isOpenValve4
        self.valve2State = self.isOpenValve2

        self.isOpenValve2 = True
        self.isOpenValve4 = True
        self.absPressureSensor.zeroSensor()
        self.difPressureSensor.zeroSensor()
    
    def resetZeroSensors(self):
        self.absPressureSensor.setDelta(0)
        self.difPressureSensor.setDelta(0)

    @pyqtSlot()
    def onSensorZeroed(self):
        self.zeroedSensorsQuantity += 1
        if self.zeroedSensorsQuantity==2:
            self.isOpenValve4 = self.valve4State
            self.isOpenValve2 = self.valve2State
            
    def setTestPressure(self,testName):
        if testName!='':
            d = data()
            r = d.getReceipt(testName)
            pressureStrength = r['StrengthTestPressure']
            pressureSealed = r['SealedTestPressure']
    
            CommonControl.setMaxChannelPressure(pressureStrength)
            CommonControl.setMaxChannelPressure(pressureSealed)
        else:
            CommonControl.setMaxChannelPressure(0)
   
if __name__ == '__main__':
    print(f'm = {PressureSensor.PRESSURE_MAX["DIF"]}')
    k = 1/pow(10,2)
    print(f'{k}')
