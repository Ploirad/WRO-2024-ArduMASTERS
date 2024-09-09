# Libraries
import time
from Libraries import MOTOR_DRIVER as MD                # MD.move(percent_vel, percent_dir)
import json
import os

# Controls robot movement based on direction data from the json file of the camera
def pivot_aproximation(last_direction):
    print("sign detected")
    traction = 25
    opposite_direction = -last_direction
    post_passed = False

    while True:
        with open(os.path.join(os.path.dirname(__file__), "Json", "Move.json"), 'r', encoding='utf-8') as HC_detection:
            HC_detection_data = json.load(HC_detection)
            front_distance =  HC_detection_data["HC0"]
            right_distance = HC_detection_data["HC1"]
            left_distance = HC_detection_data["HC3"]

        if  5 < front_distance or front_distance < 2000:
            backward(traction, last_direction)

        if front_distance > 30:
            if (right_distance < 15 and last_direction == -100) or (left_distance < 15 and last_direction == 100):
                post_passed = True
        if post_passed:
            break

        MD.move(traction, last_direction)
    print("sign passed")
    turn_timer_start = time.time()
    turn_timer_stop = time.time()

    while turn_timer_stop - turn_timer_start  < 1.5:
        with open(os.path.join(os.path.dirname(__file__), "Json", "CAM.json"), 'r', encoding='utf-8') as color_detection:
            color_detection_data = json.load(color_detection)
            camera_color =  color_detection_data["Color"]

        if camera_color != "" or "magenta":
            print("another sign detected")
            pivot_aproximation(last_direction)
            return 
        turn_timer_stop = time.time()
        MD.move(25, opposite_direction)
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
