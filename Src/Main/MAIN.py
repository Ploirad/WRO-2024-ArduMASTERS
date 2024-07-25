import json
import time
from Libraries import MOTOR_DRIVER as Motor
from Libraries import Boton
#from Libraries import parking

can_start = False

tim = float(input("Tim: "))

while True:
    try:
        if can_start:
            traction = 0
            direction = 0
            with open("CAM.json", "r", encoding='utf-8') as f:
                CAM = json.load(f)
                print(CAM)

                if "TRACTION" in CAM and "DIRECTION" in CAM:
                    traction = int(CAM["TRACTION"])
                    direction = int(CAM["DIRECTION"])

                if CAM["Parking"]:
                    print("parking")#parking.parking()
                
                else:
                    if CAM["Ignore"]:
                        print("Ignore CAM")
                        with open("Move.json", "r", encoding='utf-8') as f:
                            Move = json.load(f)
                            print(Move)

                            if "TRACTION" in Move and "DIRECTION" in Move:
                                traction = int(Move["TRACTION"])
                                direction = int(Move["DIRECTION"])

                            else:
                                print("Invalid data format in JSON file")

            with open("tcs_color_detection.json", "r", encoding='utf-8') as f:
                tcs = json.load(f)
                print(tcs)

                laps = tcs["laps"]

                if laps >= 3:
                    print("OK")
                    break

                Motor.move(traction, direction)
                if traction < 0:
                    time.sleep(tim)

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
