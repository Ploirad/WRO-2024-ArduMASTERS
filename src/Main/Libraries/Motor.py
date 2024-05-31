import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)

Motor = GPIO.PWM(3, 50)
Direccion = GPIO.PWM(2, 50)

def movimiento(vel, dir, stop):
    stop_direccion = False
    sen = 10
    if vel > 0:
        sen = 13
    elif vel < 0: 
        sen = 1
    else:
        stop_direccion = True

    if not stop:
        Motor.start(sen)
        #Direccion.start(4.5+(dir/30))
        if not stop_direccion:
            if dir > 0:
                Direccion.start(2)
            elif dir < 0:
                Direccion.start(18)
            else:
                Direccion.start(8)
        else:
            Direccion.start(8)
    else:
        Motor.stop()
        Direccion.start(8)
