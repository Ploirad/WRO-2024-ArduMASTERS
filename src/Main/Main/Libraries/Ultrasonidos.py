import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.IN)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.IN)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.IN)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(10, GPIO.IN)

def measure_distance(position):
    
    # Declare wich pins are going to be used depending on the position requested
    if position == "front":
        GPIO_TRIGGER = 23
        GPIO_ECHO = 24
    elif position == "right" or "red": # RED sings will be at the RIGHT
        GPIO_TRIGGER = 5
        GPIO_ECHO = 6
    elif position == "back":
        GPIO_TRIGGER = 17
        GPIO_ECHO = 27
    elif position == "left" or "green":# GREEN sings will be at the LEFT
        GPIO_TRIGGER = 22
        GPIO_ECHO = 10

    # Assure the TRIG pin is clean
    GPIO.output(GPIO_TRIGGER, False)

    # Send a pulse of 10µs to trig the sensor
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    # Save the start and end time of the pulse
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()

    # Calculate the duration of the pulse
    elapsed_time = stop_time - start_time

    # The velocity of sound is 34300 cm/s
    distance = (elapsed_time * 34300) / 2

    return distance