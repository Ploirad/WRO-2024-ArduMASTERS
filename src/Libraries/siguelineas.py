import RPi.GPIO as GPIO

IRsensor = 8

def init_siguelineas():
    GPIO.setup(IRsensor, GPIO.IN)

def leer_linea():
    linea = GPIO.input(IRsensor)
    return linea
