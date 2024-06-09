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
    trigger_echo = {
        1: (23, 24), # Front
        2: (5, 6),   # Right
        3: (17, 27), # Back
        4: (22, 10)  # Left
    }
    
    GPIO_TRIGGER, GPIO_ECHO = trigger_echo[position]

    # Assure the TRIG pin is clean
    GPIO.output(GPIO_TRIGGER, False)
    time.sleep(0.000002)  # Reduce the delay here if possible

    # Send a pulse of 10µs to trig the sensor
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    # Save the start and end time of the pulse
    start_time, stop_time = time.time(), time.time()
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()

    # Calculate the duration of the pulse
    elapsed_time = stop_time - start_time

    # The velocity of sound is 34300 cm/s
    distance = (elapsed_time * 34300) / 2

    return distance
