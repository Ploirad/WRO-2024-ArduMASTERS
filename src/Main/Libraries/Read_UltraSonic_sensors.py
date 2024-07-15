# This Library is for read the threads of the Ultrasonic sensors

import time
import os

# This function reads the distance from the specified sensor
def read_HC(i):
    file_path = f"/tmp/sensor_{i}.txt"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            content = file.read()
            return content
    else:
        return ""

while True:
    print(read_HC(0))
    time.sleep(0.5)  # Pausa para evitar uso excesivo de CPU
