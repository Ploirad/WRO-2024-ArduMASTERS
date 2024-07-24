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
for i in range(4):
    GPIO.setup(TRIG[i], GPIO.OUT)
    GPIO.setup(ECHO[i], GPIO.IN)

# This function is for read the distances of the pins specified
def read_sensor_distance(trig, echo):
    GPIO.output(trig, False)
    pulse_start = time.time()
    while True:
        GPIO.output(trig, True)
        time.sleep(0.00001)
        GPIO.output(trig, False)

        while GPIO.input(echo) == 0:
            pulse_start = time.time()

        while GPIO.input(echo) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        yield distance

# Handler for SIGINT to stop threads
def signal_handler(sig, frame):
    global stop_event
    stop_event.set()

def principal_logic(HC0, HC1, HC3):
    direction = 0
    traction = 0
    if HC0 > 70:
        traction = 100
        if HC1 < 15:
            direction = -100
        elif HC3 < 15:
            direction = 100
        else:
            direction = 0
    elif HC0 > 30:
        traction = 100
        if HC1 > HC3:
            direction = 100
        else:
            direction = -100
    else:
        traction = -100
        if HC1 > HC3:
            direction = -100
        else:
            direction = 100

    return traction, direction

def move(stop_event):
    if stop_event.is_set():
        return None

    HC0 = read_sensor_distance(TRIG[0], ECHO[0])
    HC1 = read_sensor_distance(TRIG[1], ECHO[1])
    HC2 = read_sensor_distance(TRIG[2], ECHO[2])
    HC3 = read_sensor_distance(TRIG[3], ECHO[3])

    hc0_distance = next(HC0)
    hc1_distance = next(HC1)
    hc2_distance = next(HC2)
    hc3_distance = next(HC3)

    with open("Move.json", "w", encoding='utf-8') as j:
        t, d = principal_logic(hc0_distance, hc1_distance, hc3_distance)
        data = {
            "HC0": hc0_distance,
            "HC1": hc1_distance,
            "HC2": hc2_distance,
            "HC3": hc3_distance,
            "Traction": t,
            "Direction": d
        }
        json.dump(data, j, indent=4)

# Create and start the threads
threads = []
stop_event = threading.Event()
signal.signal(signal.SIGINT, signal_handler)

try:
    t = threading.Thread(target=move, args=(stop_event,))
    t.start()
    threads.append(t)

    # Wait for the end of the threads (in this case it doesn't happen unless interrupted)
    for t in threads:
        t.join()

except Exception as e:
    print(f"eWRITE = {e}")
finally:
    # Clean the GPIO at the end
    GPIO.cleanup()