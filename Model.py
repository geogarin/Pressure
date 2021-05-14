import sys
from PyQt5 import QtCore
from PyQt5.QtCore import Qt,QObject,pyqtSignal,QTimer
import Config
from Database.database import data
import spidev
import Odroid.GPIO as GPIO

GPIO.setmode(GPIO.SOC)
class ChannelModel(QObject):
    absValueChanged = pyqtSignal(float)
    difValueChanged = pyqtSignal(float)
    durationValueChanged = pyqtSignal(float)

    #butNameChanged = pyqtSignal(str)

    d = data()
    absSensorAlias = 'ABS'
    difSensorAlias = 'DIF'


    absSensor = d.getSensorParameters('Absolute')
    difSensor = d.getSensorParameters('Differential')

    OUTPUT_MIN = {absSensorAlias: absSensor['DigitalCounts10Percent'], difSensorAlias : difSensor['DigitalCounts10Percent'] }
    OUTPUT_MAX = {absSensorAlias: absSensor['DigitalCounts90Percent'], difSensorAlias : difSensor['DigitalCounts90Percent']}

    PRESSURE_MIN = {absSensorAlias: absSensor['SensorPressureMin'], difSensorAlias : difSensor['SensorPressureMin']}
    PRESSURE_MAX = {absSensorAlias: absSensor['SensorPressureMax'],difSensorAlias :  difSensor['SensorPressureMax']}

    DISPLAY_RATIO = {absSensorAlias: absSensor['Ratio'], difSensorAlias: difSensor['Ratio']}
    DISPLAY_UNIT_OF_MEASURE = {absSensorAlias: absSensor['DisplayUnitOfMeasure'], difSensorAlias: difSensor['DisplayUnitOfMeasure']}

    TEMPERATURE_MAX = absSensor['TemperatureMax']

    def __init__(self,channelName,pinAbs,pinDiff):
        super().__init__()
        self.channelName = channelName
        
        self.pinAbs = pinAbs
        self.pinDiff = pinDiff
        self.initSensorValues()

        self.minDurationValue = 0
        self.maxDurationValue = 5
        self.curDurationValue = 0
        self.durationTimerStep = 0.1    
        self.durationTimer = QTimer()
        self.durationTimer.timeout.connect(self.durationTimerUpdate)
        self.durationTimerStarted = False
    
    def initSensorValues(self):
        self._valueAbs = [0] * Config.SAMPLES_QUANTITY
        self._valueAbsIdx = 0

        self._valueDif = [0] * Config.SAMPLES_QUANTITY
        self._valueDifIdx = 0

    @property
    def valueAbs(self):
        return(ChannelModel.DISPLAY_RATIO[ChannelModel.absSensorAlias]*sum(self._valueAbs)/Config.SAMPLES_QUANTITY)
        
    @valueAbs.setter
    def valueAbs(self,value):
        self._valueAbs[self._valueAbsIdx] = value
        self._valueAbsIdx += 1
        if (self._valueAbsIdx==Config.SAMPLES_QUANTITY):
            self._valueAbsIdx = 0
        self.absValueChanged.emit(ChannelModel.DISPLAY_RATIO[ChannelModel.absSensorAlias]*sum(self._valueAbs)/Config.SAMPLES_QUANTITY)
    
    @property
    def valueDif(self):
        return(ChannelModel.DISPLAY_RATIO[ChannelModel.difSensorAlias]*sum(self._valueDif)/Config.SAMPLES_QUANTITY)

    @valueDif.setter
    def valueDif(self,value): 
        self._valueDif[self._valueDifIdx] = value
        self._valueDifIdx += 1
        if (self._valueDifIdx==Config.SAMPLES_QUANTITY):
            self._valueDifIdx = 0
        self.difValueChanged.emit(ChannelModel.DISPLAY_RATIO[ChannelModel.difSensorAlias]*sum(self._valueDif)/Config.SAMPLES_QUANTITY)

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
        if (sensorType == ChannelModel.absSensorAlias):
            sensorPin = self.pinAbs
        else:
            sensorPin = self.pinDiff
        GPIO.setup(sensorPin,GPIO.OUT)
        spi = spidev.SpiDev()
        GPIO.output(sensorPin,GPIO.LOW)
        spi.open(0,0)
        spi.max_speed_hz = 122000

        res = spi.xfer2([0,0,0,0])
        spi.close()
        GPIO.output(sensorPin, GPIO.HIGH)

        status_bits = res[0] >> 6

        output = ((res[0]&63)<<8)|res[1]
        pressure = (output-ChannelModel.OUTPUT_MIN[sensorType])*(ChannelModel.PRESSURE_MAX[sensorType]-ChannelModel.PRESSURE_MIN[sensorType])/(ChannelModel.OUTPUT_MAX[sensorType]-ChannelModel.OUTPUT_MIN[sensorType])+ChannelModel.PRESSURE_MIN[sensorType]
        
        output_t = ((res[2]<<8) | (res[3])) >> 5
        temperature = output_t*200/ChannelModel.TEMPERATURE_MAX-50
        if (status_bits==0):
            if (sensorType == ChannelModel.absSensorAlias):
                self.valueAbs = pressure
            else:
                self.valueDif = pressure
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
    print(f'm = {ChannelModel.PRESSURE_MAX["DIF"]}')