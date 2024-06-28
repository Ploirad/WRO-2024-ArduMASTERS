#This code is a library for the ultrasonic sensors

#Import the necessary libraries
import RPi.GPIO as GPIO
import time

#Initialize the sensors
GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.IN)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(7, GPIO.IN)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.IN)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(10, GPIO.IN)

#This function is used to give the distances depending 1 variable that is the position and the variable can be:
#1 for the front sensor
#2 for the right sensor
#3 for the back sensor
#4 for the left sensor
#And depending the positon and the distance detected by that sensor the function returns a float variable of the distance detected
def measure_distance(position):
    trigger_echo = {
        1: (23, 24), # Front
        2: (8, 7),   # Right
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


##Code to try the ultrasonic sensors
#while True:
#    front_distance = measure_distance(1)
#    right_distance = measure_distance(2)
#    left_distance = measure_distance(4)
#    back_distance = measure_distance(3)
#    print(f"Front Distance: {front_distance}; Right Distance: {right_distance}; Left Distance: {left_distance}; Back Distance: {back_distance}")