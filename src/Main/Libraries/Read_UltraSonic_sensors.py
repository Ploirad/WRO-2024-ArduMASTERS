# This Library is for read the threads of the Ultrasonic sensors

# This function returns a list of distances:
# [Front_Distance, Right_Distance, Back_Distance, Left_Distance]
def read_HC():

    # First we initialize and clear the list of distances
    dists = []
    dists.clear()

    # Then we travel by the four archives of distances
    for i in range(4):
        # Then we read the distance of the sensor
        file_path = f"/tmp/sensor_{i}.txt"
        
        with open(file_path, "r") as file:
            # Then we save the content of the archive in the list
            content = file.read()
            if content:
                dists.append(content)
    
    # Finally we return the list
    return dists


# Example of use:
while True:
    d = read_HC()
    print(f"D: {d}")
    print("")