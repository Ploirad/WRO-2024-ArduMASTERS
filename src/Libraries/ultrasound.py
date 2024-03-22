import RPi.GPIO as GPIO
import time

Tforw = 23
Eforw = 24
Tback = 17
Eback = 27
TI = 22
EI = 10
TD = 5
ED = 6

def init_ultrasonido():
    GPIO.setmode(GPIO.BCM)
        GPIO.setup(Tforw, GPIO.OUT)
        GPIO.setup(Eforw, GPIO.IN)
        GPIO.setup(Tback, GPIO.OUT)
        GPIO.setup(Eback, GPIO.IN)
        GPIO.setup(TI, GPIO.OUT)
        GPIO.setup(EI, GPIO.IN)
        GPIO.setup(TD, GPIO.OUT)
        GPIO.setup(ED, GPIO.IN)

def get_distance(trig_pin, echo_pin):
    GPIO.output(trig_pin, True)
    time.sleep(0.00001)
    GPIO.output(trig_pin, False)
    pulse_start = time.time()
    pulse_end = time.time()
    while GPIO.input(echo_pin) == 0:
        pulse_start = time.time()
    while GPIO.input(echo_pin) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance
