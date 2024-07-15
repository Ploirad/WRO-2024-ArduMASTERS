# This Library is for reading the threads of the Ultrasonic sensors

# This are the libraries used
from External_Libraries import time
from External_Libraries import os

# This variables are for save the lasts distances read
last_distance = 0
last_distance_0 = 0
last_distance_1 = 0
last_distance_2 = 0
last_distance_3 = 0

# This function reads the distance from the specified sensor
def read_HC(i):
    # We use all this variables
    global last_distance, last_distance_0, last_distance_1, last_distance_2, last_distance_3
    
    # We save in last_distance the last distance of the sensor (0, 1, 2 or 3)
    if i == 0:
        last_distance = last_distance_0
    elif i == 1:
        last_distance = last_distance_1
    elif i == 2:
        last_distance = last_distance_2
    elif i == 3:
        last_distance = last_distance_3
    
    # This is the path of the archive
    file_path = f"/tmp/sensor_{i}.txt"

    # If the path exists
    if os.path.exists(file_path):

        # We open it in read mode
        with open(file_path, "r") as file:
            try:
                # We read the distance from the archive
                content = file.read().strip()
                # We convert the string to a float
                distance = float(content)

                # We save the distance in the specific variable
                if i == 0:
                    last_distance_0 = distance
                elif i == 1:
                    last_distance_1 = distance
                elif i == 2:
                    last_distance_2 = distance
                elif i == 3:
                    last_distance_3 = distance

                # And finnally we return the distance of the sensor
                return distance
            
            # If we can't execute the change from string to float we return the last distance of the sensor
            except ValueError:
                return last_distance
            
    # If the path doesn't exists we return a value
    else:
        return 100

# Example of usage
# while True:
    # for i in range(4):
        # distance = read_HC(i)
        # print(f"distance{i}: {distance}")
    # print("")
    # time.sleep(1)