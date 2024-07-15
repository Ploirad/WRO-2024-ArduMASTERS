# This code is for writing in text archives the distances of the sensors

# First we import the libraries
from External_Libraries import GPIO
from External_Libraries import time
from External_Libraries import threading
from External_Libraries import signal
from External_Libraries import sys

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

# This function is for writing the distances in four archives
def write_distances(sensor_id, stop_event):
    archive = f"/tmp/sensor_{sensor_id}.txt"
    trig = TRIG[sensor_id]
    echo = ECHO[sensor_id]

    for d in read_sensor_distance(trig, echo):
        if stop_event.is_set():
            break
        with open(archive, "w") as f:
            f.write(str(d) + "\n")
        time.sleep(0.1)  # Pausa para evitar uso excesivo de CPU

# Handler for SIGINT to stop threads
def signal_handler(sig, frame):
    global stop_event
    stop_event.set()

# Create and start the threads
threads = []
stop_event = threading.Event()
signal.signal(signal.SIGINT, signal_handler)

try:
    for i in range(4):
        t = threading.Thread(target=write_distances, args=(i, stop_event))
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
