import spidev
import Odroid.GPIO as GPIO
import time

# dif
PINS_DIF = [480,483,476,477]

# abs
PINS_ABS = [434,490,492,479]
GPIO.setmode(GPIO.SOC)


# sensor HSCDRRD2.5MDSA3
OUTPUT_MIN = {'ABS': 1638, 'DIF' : 1638 }
OUTPUT_MAX = {'ABS':14746, 'DIF' : 14746}
#PRESSURE_MIN = -6
#PRESSURE_MAX = 6
PRESSURE_MIN = {'ABS': 0, 'DIF' : -6}
PRESSURE_MAX = {'ABS': 60,'DIF' :  6}

TEMPERATURE_MAX = 2047


def readSensor(sensorPin,sensorType):
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
    pressure = (output-OUTPUT_MIN[sensorType])*(PRESSURE_MAX[sensorType]-PRESSURE_MIN[sensorType])/(OUTPUT_MAX[sensorType]-OUTPUT_MIN[sensorType])+PRESSURE_MIN[sensorType]

    output_t = ((res[2]<<8) | (res[3])) >> 5
    temperature = output_t*200/TEMPERATURE_MAX-50

    """
    qqq
    print(f'Sensor data {res}')
    print('Decoded:')


    print(f'status bits={status_bits:02b}')
    print(f'Pressure={pressure} mbar (in counts {output})')
    print(f'Temperature={temperature} (in counts {output_t})')
    """
    #print(f'Датчик {sensorPin}: давление={pressure:.5f}; температура={temperature:.2f}')
    return [sensorPin,pressure,temperature]


while True:
    s = ""
    for p in PINS_DIF:
        res = readSensor(p,'DIF')
        s += f'Датчик {res[0]}: P={res[1]:.5f}; T={res[2]:.2f} | '
    for p in PINS_ABS:
        res = readSensor(p,'ABS')
        s += f'Датчик {res[0]}: P={res[1]:.5f}; T={res[2]:.2f} | '
    print(s)
