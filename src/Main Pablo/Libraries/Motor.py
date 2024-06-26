import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)

# Declase the PWM pins for the motors
Motor = GPIO.PWM(2,50)
Direccion = GPIO.PWM(3,50)
stop = False

# Inputs of the function are VELocity and DIRection
def movement(vel,dir):
    
    # Convert input into usable value
    if vel == 1:
        # Max velocity forward 
        vel = 12.5
    elif vel == -1: 
        # Max velocity backward
        vel = 2.5
    else:
        # If null is introduced stop car
        stop = True

    if not stop:
        Motor.start(vel)
        Direccion.start(4.5+dir/30)
    else:
        Motor.stop()
        Direccion.start(7,5)