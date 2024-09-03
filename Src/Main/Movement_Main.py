import Libraries.MOTOR_DRIVER as M
import time
import threading
import signal
import sys
import json

data = None

# Handler for SIGN to stop threads
def signal_handler(sig, frame):
    global stop_event
    stop_event.set()

def main(stop_event):
    while not stop_event:
        with open("Libraries/Json/Movement.json","r",encoding='utf-8') as j:
            data = json.load(j)
            print(f"MVMNT-MN:{data}")

        M.move(data["traccion"],data["direccion"])


# Create and start the threads
threads = []
stop_event = threading.Event()
signal.signal(signal.SIGINT, signal_handler)

try:
    t = threading.Thread(target=main, args=(stop_event,))
    t.start()
    threads.append(t)

    # Wait for the end of the threads (in this case it doesn't happen unless interrupted)
    for t in threads:
        t.join()

except Exception as e:
    print(f"Error: {e}")
finally:
    # Clean the GPIO at the end
    M.GPIO.cleanup()