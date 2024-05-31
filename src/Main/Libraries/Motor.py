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
            Direccion.start(4.5)
        elif dir < 0:
            Direccion.start(10.5)
        else:
            Direccion.start(7.5)
    else:
        Motor.stop()
        Direccion.start(7.5)

import time
while True:
    t1 = time.time()
    movimiento(0, )
    print(time.time() - t1)
