import RPi.GPIO as GPIO

IRsensor = 8

def init_siguelineas():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IRsensor, GPIO.IN)

def leer_linea():
    linea = GPIO.input(IRsensor)
    return linea
