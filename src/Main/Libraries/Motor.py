import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)

# Declare the PWM pins for the motors
Motor = GPIO.PWM(3, 50)
Direccion = GPIO.PWM(2, 50)

# Inputs of the function are VELocity and DIRection
def movement(vel, dir, stop):
    # Convert input into usable value
    if vel == 1:
        # Max velocity forward 
        vel = 12.5
    elif vel == -1: 
        # Max velocity backward
        vel = 2.5
    else:
        # If null is introduced stop car
        stop = 1

    if not stop:
        Motor.start(vel)
        if dir == 0:
            Direccion.start(6.8)
        elif dir <= -1:
            Direccion.start(12.5)
        else:
            Direccion.start(2.5)
    else:
        Motor.stop()
        Direccion.start(7.5)

def avance(evitate):
    if not evitate:
        Motor.start(12.5)
