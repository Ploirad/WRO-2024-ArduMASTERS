# This Library is for read the threads of the Ultrasonic sensors

# This function
def read_HC(i):

    # First we initialize and clear the list of distances
    dists = []
    dists.clear()

    # Then we read the distance of the sensor
    file_path = f"/tmp/sensor_{i}.txt"
        
    with open(file_path, "r") as file:
    # Then we save the content of the archive in the list
        content = file.read()
        return content

print(read_HC(0))