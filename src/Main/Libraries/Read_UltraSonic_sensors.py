dists = []
distances = []

def read_HC():
    global dists, distances
    for i in range(4):
        file_path = f"/tmp/sensor_{i}.txt"
        with open(file_path, "r") as file:
            content = file.read()
            dists.append(content)
    distances.append(dists)
    dists.clear()
    return dists

while True:
    print(read_HC())