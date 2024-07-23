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
    # Convert input into usable value with the mathematic function: 7.5x^2 + 5x
    v = (7.5 * pow(vel, 2)) + (5 * vel)
    if v == 0 or stop:
        Motor.stop()
        Direccion.start(6.8)
    
    else:
        Motor.start(v)

        # Convert input into usable value with the mathematic function: 0.7x^2 − 5x + 6.8 
        d = ((0.7 * pow(dir, 2)) - (5 * dir) + 6.8)
        Direccion.start(d)