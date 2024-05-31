import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)

Motor = GPIO.PWM(3, 50)
Direccion = GPIO.PWM(2, 50)

def movimiento(vel, dir, stop):
    stop_direccion = False
    if vel > 0:
        sen = 12.5
    elif vel < 0: 
        sen = 2.5
    else:
        stop_direccion = True

    if not stop:
        Motor.start(sen)
        #Direccion.start(4.5+(dir/30))
        if not stop_direccion:
            if dir > 0:
                Direccion.start(2.5)
            elif dir < 0:
                Direccion.start(12.5)
            else:
                Direccion.start(10.5)
        else:
            Direccion.start(10.5)
    else:
        Motor.stop()
        Direccion.start(10.5)

movimiento(0, 0, True)
