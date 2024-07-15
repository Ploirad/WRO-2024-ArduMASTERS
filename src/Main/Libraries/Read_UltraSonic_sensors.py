# This Library is for reading the threads of the Ultrasonic sensors

import time
import os

last_distance = 0
last_distance_0 = 0
last_distance_1 = 0
last_distance_2 = 0
last_distance_3 = 0

# This function reads the distance from the specified sensor
def read_HC(i):
    global last_distance, last_distance_0, last_distance_1, last_distance_2, last_distance_3
    if i == 0:
        last_distance = last_distance_0
    elif i == 1:
        last_distance = last_distance_1
    elif i == 2:
        last_distance = last_distance_2
    elif i == 3:
        last_distance = last_distance_3
    
    file_path = f"/tmp/sensor_{i}.txt"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                content = file.read().strip()  # Read and strip any extra whitespace/newlines
                distance = float(content)
                if i == 0:
                    last_distance_0 = distance
                elif i == 1:
                    last_distance_1 = distance
                elif i == 2:
                    last_distance_2 = distance
                elif i == 3:
                    last_distance_3 = distance
                return distance
            except ValueError:
                return last_distance
    else:
        return 10000000.987654321

while True:
    for i in range(4):
        distance = read_HC(i)
        print(f"distance{i}: {distance}")
    print("")
    time.sleep(1)