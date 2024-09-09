import RPi.GPIO as GPIO
import time
import threading
import signal
import json
from Libraries import tcs34725 as tcs
import MAIN

def signal_handler(sig, frame):
    global stop_event
    stop_event.set()


def color_detection(stop_event):
    first_color_obteined = ""
    turn_started = False
    turn_done = False
    turn_count = 0
    lap_count = 0
    while not stop_event.is_set():
        color_obteined = tcs.get_color()

        if first_color_obteined == "":
            if color_obteined == "Orange" or color_obteined == "Blue":
                first_color_obteined = color_obteined


        if color_obteined == "Orange" and first_color_obteined == "Orange" and not turn_started:
            turn_started = True
            turn_done = False

        elif color_obteined == "Blue" and first_color_obteined == "Blue" and not turn_started:
            turn_started = True
            turn_done = False

        elif color_obteined == "Gray":   #this should be Gray but this to make a test
            turn_started = False

        
        if color_obteined == "Orange" and first_color_obteined == "Blue" and not turn_done: 
            turn_done = True
            turn_count += 1

        if color_obteined == "Blue" and first_color_obteined == "Orange" and not turn_done:
            turn_done = True
            turn_count += 1

        if MAIN.extra_lap:
            lap_count += 1
            MAIN.extra_lap = False

        if turn_count == 4:
            lap_count += 1
            turn_count = 0

        data = {
            "first_color_obteined": first_color_obteined,
            "color_obteined" : color_obteined,
            "turns": turn_count,
            "laps": lap_count 
        }

        try:
            with open("Libraries/Json/tcs_color_detection.json", "w", encoding='utf-8') as j:
                json.dump(data, j, indent=4, ensure_ascii=False)
        except TypeError as e:
            print(f"Error: {e} - data is not JSON-serializable")
        except FileNotFoundError:
            print("El archivo no existe")
        except PermissionError:
            print("No tienes permisos para escribir el archivo")
        except OSError as e:
            print("Error al escribir el archivo:", e)
        except  Exception as e:
            print(f"Error: {e}")

        # Optional sleep to reduce the frequency of measurements
        time.sleep(0.1)
        # print(turn_done)
        

threads = []
stop_event = threading.Event()
signal.signal(signal.SIGINT, signal_handler)

data = {
            "first_color_obteined": "",
            "color_obteined" : "",
            "turns": 0,
            "laps": 0 
        }

def start_threds():
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