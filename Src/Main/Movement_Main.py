# This code is for writing in text archives the distances of the sensors

# First we import the libraries
import RPi.GPIO as GPIO
import time
import threading
import signal
import sys
import json

# Second we create two lists of the pins
TRIG = [23, 8, 17, 22]
ECHO = [24, 7, 27, 10]

# Third we configure the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for i in range(4):
    GPIO.setup(TRIG[i], GPIO.OUT)
    GPIO.setup(ECHO[i], GPIO.IN)
    GPIO.output(TRIG[i], False)  # Ensure TRIG pins are low

# Handler for SIGINT to stop threads
def signal_handler(sig, frame):
    global stop_event
    stop_event.set()

def principal_logic(HC0, HC1, HC3):
    direction = 0
    traction = 0
    if HC0 > 70:
        traction = 25
        if HC1 < 15:
            direction = -100
        elif HC3 < 15:
            direction = 100
        else:
            direction = 0
    elif HC0 > 30:
        traction = 25
        if HC1 > HC3:
            direction = 100
        else:
            direction = -100
    else:
        traction = -25
        if HC1 > HC3:
            direction = 100
        else:
            direction = -100

    return traction, direction

def measure_distance(GPIO_TRIGGER, GPIO_ECHO):
    # Assure the TRIG pin is clean
    GPIO.output(GPIO_TRIGGER, False)
    time.sleep(0.000002)  # Short delay to settle the TRIG pin

    # Send a pulse of 10µs to trigger the sensor
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    # Save the start and end time of the pulse
    start_time = time.time()
    stop_time = time.time()

    # Wait for the echo start
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()
        if start_time - stop_time > 0.1:  # Timeout to avoid infinite loop
            return None

    # Wait for the echo end
    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()
        if stop_time - start_time > 0.1:  # Timeout to avoid infinite loop
            return None

    # Calculate the duration of the pulse
    elapsed_time = stop_time - start_time

    # The velocity of sound is 34300 cm/s
    distance = (elapsed_time * 34300) / 2

    return distance

def move(stop_event):
    while not stop_event.is_set():
        HC0 = measure_distance(TRIG[0], ECHO[0])
        HC1 = measure_distance(TRIG[1], ECHO[1])
        HC2 = measure_distance(TRIG[2], ECHO[2])
        HC3 = measure_distance(TRIG[3], ECHO[3])

        # Check for None values to avoid writing invalid data
        if HC0 is None or HC1 is None or HC2 is None or HC3 is None:
            continue

        t, d = principal_logic(HC0, HC1, HC3)
        data = {
            "HC0": HC0,
            "HC1": HC1,
            "HC2": HC2,
            "HC3": HC3,
            "TRACTION": t,
            "DIRECTION": d
        }

        with open("Libraries/Json/Move.json", "w", encoding='utf-8') as j:
            json.dump(data, j, indent=4)

        # Optional sleep to reduce the frequency of measurements
        time.sleep(0.1)

# Create and start the threads
threads = []
stop_event = threading.Event()
signal.signal(signal.SIGINT, signal_handler)

def start_threds():
    try:
        t = threading.Thread(target=move, args=(stop_event,))
        t.start()
        threads.append(t)

        # Wait for the end of the threads (in this case it doesn't happen unless interrupted)
        for t in threads:
            t.join()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean the GPIO at the end
        GPIO.cleanup()