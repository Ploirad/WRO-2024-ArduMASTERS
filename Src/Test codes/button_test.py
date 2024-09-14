import RPi.GPIO as GPIO

# This function is used to give a boolean variable if the button has pressed (True) or not (False)
while True:
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(9, GPIO.IN)
        if GPIO.input(9) == GPIO.HIGH:
            print("boton pulsado")
    except KeyboardInterrupt:
        break