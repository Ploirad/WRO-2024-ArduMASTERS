#This code is a library for the button to know if the button has been pressed or not

#Import the necessary libraries
import RPi.GPIO as GPIO

#This function is used to give a boolean variable if the button has pressed (True) or not (False)
def button_state():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(9, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    return GPIO.input(9) == GPIO.HIGH
