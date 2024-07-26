import json
import time
from Libraries import MOTOR_DRIVER as Motor
from Libraries import Boton
import End_rounds as End

can_start = False
waiting_magenta = False
tim = float(input("Tim: "))
tcs_color = ""
first_front_distance = 0
first_right_distance = 0
first_loop_done = False

while True:
    try:
        if can_start:
            if not first_loop_done:
                with open("Move.json", "r", encoding='utf-8') as f:
                    Move = json.load(f)
                    first_front_distance = Move["HC0"]
                    first_right_distance = Move["HC1"]
                first_loop_done = True

            traction = 0
            direction = 0
            with open("CAM.json", "r", encoding='utf-8') as f:
                CAM = json.load(f)
                print(CAM)

                color = CAM["Color"]
                ignore = CAM["Ignore"]

                if (color == "red" or color == "green" or color == "magenta") and not ignore:
                    second_round = True

                if waiting_magenta:
                    if second_round:
                        if color == "magenta":
                           End.parking()
                    else:
                        if tcs_color == "Gray":
                            End.home_sweet_home(first_front_distance, first_right_distance)
                            break

                if "TRACTION" in CAM and "DIRECTION" in CAM:
                    traction = int(CAM["TRACTION"])
                    direction = int(CAM["DIRECTION"])
                
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
                tcs_color = tcs["color_obtained"]

                if laps >= 3:
                    print("OK")
                    waiting_magenta = True

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
