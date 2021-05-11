import Odroid.GPIO as GPIO
import time

PINS = [480,500,600]

for p in PINS:
    print(p)

"""
GPIO.setmode(GPIO.SOC)
GPIO.setup(PIN,GPIO.OUT)

while True:
    GPIO.output(PIN, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(PIN,GPIO.LOW)
    time.sleep(2)
"""