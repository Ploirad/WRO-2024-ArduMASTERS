import RPi.GPIO as GPIO

def button_state():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(9, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    return GPIO.input(9) == GPIO.LOW
