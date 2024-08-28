# Libraries
import time
import MOTOR_DRIVER as MD                # MD.move(percent_vel, percent_dir)
import json
import os

move_json = os.path.join(os.path.dirname(__file__), "..","../Json", "Move.json")

# This function is for go backward in the MAIN code
def backward(traction, initial_direction):
    print("BACKWARD STARTED")
    traction = abs(traction)
    while True:
        with open("move_json", "r", encoding='utf-8') as f:
            Move = json.load(f)
            front_distance = Move["HC0"]
            back_distance = Move["HC2"]
        
        while front_distance < 40 or back_distance > 100:
            MD.move(-traction, -initial_direction)
            with open("move_json", "r", encoding='utf-8') as f:
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