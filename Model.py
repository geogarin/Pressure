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
from math import pi,sqrt
from datetime import datetime
import time

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

        self.testStopType = ''

        self.minDurationValue = 0
        self.curDurationValue = 0
        
        self.currentTestDuration = 0

        self.sensorRequestTimer = QTimer()
        self.sensorRequestTimer.timeout.connect(self.onSensorRequest)

        self.pressureTestTimerDuration = Config.SENSORS_REQUEST_PERIOD
        self.pressureTestTimer = QTimer()
        self.pressureTestTimer.timeout.connect(self.onPressureTestTimer)

        self.testTimerDuration = Config.SENSORS_REQUEST_PERIOD
        self.testTimer = QTimer()
        self.testTimer.timeout.connect(self.onTestTimer)

        self.idleTimerDuration = 0
        self.idleTimer = QTimer()
        self.idleTimer.timeout.connect(self.onIdleTimer)
        self.idleTimer.start(Config.IDLE_TIMER_PERIOD)
        
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

        self.absValueChanged.emit('')
        self.difValueChanged.emit('')

    
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
        #print(f'update channel {self.channelName}')
        self.testNameModel.layoutChanged.emit()

        self.modelUpdated.emit()
        self.updateTestParameters()

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
        #print(f'dif={self.valueDif}')
        if (vr>Config.MAX_PRESSURE_VALVE2_CLOSED) or (vr<-Config.MAX_PRESSURE_VALVE2_CLOSED): self.isOpenValve2 = True

        self.difValueChanged.emit(str.format("{:.{}f}",vr,self.difRoundingPrecision)) 
       
    """
    def startDurationTimer(self,start):
        
        if (start):
            self.curDurationValue = 0
            self.durationTimer.start(self.durationTimerStep)
            self.durationTimerStarted = True
        else:
            self.durationTimer.stop()    

    def durationTimerUpdate(self):
        if (self.durationTimerStarted):
            #self.curDurationValue += self.durationTimerStep/1000
            self.curDurationValue = self.currentTestDuration
            if (self.curDurationValue>self.maxDurationValue):
                print(f'{self.currentTestDuration} {self.curDurationValue} stop 111 !!!')
                self.curDurationValue = self.maxDurationValue
                self.durationTimerStarted = False
            self.durationValueChanged.emit(self.curDurationValue)
    """

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
        self.idleTimerDuration = 0

    @property
    def isOpenValve2(self):
        return self._isOpenValve2
        
    @isOpenValve2.setter
    def isOpenValve2(self,value):
        self._isOpenValve2 = value        
        self.valveStateChanged.emit(2)
        state = LOW if self.isOpenValve2 else HIGH
        self.channelRelay.digitalWrite(2,state)
        self.idleTimerDuration = 0

    @property
    def isOpenValve3(self):
        return self._isOpenValve3

    @isOpenValve3.setter
    def isOpenValve3(self,value):
        self._isOpenValve3 = value
        self.valveStateChanged.emit(3)
        state = HIGH if self.isOpenValve3 else LOW
        self.channelRelay.digitalWrite(3,state)
        self.idleTimerDuration = 0

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
        self.idleTimerDuration = 0

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
        self.idleTimerDuration = 0


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
            #print(f'{self.currentTestDuration} {self.curDurationValue} close valves')
            self.isOpenValve4 = self.valve4State
            self.isOpenValve2 = self.valve2State
            
    def testNameChanged(self,testName):
        self.testName = testName
        self.updateTestParameters()
        
    def updateTestParameters(self):
        self.stepName = []
        self.subStepName = []
        self.stepDuration = []
        self.processFunction = []
        self.maxStepIndex = 0

        if self.testName!='':
            d = data()
            r = d.getReceipt(self.testName)
            self.pressureStrength = r['StrengthTestPressure']
            self.pressureSealed = r['SealedTestPressure']
            self.savedPressureStrengthAbs = 0
            self.savedPressureSealedAbs = 0
            self.savedPressureSealedDif = 0 
    
            CommonControl.setMaxChannelPressure(self.pressureStrength)
            CommonControl.setMaxChannelPressure(self.pressureSealed)

            self.strengthTestResult = 0
            self.sealedTestResult = 0

            if not (self.testStrengthOff and self.testSealedOff):

                self.stepName.append(Config.RC_ZERO_SENSORS)
                self.subStepName.append('')
                self.stepDuration.append((Config.SENSOR_WAIT_PERIOD+Config.SENSORS_INIT_PERIOD+Config.DELAY_BETWEEN_STEPS)/1000)
                self.processFunction.append(self.testZeroSensors)
                self.maxStepIndex += 1

                self.stepName.append(Config.RC_CONNECTION_DURATION)
                self.subStepName.append('')
                self.stepDuration.append(r['ConnectionDuration']+Config.DELAY_BETWEEN_STEPS/1000)
                self.stepDuration[self.maxStepIndex] += self.stepDuration[self.maxStepIndex-1]
                self.processFunction.append(self.testConnection)
                self.maxStepIndex += 1

           
            if (not self.testStrengthOff):
                self.stepName.append(Config.RC_STRENGTH_TEST)
                self.subStepName.append(Config.RC_INFLATING_DURATION)
                self.stepDuration.append(r['InflatingDuration']+Config.DELAY_BETWEEN_STEPS/1000)
                self.stepDuration[self.maxStepIndex] += self.stepDuration[self.maxStepIndex-1]
                self.processFunction.append(self.testStrengthInflating)
                self.maxStepIndex += 1

                self.stepName.append(Config.RC_STRENGTH_TEST)
                self.subStepName.append(Config.RC_TESTING)
                self.stepDuration.append(r['StrengthTestDuration']+Config.DELAY_BETWEEN_STEPS/1000)
                self.stepDuration[self.maxStepIndex] += self.stepDuration[self.maxStepIndex-1]
                self.processFunction.append(self.testStrengthTest)
                self.maxStepIndex += 1
            
            if (not self.testSealedOff):
                self.stepName.append(Config.RC_SEALED_TEST)
                self.subStepName.append(Config.RC_INFLATING_DURATION)
                self.stepDuration.append(r['InflatingDuration']+Config.DELAY_BETWEEN_STEPS/1000)
                self.stepDuration[self.maxStepIndex] += self.stepDuration[self.maxStepIndex-1]
                self.processFunction.append(self.testSealedInflating)
                self.maxStepIndex += 1

                self.stepName.append(Config.RC_SEALED_TEST)
                self.subStepName.append(Config.RC_STABILIZATION_DURATION)
                self.stepDuration.append(r['StabilizationDuration']+Config.DELAY_BETWEEN_STEPS/1000)
                self.stepDuration[self.maxStepIndex] += self.stepDuration[self.maxStepIndex-1]
                self.processFunction.append(self.testSealedStabilization)
                self.maxStepIndex += 1

                self.stepName.append(Config.RC_SEALED_TEST)
                self.subStepName.append(Config.RC_TESTING)
                self.stepDuration.append(r['SealedTestDuration']+Config.DELAY_BETWEEN_STEPS/1000)
                self.stepDuration[self.maxStepIndex] += self.stepDuration[self.maxStepIndex-1]
                self.processFunction.append(self.testSealedTest)
                self.maxStepIndex += 1

                self.maxAllowedLeakDynamic = r['SealedTestDeltaThreshold']/r['SealedTestDuration']
                self.maxAllowedLeak = r['SealedTestDeltaThreshold']
                self.volumeOfProduct = r['Volume']
                self.volumeOfLeak = 0
                self.crossSecAreaLeak = 0
                self.diaLeak = 0
                self.initialSealedTestTime = 0
                self.initialSealedTestPressure = 0

        else:
            CommonControl.setMaxChannelPressure(0)

        if self.testStrengthOff and self.testSealedOff:
            CommonControl.setMaxChannelPressure(0)
            self.maxDurationValue = 0
        else:
            self.maxDurationValue = self.stepDuration[self.maxStepIndex-1]
            self.durationChanged.emit(self.maxDurationValue)
        #print(f'{self.maxDurationValue} max duration')

    def setTestStopType(self,stopType):
        self.testStopType = stopType

    def startTest(self):
        #print(f'start test')
        self.currentTestDuration = 0
        self.testLabel = ''
        self.stepLabel = ''
        self.firstRun = False
        self.volumeOfLeak = 0
        self.maxSealedTestPressure = 0
        if (self.maxDurationValue>0):
            self._curValAbs = 0       
            self._curValDif = 0           
            self.currentStep = ''
            self.currentSubStep = ''
            self.curStepIndex = 0  
            self.resultStrength = 0
            self.resultSealed = 0
            self.absPressureSensor.initFilterValues()
            self.difPressureSensor.initFilterValues()
            self.testTimer.start(self.testTimerDuration)
            self.pressureTestTimer.start(self.pressureTestTimerDuration)
            self.startTime = time.time()
        else:
            self.testComplete.emit()

    def stopTest(self):
        #print(f'stop test')
        self.sensorRequest(False)
        self.pressureTestTimer.stop()
        CommonControl.closeInputPressure()
        self.testTimer.stop()
        self.isOpenValve1 = False
        self.isOpenValve3 = True
        self.isOpenValve4 = True
        self.isOpenFittingValve = False

        self.resultStrength = self.strengthTestResult
        self.resultSealed = self.sealedTestResult

        self.strengthTestResultDescription = ''
        
        if (self.resultStrength==-1): self.strengthTestResultDescription = self.stepLabel

        self.sealedTestResultDescription = ''
        if (self.resultSealed==-1): self.sealedTestResultDescription = self.stepLabel



        self.saveTestResult()

    def onIdleTimer(self):
        if self.idleTimerDuration > Config.IDLE_PERIOD:
            if self.isOpenValve1 or not self.isOpenValve2 or self.isOpenValve3 or self.isOpenValve4 or self.isOpenFittingValve:
                self.initChannelRelay()
                self.idleTimerDuration = 0

        self.idleTimerDuration += Config.IDLE_TIMER_PERIOD

    def onTestTimer(self):
        self.currentTestDuration = time.time()-self.startTime

    def onPressureTestTimer(self):
        if (self.currentTestDuration<=self.maxDurationValue):
            self.durationValueChanged.emit(self.currentTestDuration)

        if self.currentTestDuration > self.stepDuration[self.curStepIndex]:
            self.curStepIndex += 1
            if self.curStepIndex == self.maxStepIndex: self.curStepIndex -= 1
            self.idleTimerDuration = 0
            
        newStep = self.stepName[self.curStepIndex]
        newSubStep = self.subStepName[self.curStepIndex]

        self.firstRun = False
        if self.currentSubStep!=newSubStep:
            self.currentSubStep = newSubStep
            self.stepLabel = newSubStep
            self.firstRun = True

        if self.currentStep!=newStep:
            self.currentStep = newStep
            self.testLabel = newStep
            self.firstRun = True

        self.processFunction[self.curStepIndex]()   
     
        #if self.firstRun:
        #    print(f'start={self.currentTestDuration} plan finish={self.stepDuration[self.curStepIndex]} {self.currentStep} {self.currentSubStep} volume={self.volumeOfLeak}')
                    
        if self.currentTestDuration > self.maxDurationValue:
            if not self.testSealedOff:
                #curLeak = (self.valueDif-self.initialSealedTestPressure)/(self.currentTestDuration-self.initialSealedTestTime)
                #curLeak = (self.valueDif-self.maxSealedTestPressure)/(self.currentTestDuration-self.initialSealedTestTime)
                curLeak = (self.maxSealedTestPressure-self.valueDif)
                #print(f'max={self.maxSealedTestPressure} cur={self.valueDif} delta={curLeak}')

                #self.volumeOfLeak = abs(self.valueDif-self.initialSealedTestPressure)/(self.currentTestDuration-self.initialSealedTestTime)*self.volumeOfProduct/100000
                self.volumeOfLeak = abs(curLeak)/(self.currentTestDuration-self.initialSealedTestTime)*self.volumeOfProduct/100000
                #print(f'cur={self.currentTestDuration} initT={self.initialSealedTestTime} initP={self.initialSealedTestPressure} curP={self.valueDif} curAbs={self.valueAbs} vol={self.volumeOfLeak}')
                #self.sealedTestResult = 1 if abs(curLeak)<=self.maxAllowedLeakDynamic else -1
                self.sealedTestResult = 1 if abs(curLeak)<=self.maxAllowedLeak else -1
                if self.sealedTestResult == -1:
                    self.testLabel = Config.RES_LEAK_MORE_ALLOWED
                else:
                    self.testLabel = Config.RES_TEST_OK
                       
                #if self.sealedTestResult == 1:
                self.crossSecAreaLeak = self.volumeOfLeak/330/self.initialSealedTestAbsPressure/100
                #print(f'vol={self.volumeOfLeak} pr={self.initialSealedTestAbsPressure}')
                if self.crossSecAreaLeak >= 0:
                    self.diaLeak = 2000*sqrt(self.crossSecAreaLeak/pi)
                else: 
                    self.diaLeak = 0

                self.stepLabel= str.format("D={:.{}f}{}",self.diaLeak,Config.RES_ROUNDING_PRECISION,Config.RES_MKM)
            else:
                self.testLabel = ''
                self.stepLabel = ''
                
            self.testComplete.emit()
            #print(f'{self.currentTestDuration} test complete')
    
    def testZeroSensors(self):
        if (self.firstRun):
            # обнуление датчиков
            self.isOpenValve1 = False
            CommonControl.openInputPressure()
            self.zeroSensors()

    def testConnection(self):
        if (self.firstRun):
            # открытие фитинга
            self.sensorRequest(True)
            self.isOpenFittingValve = True

    def testStrengthInflating(self):
        if (self.firstRun):
            # подача воздуха
            self.isOpenValve3 = True
            self.isOpenValve4 = False
        
        # Клапан 1 открыт, пока давление ниже заданного
        self.isOpenValve1 = (self.pressureStrength+Config.ADDITIONAL_PRESSURE-self.valueAbs) > 0
    
    def testStrengthTest(self):
        if (self.firstRun):
            self.isOpenValve1 = False

        self.savedPressureStrengthAbs = self.valueAbs
        self.strengthTestResult = 1 if self.valueAbs>=self.pressureStrength else -1
        if (self.strengthTestResult == -1):
            self.stepLabel = Config.RES_PRESSURE_TOO_LOW
            self.testComplete.emit()
            #print('stop!')

    def testSealedInflating(self):
        if (self.firstRun):
            # подача воздуха
            self.isOpenValve3 = True
            #self.inflating = self.valueAbs<self.pressureSealed

            self.resultStrength = self.strengthTestResult
        """
        if self.inflating:
            self.isOpenValve1 = (self.pressureSealed+Config.ADDITIONAL_PRESSURE-self.valueAbs) > 0
            self.isOpenValve4 = False
        else:
            self.isOpenValve1 = False
            self.isOpenValve4 = (self.pressureSealed+Config.ADDITIONAL_PRESSURE-self.valueAbs) < 0
        """
        # герметичность: либо накачиваем, либо спускаем давление
        self.isOpenValve1 = (self.pressureSealed-self.valueAbs) > 0
        self.isOpenValve4 = (self.pressureSealed+Config.ADDITIONAL_PRESSURE-self.valueAbs) < 0

    def testSealedStabilization(self):
        self.savedPressureSealedAbs = self.valueAbs
        self.savedPressureSealedDif = self.valueDif
        if (self.firstRun):
            self.isOpenValve1 = False
            self.isOpenValve4 = False
            self.stabilized = True

        if self.valueAbs < self.pressureSealed:               
            self.sealedTestResult = -1
            self.stepLabel = Config.RES_PRESSURE_TOO_LOW
            self.testComplete.emit()    

        self.stabilized = abs(self.valueDif)<=Config.ALLOWED_PRESSURE_DELTA

        #self.initialSealedTestTime = self.currentTestDuration
        #self.initialSealedTestPressure = self.valueDif

    def testSealedTest(self):
        self.savedPressureSealedAbs = self.valueAbs
        self.savedPressureSealedDif = self.valueDif
        if (self.firstRun):
            self.isOpenValve2 = False
            self.initialSealedTestTime = self.currentTestDuration
            self.initialSealedTestPressure = self.valueDif
            self.initialSealedTestAbsPressure = self.valueAbs
            self.maxSealedTestPressure = self.valueDif
        if not self.stabilized:
            self.testLabel = Config.RES_UNSTABLE_PARAMETRES
            self.stepLabel = Config.RES_LEAK_OUT_OF_DIAGNOSTIC
            self.testComplete.emit()

        valDif = self.valueDif
        if valDif > self.maxSealedTestPressure: self.maxSealedTestPressure = valDif

        if self.valueAbs < self.pressureSealed:               
            self.sealedTestResult = -1
            self.stepLabel = Config.RES_PRESSURE_TOO_LOW
            self.testComplete.emit()    
        
    def saveTestResult(self):
        if self.testStopType != Config.RES_TEST_CANCELED:
            d = data()
            r = d.getReceipt(self.testName)


            testResult = {}
            testResult["TestDate"] = datetime.now().strftime('%d.%m.%y %H:%M:%S')
            testResult["ChannelNumber"] = self.fittingValve
            testResult["TestName"] = self.testName
            testResult["ProductVolume"] = self.volumeOfProduct
            testResult["StrengthTestEnabled"] = Config.RES_YES if not self.testStrengthOff else Config.RES_NO
            if self.testStrengthOff:
                testResult["StrengthTestPassed"] = Config.RES_TEST_OFF
                testResult["StrengthTestResult"] = ''
                testResult["StrengthTestDuration"] = ''
                testResult["StrengthTestPlanPressure"] = ''
                testResult["StrengthTestFactPressure"] = ''
            else:
                testResult["StrengthTestPassed"] = Config.RES_TEST_OK if self.resultStrength==1 else Config.RES_TEST_FAILED
                testResult["StrengthTestResult"] = self.strengthTestResultDescription
                testResult["StrengthTestDuration"] = str(r['StrengthTestDuration'])
                testResult["StrengthTestPlanPressure"] = str.format("{:.{}f}",r['StrengthTestPressure'],Config.RES_ROUNDING_PRECISION)
                testResult["StrengthTestFactPressure"] = str.format("{:.{}f}",self.savedPressureStrengthAbs,Config.RES_ROUNDING_PRECISION)

            testResult["SealedTestEnabled"] = Config.RES_YES if not self.testSealedOff else Config.RES_NO
            testResult["SealedTestPassed"] = ''
            testResult["SealedTestResult"] = ''
            testResult["SealedTestDuration"] = ''
            testResult["SealedTestPlanPressure"] = ''
            testResult["SealedTestFactPressure"] = ''
            testResult["SealedTestMaxDeltaThreshold"] = ''
            testResult["SealedTestFactDeltaThreshold"] = ''
            testResult["SealedTestMaxAllowedLeak"] = ''
            testResult["SealedTestVolumeOfLeak"] = ''
            testResult["SealedTestCrossSecAreaLeak"] = ''
            testResult["SealedTestLeakDiameter"] = ''
            if self.testSealedOff:
                testResult["SealedTestPassed"] = Config.RES_TEST_OFF
            else:
                if self.resultStrength==-1: 
                    testResult["SealedTestPassed"] = Config.RES_TEST_OFF
                else: 
                    testResult["SealedTestPassed"] = Config.RES_TEST_OK if self.resultSealed==1 else Config.RES_TEST_FAILED
        
            if testResult["SealedTestPassed"] != Config.RES_TEST_OFF:            
                testResult["SealedTestResult"] = self.sealedTestResultDescription
                testResult["SealedTestDuration"] = str(r['SealedTestDuration'])
                testResult["SealedTestPlanPressure"] = str.format("{:.{}f}",r['SealedTestPressure'],Config.RES_ROUNDING_PRECISION)
                testResult["SealedTestFactPressure"] = str.format("{:.{}f}",self.savedPressureSealedAbs,Config.RES_ROUNDING_PRECISION)

            #if testResult["SealedTestPassed"] == Config.RES_TEST_OK: 
                testResult["SealedTestMaxDeltaThreshold"] = str.format("{:.{}f}",r['SealedTestDeltaThreshold'],Config.RES_ROUNDING_PRECISION)
                testResult["SealedTestFactDeltaThreshold"] = str.format("{:.{}f}",self.savedPressureSealedDif,Config.RES_ROUNDING_PRECISION)
                #testResult["SealedTestMaxAllowedLeak"] = str.format("{:.{}f}",self.maxAllowedLeakDynamic,Config.RES_ROUNDING_PRECISION)
                testResult["SealedTestVolumeOfLeak"] = str.format("{:.{}f}",self.volumeOfLeak,Config.RES_ROUNDING_PRECISION)
                testResult["SealedTestCrossSecAreaLeak"] = str.format("{:.{}f}",self.crossSecAreaLeak,Config.RES_ROUNDING_PRECISION)
                testResult["SealedTestLeakDiameter"] = str.format("{:.{}f}",self.diaLeak,Config.RES_ROUNDING_PRECISION)

            s = data()
            s.saveTestResult(testResult)

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
