import sys
from PyQt5 import QtCore
from PyQt5.QtCore import Qt,QObject,pyqtSignal,QTimer
import Config
import spidev
import Odroid.GPIO as GPIO

GPIO.setmode(GPIO.SOC)
class ChannelModel(QObject):
    absValueChanged = pyqtSignal(float)
    butNameChanged = pyqtSignal(str)

    

    OUTPUT_MIN = {'ABS': 1638, 'DIF' : 1638 }
    OUTPUT_MAX = {'ABS':14746, 'DIF' : 14746}

    PRESSURE_MIN = {'ABS': 0, 'DIF' : -6}
    PRESSURE_MAX = {'ABS': 60,'DIF' :  6}

    TEMPERATURE_MAX = 2047


    def __init__(self,pinAbs,pinDiff):
        super().__init__()
        self.pinAbs = pinAbs
        self.pinDiff = pinDiff
        self._valueAbs = [0] * Config.SAMPLES_QUANTITY
        self._valueAbsIdx = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.upd)
        self.started = False
        self._butName = 'Start'
    
    @property
    def valueAbs(self):
        return(round(sum(self._valueAbs)/Config.SAMPLES_QUANTITY,3))

    @valueAbs.setter
    def valueAbs(self,value):
        #print(f'index={self._valueAbsIdx} curValue={value}')  
        self._valueAbs[self._valueAbsIdx] = value
        self._valueAbsIdx += 1
        if (self._valueAbsIdx==Config.SAMPLES_QUANTITY):
            self._valueAbsIdx = 0
        #print(f'array={self._valueAbs} avg={round(sum(self._valueAbs)/Config.SAMPLES_QUANTITY,5)}')
        self.absValueChanged.emit(round(sum(self._valueAbs)/Config.SAMPLES_QUANTITY,3))
    
    @property
    def butName(self):
        return self._butName

    @butName.setter
    def butName(self,value):
        self._butName = value
        self.butNameChanged.emit(value)

    
    def buttonPressed(self):
        self.started = not self.started
        if self.started:
            self.timer.start(100)
            self.butName = 'Stop'
            #self.readSensor('ABS')
        else:
            self.timer.stop()
            self.butName = 'Start'


    def upd(self):
        self.readSensor('ABS')

    def readSensor(self,sensorType):
        #while (self.butName=='Stop'):
        if (sensorType == 'ABS'):
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
        print(f'Датчик {sensorPin}: давление={pressure:.5f}; температура={temperature:.2f}; status={status_bits}')
        if (status_bits==0):
            if (sensorType == 'ABS'):
                self.valueAbs = pressure
            #else:
            #    sensorPin = pressure
        """
        qqq
        print(f'Sensor data {res}')
        print('Decoded:')


        print(f'status bits={status_bits:02b}')
        print(f'Pressure={pressure} mbar (in counts {output})')
        print(f'Temperature={temperature} (in counts {output_t})')
        
        #print(f'Датчик {sensorPin}: давление={pressure:.5f}; температура={temperature:.2f}')
        return [sensorPin,pressure,temperature]
        """