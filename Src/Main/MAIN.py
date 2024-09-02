import json
import time
from Libraries import MOTOR_DRIVER as Motor
from Libraries import Boton
import Extra_Functions as F
import End_rounds as End

extra_lap = False

if __name__ == "__main__":
    can_start = False
    waiting_magenta = False
    possible_changing_direction = False
    last_pillar = ""
    tcs_color = ""
    first_front_distance = 0
    first_right_distance = 0
    first_loop_done = False
    second_round = False
    tim = 1.5
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

                    if second_round and possible_changing_direction and not ignore:
                        last_pillar = color

                    if waiting_magenta:
                        if second_round:
                            if color == "magenta":
                                End.parking()
                        else:
                            if tcs_color == "Gray":
                                End.home_sweet_home(first_front_distance, first_right_distance)
                                break

                    if ("TRACTION" in CAM and "DIRECTION" in CAM) and not CAM["Ignore"]:
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
                    tcs_first_color = tcs["first_color_obteined"]
                    turns = tcs["turns"]
                    tcs_color = tcs["color_obteined"]

                    if laps == 1 and turns == 3:
                        possible_changing_direction = True

                    if tcs_first_color == tcs_color and possible_changing_direction:
                        if last_pillar == "red":
                            F.change_direction()
                        possible_changing_direction = False
                        extra_lap = True

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