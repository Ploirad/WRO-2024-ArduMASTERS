# Libraries
import time
from Libraries import MOTOR_DRIVER as MD                # MD.move(percent_vel, percent_dir)
import json

# Controls robot movement based on direction data from the json file of the camera 
def pibot_aproximation(last_direction):
    traction = 25
    opposite_direction = -last_direction
    with open("Json/CAM.json", 'r', encoding='utf-8') as CAM:
        CAM_data = json.load(CAM)
    
    if not CAM_data["ignore"]:
        with open("Json/CAM.json", 'r', encoding='utf-8') as C1:
            C1_data = json.load(C1)
            MD.move(traction, C1_data["DIRECTION"])
    else:
        MD.move(traction, opposite_direction)
        with open("Json/CAM.json", 'r', encoding='utf-8') as C2:
            C2_data = json.load(C2)
            if not C2_data["ignore"]:
                MD.move(traction, C2_data["DIRECTION"])

# This function is for go backward in the MAIN code
def backward(traction, initial_direction):
    print("BACKWARD STARTED")
    traction = abs(traction)
    while True:
        with open("Json/Move.json", "r", encoding='utf-8') as f:
            Move = json.load(f)
            front_distance = Move["HC0"]
            back_distance = Move["HC2"]

        while front_distance < 40 or back_distance > 100:
            MD.move(-traction, -initial_direction)
            with open("Json/Move.json", "r", encoding='utf-8') as f:
                Move = json.load(f)
                front_distance = Move["HC0"]
                back_distance = Move["HC2"]

        MD.move(traction, initial_direction)
        time.sleep(1)

        if front_distance > 100:
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
