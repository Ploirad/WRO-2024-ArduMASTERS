GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)

Motor = GPIO.PWM(2,50)
Direccion = GPIO.PWM(3,50)

def movimiento(vel,dir,stop):
   
    if vel > 0:
        sen = 12.5
    elif vel < 0: 
        sen = 2.5
    else:
        stop = 1

    if not stop:
        Motor.start(sen)
        Direccion.start(4.5+dir/30)
    else:
        Motor.stop()
        Direccion.start(6)