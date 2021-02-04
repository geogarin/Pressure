import spidev
import Odroid.GPIO as GPIO
import time

PINS = [480,483,476]
GPIO.setmode(GPIO.SOC)


# sensor HSCDRRD2.5MDSA3
OUTPUT_MIN = 1638 
OUTPUT_MAX = 14746
PRESSURE_MIN = -6
PRESSURE_MAX = 6

TEMPERATURE_MAX = 2047


def readSensor(sensorPin:int):
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
    pressure = (output-OUTPUT_MIN)*(PRESSURE_MAX-PRESSURE_MIN)/(OUTPUT_MAX-OUTPUT_MIN)+PRESSURE_MIN

    output_t = ((res[2]<<8) | (res[3])) >> 5
    temperature = output_t*200/TEMPERATURE_MAX-50

    """
    
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
    for p in PINS:
        res = readSensor(p)
        s += f'Датчик {res[0]}: P={res[1]:.5f}; T={res[2]:.2f} | '
    print(s)
