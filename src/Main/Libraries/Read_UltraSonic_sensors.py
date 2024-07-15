# This Library is for reading the threads of the Ultrasonic sensors

import time
import os

# This function reads the distance from the specified sensor
def read_HC(i):
    file_path = f"/tmp/sensor_{i}.txt"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            content = file.read().strip()  # Read and strip any extra whitespace/newlines
            return content
    else:
        return ""

while True:
    for i in range(4):
        distance = read_HC(i)
        print(f"distance{i}: {distance}")
    time.sleep(0.5)  # Pausa para evitar uso excesivo de CPU
