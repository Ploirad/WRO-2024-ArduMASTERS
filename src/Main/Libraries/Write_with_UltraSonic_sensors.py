# This code is for write in text archives the distances of the sensors

# First we import the libraries
from External_Libraries import GPIO
from External_Libraries import time
from External_Libraries import threading

# Second we create two lists of the pins
TRIG = [23, 8, 17, 22]
ECHO = [24, 7, 27, 10]

# Third we configurate the GPIO
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

# This function is for write the distances in four archives
def write_distances(sensor_id):
    archive = f"/tmp/sensor_{sensor_id}.txt"
    trig = TRIG[sensor_id]
    echo = ECHO[sensor_id]

    with open(archive, "w") as f:
        for d in read_sensor_distance(trig, echo):
            f.write(str(d))

# Create and start the threats
threads = []
try:
    while True:
        for i in range(4):
            t = threading.Thread(target=write_distances, args=(i,))
            t.start()
            threads.append(t)
        # Wait for the end of the threats (in this case it doesn't happen)
        for t in threads:
            t.join()

except Exception as e:
    print(f"eWRITE = {e}")
finally:
    # Clean the GPIO at the end
    GPIO.cleanup()