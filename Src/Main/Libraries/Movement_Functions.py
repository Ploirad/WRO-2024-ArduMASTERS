# Libraries
import time
from Libraries import MOTOR_DRIVER as MD                # MD.move(percent_vel, percent_dir)
import json
import os

# Controls robot movement based on direction data from the json file of the camera
def pivot_aproximation(last_direction, color_detected):
    print("sign detected")
    traction = 25
    opposite_direction = -last_direction
    post_reached = False
    post_passed = False
    side = 0
    last_side = 0

    while True:
        try:
            with open(os.path.join(os.path.dirname(__file__), "Json", "Move.json"), 'r', encoding='utf-8') as HC_detection:
                HC_detection_data = json.load(HC_detection)
                print(HC_detection_data)
                front_distance =  HC_detection_data["HC0"]
                right_distance = HC_detection_data["HC1"]
                left_distance = HC_detection_data["HC3"]

            if  front_distance < 10 or front_distance > 2000:
                backward(traction, last_direction)

            if color_detected == "green":
                side = right_distance
            else:
                side = left_distance


            if (last_side - side) > 30:
                    post_reached = True
                    print("post reached")
            last_side = side

            if post_reached and (side - last_side) > 30:
                post_passed = True

            MD.move(traction, last_direction)

        except:
            print("Error 1 reading json files")
        finally:
            if post_passed:
                break
    print("sign passed")
    turn_timer_start = time.time()
    turn_timer_stop = time.time()

    while turn_timer_stop - turn_timer_start  < 1.5:
        try:
            with open (os.path.join(os.path.dirname(__file__), "Json", "CAM.json"), 'r', encoding='utf-8') as camera_color:
                camera_color_data = json.load(camera_color)
                print(camera_color_data)
                color =  camera_color_data["Color"]

            if color != "" or "magenta":
                print("another sign detected")
                pivot_aproximation(last_direction, camera_color)
                return 
            turn_timer_stop = time.time()
            MD.move(25, opposite_direction)
        except:
            print("Error 2 reading json files")
    print("Nothing found")
    MD.move(25, last_direction)
    time.sleep(1.5)
        



# This function is for go backward in the MAIN code
def backward(traction, initial_direction):
    print("BACKWARD STARTED")
    traction = abs(traction)
    while True:
        with open(os.path.join(os.path.dirname(__file__), "Json", "Move.json"), "r", encoding='utf-8') as f:
            Move = json.load(f)
            front_distance = Move["HC0"]
            back_distance = Move["HC2"]

        while front_distance < 40 or back_distance > 100:
            MD.move(-traction, -initial_direction)
            with open(os.path.join(os.path.dirname(__file__), "Json", "Move.json"), "r", encoding='utf-8') as f:
                Move = json.load(f)
                front_distance = Move["HC0"]
                back_distance = Move["HC2"]

        MD.move(traction, initial_direction)
        time.sleep(1)

        if front_distance > 50:
            break

# This function is for turn 180 degrees the car
def change_direction():
    normal_traction = 100
    print("Backward and right")
    MD.move(-100, normal_traction)
    print("delay 1.5s")
    time.sleep(1.5)
    print("Forward and left")
    MD.move(100, -normal_traction)
    print("delay 1.5s")
    time.sleep(1.5)
    print("Direction changed")
