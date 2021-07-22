import sys
from types import new_class
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
    testLabelChanged = pyqtSignal(str)
    stepLabelChanged = pyqtSignal(str)
    durationChanged = pyqtSignal(float)
    testComplete = pyqtSignal()
    resultStrengthChanged = pyqtSignal(int)
    resultSealedChanged = pyqtSignal(int) 

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

        self.testStrengthOff = False
        self.testSealedOff = False
        self._resultStrength = 0
        self._resultSealed = 0

        self.minDurationValue = 0
        self.curDurationValue = 0
        self.durationTimerStep = 0.1    
        self.durationTimer = QTimer()
        self.durationTimer.timeout.connect(self.durationTimerUpdate)
        self.durationTimerStarted = False
        self.currentTestDuration = 0

        self.sensorRequestTimer = QTimer()
        self.sensorRequestTimer.timeout.connect(self.onSensorRequest)

        self.pressureTestTimer = QTimer()
        self.pressureTestTimer.timeout.connect(self.onPressureTestTimer)
        
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
        self.isOpenFittingValve = False

    def sensorRequest(self,enabled):
        if (enabled):
            self.sensorRequestTimer.start(Config.SENSORS_REQUEST_PERIOD)
        else:
            self.sensorRequestTimer.stop()

    def initRoundingPrecision(self,absRoundingPrecision=Config.ABS_PRESSURE_ROUNDING_PRECISION,difRoundingPrecision=Config.DIF_PRESSURE_ROUNDING_PRECISION):
        self.absRoundingPrecision = absRoundingPrecision
        self.difRoundingPrecision = difRoundingPrecision
       
    def updateModel(self):
        print(f'update channel {self.channelName}')
        self.testNameModel.layoutChanged.emit()

        self.modelUpdated.emit()

    @property 
    def resultStrength(self):
        return(self._resultStrength)
    
    @resultStrength.setter
    def resultStrength(self,value):
        self._resultStrength = value
        self.resultStrengthChanged.emit(self._resultStrength)

    @property 
    def resultSealed(self):
        return(self._resultSealed)
    
    @resultSealed.setter
    def resultSealed(self,value):
        self._resultSealed = value
        self.resultSealedChanged.emit(self._resultSealed)

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
                print(f'{self.currentTestDuration} {self.curDurationValue} stop!!!')
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
        if (valveNumber==5): self.isOpenFittingValve = not self.isOpenFittingValve

    def inverseTestStrength(self):
        self.testStrengthOff = not self.testStrengthOff
        self.updateTestParameters()

    def inverseTestSealed(self):
        self.testSealedOff = not self.testSealedOff
        self.updateTestParameters()

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
    def isOpenFittingValve(self):
        return self._isOpenFittingValve
        
    @isOpenFittingValve.setter
    def isOpenFittingValve(self,value):
        self._isOpenFittingValve = value        
        self.valveStateChanged.emit(5)
        state = HIGH if self.isOpenFittingValve else LOW
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
            print(f'{self.currentTestDuration} {self.curDurationValue} close valves')
            self.isOpenValve4 = self.valve4State
            self.isOpenValve2 = self.valve2State
            
    def testNameChanged(self,testName):
        self.testName = testName
        self.updateTestParameters()
        
    def updateTestParameters(self):
        self.stepName = []
        self.stepDuration = []
        self.maxStepIndex = 0

        if self.testName!='':
            d = data()
            r = d.getReceipt(self.testName)
            pressureStrength = r['StrengthTestPressure']
            pressureSealed = r['SealedTestPressure']
    
            CommonControl.setMaxChannelPressure(pressureStrength)
            CommonControl.setMaxChannelPressure(pressureSealed)

            self.stepName.append(Config.RC_ZERO_SENSORS)
            self.stepDuration.append((Config.SENSOR_WAIT_PERIOD+Config.SENSORS_INIT_PERIOD+Config.DELAY_BETWEEN_STEPS)/1000)
            self.maxStepIndex += 1

            self.stepName.append(Config.RC_CONNECTION_DURATION)
            self.stepDuration.append(r['ConnectionDuration']+Config.DELAY_BETWEEN_STEPS/1000)
            self.stepDuration[self.maxStepIndex] += self.stepDuration[self.maxStepIndex-1]
            self.maxStepIndex += 1

            self.stepName.append(Config.RC_INFLATING_DURATION)
            self.stepDuration.append(r['InflatingDuration']+Config.DELAY_BETWEEN_STEPS/1000)
            self.stepDuration[self.maxStepIndex] += self.stepDuration[self.maxStepIndex-1]
            self.maxStepIndex += 1
        else:
            CommonControl.setMaxChannelPressure(0)

        if self.testStrengthOff and self.testSealedOff:
            CommonControl.setMaxChannelPressure(0)
            self.maxDurationValue = 0
        else:
            self.maxDurationValue = self.stepDuration[self.maxStepIndex-1]
            self.durationChanged.emit(self.maxDurationValue)



    def startTest(self):
        print(f'start test')
        self.currentTestDuration = 0
        self.startDurationTimer(True)
        self.testLabel = ''
        self.stepLabel = ''
        if (self.maxDurationValue>0):
            self._curValAbs = 0       
            self._curValDif = 0           
            self.currentStep = ''
            self.curStepIndex = 0
            self.pressureTestTimer.start(self.durationTimerStep*1000)
            CommonControl.openInputPressure()
        else:
            self.testComplete.emit()

    def stopTest(self):
        print(f'stop test')
        self.pressureTestTimer.stop()
        self.startDurationTimer(False)
        CommonControl.closeInputPressure()
        self.isOpenValve1 = False
        self.isOpenValve3 = False
        self.isOpenValve4 = True
        self.isOpenFittingValve = False

        self.resultStrength = 1
        self.resultSealed = -1

        

    def onPressureTestTimer(self):
        if self.currentTestDuration > self.stepDuration[self.curStepIndex]:
            self.curStepIndex += 1
            if self.curStepIndex == self.maxStepIndex: self.curStepIndex -= 1
        
        newStep = self.stepName[self.curStepIndex]

        if self.currentStep!=newStep:
            self.currentStep = newStep
            self.testLabel = self.currentStep

            if self.currentStep==Config.RC_ZERO_SENSORS:
                # обнуление датчиков
                print(f'{self.currentTestDuration} zero sensors started')
                self.zeroSensors()
                
            if self.currentStep == Config.RC_CONNECTION_DURATION:
                # открытие фитинга
                print(f'{self.currentTestDuration} {self.curDurationValue} {self.currentStep}')
                self.isOpenFittingValve = True

            if self.currentStep == Config.RC_INFLATING_DURATION:
                # подача воздуха
                self.isOpenValve4 = False
                self.isOpenValve3 = True
                self.isOpenValve1 = True
                print(f'{self.currentTestDuration} {self.curDurationValue} {self.currentStep}')


        
        if self.currentTestDuration > self.maxDurationValue:
            self.testComplete.emit()
            print(f'{self.currentTestDuration} test complete')
        self.currentTestDuration += self.durationTimerStep

    @property
    def testLabel(self):
        return(self._testLabel)
          
    @testLabel.setter
    def testLabel(self,value):
        self._testLabel = value
        self.testLabelChanged.emit(self._testLabel)

    @property
    def stepLabel(self):
        return(self._stepLabel)
          
    @stepLabel.setter
    def stepLabel(self,value):
        self._stepLabel = value
        self.stepLabelChanged.emit(self._stepLabel)
   
if __name__ == '__main__':
    print(f'm = {PressureSensor.PRESSURE_MAX["DIF"]}')
    k = 1/pow(10,2)
    print(f'{k}')
