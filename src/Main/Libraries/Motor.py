import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)

Motor = GPIO.PWM(3, 50)
Direccion = GPIO.PWM(2, 50)

def movimiento(vel, dir, stop):
    if vel > 0:
        sen = 12.5
    elif vel < 0: 
        sen = 2.5
    else:
        stop = 1

    if not stop:
        Motor.start(sen)
        #Direccion.start(4.5+(dir/30))
        if dir > 0:
            Direccion.start(2.5)
        elif dir < 0:
            Direccion.start(12.5)
        else:
            Direccion.start(10)
    else:
        Motor.stop()
        Direccion.start(7.5)

def m(a, b):
    Motor.start(a)
    Direccion.start(b)
import time
a = int(input("a: "))
b = int(input("b: "))
while True:
    t1 = time.time()
    movimiento(a, b, 0)
    print(time.time() - t1)
