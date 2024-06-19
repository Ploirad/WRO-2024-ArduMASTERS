#This code is a library for the servos and motors to move the car

#Import the necessary libraries
import RPi.GPIO as GPIO

#Initialize the motors
GPIO.setmode(GPIO.BCM)

GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)

# Declare the PWM pins for the motors
Motor = GPIO.PWM(3, 50)
Direccion = GPIO.PWM(2, 50)

#This function is used to move the car depending 3 variables:
#   vel: Say if the car is going to go forward (1), backward (-1) or is going to be stopped (0)
#   dir: Say if the car is going to turn left (1), right (-1) or straight (0)
#   stop:Say if the car is going to move (True) or is going to stop (False)
#And depending the variables the car will move in all directions
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

#This function is used to move the car only forward
def avance():
    Motor.start(12.5)
