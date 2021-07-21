import spidev
import Odroid.GPIO as GPIO
from Database.database import data
from time import sleep
from PyQt5.QtCore import QTimer,pyqtSignal,QObject
import Config

class PressureSensor(QObject):
    sensorZeroed = pyqtSignal()
    GPIO.setmode(GPIO.SOC)

    d = data()
    
    absSensorAlias = 'ABS'
    difSensorAlias = 'DIF'

    absSensor = d.getSensorParameters('Absolute')
    difSensor = d.getSensorParameters('Differential')
    
    _setup = d.getSetup()
    SAMPLES_QUANTITY = _setup['FilterDepth']

    OUTPUT_MIN = {absSensorAlias: absSensor['DigitalCounts10Percent'], difSensorAlias : difSensor['DigitalCounts10Percent'] }
    OUTPUT_MAX = {absSensorAlias: absSensor['DigitalCounts90Percent'], difSensorAlias : difSensor['DigitalCounts90Percent']}

    PRESSURE_MIN = {absSensorAlias: absSensor['SensorPressureMin'], difSensorAlias : difSensor['SensorPressureMin']}
    PRESSURE_MAX = {absSensorAlias: absSensor['SensorPressureMax'],difSensorAlias :  difSensor['SensorPressureMax']}

    DISPLAY_RATIO = {absSensorAlias: absSensor['Ratio'], difSensorAlias: difSensor['Ratio']}
    DISPLAY_UNIT_OF_MEASURE = {absSensorAlias: absSensor['DisplayUnitOfMeasure'], difSensorAlias: difSensor['DisplayUnitOfMeasure']}

    TEMPERATURE_MAX = absSensor['TemperatureMax']

    def getSensorData(sensorType,sensorPin):
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
        pressure = None
        if (status_bits==0):
            if ((output>=PressureSensor.OUTPUT_MIN[sensorType])and(output<=PressureSensor.OUTPUT_MAX[sensorType])):
                pressure = (output-PressureSensor.OUTPUT_MIN[sensorType])*(PressureSensor.PRESSURE_MAX[sensorType]-PressureSensor.PRESSURE_MIN[sensorType])/(PressureSensor.OUTPUT_MAX[sensorType]-PressureSensor.OUTPUT_MIN[sensorType])+PressureSensor.PRESSURE_MIN[sensorType]
                #output_t = ((res[2]<<8) | (res[3])) >> 5
                #temperature = output_t*200/PressureSensor.TEMPERATURE_MAX-50
                #if (self.channelName=='Канал 1') and (sensorType=='ABS'):
                #    print(f'{sensorType};min={PressureSensor.OUTPUT_MIN[sensorType]};output={output};max={PressureSensor.OUTPUT_MAX[sensorType]};pressure={pressure};pressure(Pa)={pressure*100};t={temperature}')        
        return pressure

    def __init__(self,sensorType,sensorPin):
        super().__init__()
        self.sensorType = sensorType
        self.sensorPin = sensorPin

        self.initTimer = QTimer()
        self.initTimer.timeout.connect(self.initTimerUpdate)
        self.initTimerStarted = False
        self.zeroed = True


        self.setDelta(0)
        self.initFilterValues()
        #self.zeroSensor()
    
    def setDelta(self,delta):
        self.delta = delta

    def initFilterValues(self):
        self._index = 0
        self._currentValue = 0
        self._prevValue = 0

    def getFilteredValue(self):
        curVal = PressureSensor.getSensorData(self.sensorType,self.sensorPin)
        if (curVal is None):
            curVal = self._prevValue

        if (self._index < PressureSensor.SAMPLES_QUANTITY):
            self._index += 1
        self._currentValue = (self._prevValue*(self._index-1)+curVal)/self._index
        #print(f'*** idx = {self._index} p = {curVal} prev={self._prevValue} cur={self._currentValue}')
        self._prevValue = self._currentValue

        return self._currentValue+self.delta

    def zeroSensor(self):
        self.zeroed = False
        self.currentStep = 0
        self.setDelta(0)
        #print(f'start zero')
        self.initTimer.start(Config.SENSORS_REQUEST_PERIOD)

    def initTimerUpdate(self):
        self.currentStep += Config.SENSORS_REQUEST_PERIOD
        p = self.getFilteredValue()
        if (self.currentStep>=Config.SENSORS_INIT_PERIOD):
            self.initTimer.stop()
            self.zeroed = True
            #print(f'zero {p}')
            self.setDelta(-p)
            self.sensorZeroed.emit()

            

if __name__ == '__main__':
    p = PressureSensor.getSensorData("ABS",479)
    p2 = PressureSensor.getSensorData("DIF",477)
    p3 = PressureSensor.getSensorData("DIF",476)
    print(f'ABS={p} DIF={p2} DIF={p3}')
    c = PressureSensor("DIF",477)
    for i in range(0,1000):
        p1 = c.getFilteredValue()
        #print(p1)
        sleep(0.01)

    p = c.getFilteredValue()
    c.setDelta(-p)

    for i in range(0,1000):
        p1 = c.getFilteredValue()
        print(p1)
        sleep(0.01)

    p = c.getFilteredValue()
    print(p)

                


