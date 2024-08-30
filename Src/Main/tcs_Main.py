import RPi.GPIO as GPIO
import time
import threading
import signal
import json
from Libraries import tcs34725 as tcs
import MAIN
import os
import sys


move_json = os.path.join(os.path.dirname(__file__), "Json", "tcs_color_detection.json")

def signal_handler(sig, frame):
    global stop_event
    stop_event.set()


def color_detection(stop_event):
    first_color_obtained = ""
    turn_started = False
    turn_done = False
    turn_count = 0
    lap_count = 0
    while not stop_event.is_set():
        color_obtained = tcs.get_color()

        if first_color_obtained == "":
            if color_obtained == "Orange" or color_obtained == "Blue":
                first_color_obtained = color_obtained


        if color_obtained == "Orange" and first_color_obtained == "Orange" and not turn_started:
            turn_started = True
            turn_done = False

        elif color_obtained == "Blue" and first_color_obtained == "Blue" and not turn_started:
            turn_started = True
            turn_done = False

        elif color_obtained == "Unknown":   
            turn_started = False

        
        if color_obtained == "Orange" and first_color_obtained == "Blue" and not turn_done: 
            turn_done = True
            turn_count += 1

        if color_obtained == "Blue" and first_color_obtained == "Orange" and not turn_done:
            turn_done = True
            turn_count += 1

        if MAIN.extra_lap:
            lap_count += 1
            MAIN.extra_lap = False

        if turn_count == 4:
            lap_count += 1
            turn_count = 0

        data = {
            "first_color_obtained": first_color_obtained,
            "color_obtained" : color_obtained,
            "turns": turn_count,
            "laps": lap_count 
        }

        with open("tcs_json", "w", encoding='utf-8') as j:
            json.dump(data, j, indent=4)

        # Optional sleep to reduce the frequency of measurements
        time.sleep(0.1)
        # print(turn_done)
        

threads = []
stop_event = threading.Event()
signal.signal(signal.SIGINT, signal_handler)

data = {
            "first_color_obtained": "",
            "color_obtained" : "",
            "turns": 0,
            "laps": 0 
        }

with open("tcs_json", "w", encoding='utf-8') as j:
    json.dump(data, j, indent=4)

try:
    t = threading.Thread(target=color_detection, args=(stop_event,))
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