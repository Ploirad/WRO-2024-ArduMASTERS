while True:
    for i in range(3):
        file_path = f"/tmp/sensor_{i}.txt"
        with open(file_path, "r") as file:
            content = file.read()
            print(f"content{i}: {content}") 
    print("")