extra_lap = False

if __name__ == "__main__":
    import json
    import time
    from Libraries import MOTOR_DRIVER as Motor
    from Libraries import Boton
    import Libraries.Movement_Functions as F
    import Libraries.End_rounds as End

    dir_changed = False
    can_start = False
    laps_ended = False
    possible_changing_direction = False
    last_pillar = ""
    tcs_color = ""
    first_front_distance = 0
    first_right_distance = 0
    first_loop_done = False
    second_challenge = False
    tim = 1.5
    while True:
        try:
            if can_start:
                if not first_loop_done:
                    with open("Libraries/Json/Move.json", "r", encoding='utf-8') as f:
                        Move = json.load(f)
                        first_front_distance = Move["HC0"]
                        first_right_distance = Move["HC1"]
                    first_loop_done = True

                traction = 0
                direction = 0
                with open("Libraries/Json/CAM.json", "r", encoding='utf-8') as f:
                    CAM = json.load(f)
                    print(CAM)
                    color = CAM["Color"]

                    if color != "" :
                        second_challenge = True

                    if possible_changing_direction and color != "":
                        last_pillar = color

                    if laps_ended:
                        if second_challenge and color == "magenta":
                            End.parking(dir_changed)
                        else:
                            if tcs_color == "Gray":
                                End.home_sweet_home(first_front_distance, first_right_distance)
                                break

                    if (color != "" and color != "magenta"):
                        F.pivot_aproximation(CAM["DIRECTION"], CAM["Color"])

                    elif color == "":
                        print("Ignore CAM")
                        try:
                            with open("Libraries/Json/Move.json", "r", encoding='utf-8') as f:
                                Move = json.load(f)
                                print(Move)

                                traction = int(Move["TRACTION"])
                                direction = int(Move["DIRECTION"])

                        except Exception as e:
                            print(e)

                with open("Libraries/Json/tcs_color_detection.json", "r", encoding='utf-8') as f:
                    tcs = json.load(f)
                    print(tcs)

                    laps = tcs["laps"]
                    tcs_first_color = tcs["first_color_obteined"]
                    turns = tcs["turns"]
                    tcs_color = tcs["color_obteined"]

                    if laps == 1 and turns == 3 and second_challenge:
                        possible_changing_direction = True

                    if tcs_first_color == tcs_color and possible_changing_direction:
                        if last_pillar == "red":
                            F.change_direction()
                            dir_changed = True
                        possible_changing_direction = False
                        extra_lap = True

                    if laps >= 3:
                        print("OK")
                        laps_ended = True

                Motor.move(traction, direction)

            else:
                print("Waiting for start signal")
                if Boton.button_state():
                    can_start = True

        except FileNotFoundError as e:
            print(f"file not found. Make sure the file {e} exists")
        except json.JSONDecodeError:
            print("Error decoding JSON. Ensure the JSON format is correct.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        # Optional sleep to avoid excessive CPU usage
        time.sleep(0.1)