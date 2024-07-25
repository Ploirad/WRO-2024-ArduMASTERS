import json
import time
from Libraries import MOTOR_DRIVER as Motor
from Libraries import Boton

can_start = False

tim = float(input("Tim: "))

while True:
    try:
        if can_start:
            with open("Move.json", "r", encoding='utf-8') as f:
                data = json.load(f)
                print(data)

                if "TRACTION" in data and "DIRECTION" in data:
                    traction = int(data["TRACTION"])
                    direction = int(data["DIRECTION"])

                    Motor.move(traction, direction)

                    if traction < 0:
                        time.sleep(tim)
                else:
                    print("Invalid data format in JSON file")

        else:
            print("Waiting for start signal")
            if Boton.button_state():
                can_start = True

    except FileNotFoundError:
        print("Move.json file not found. Make sure the file exists.")
    except json.JSONDecodeError:
        print("Error decoding JSON. Ensure the JSON format is correct.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Optional sleep to avoid excessive CPU usage
    time.sleep(0.1)
