# Libraries
import time
from Libraries import MOTOR_DRIVER as MD                # MD.move(percent_vel, percent_dir)
import json
import os

# Controls robot movement based on direction data from the json file of the camera
def pivot_aproximation(color):
    target = color
    phase = 0
    while True:
        try:
            with open(os.path.join(os.path.dirname(__file__), "Json", "Move.json"), 'r', encoding='utf-8') as M:
                HC_data = json.load(M)
                front_distance = HC_data["HCO"]
                var_distance = HC_data["HC1" if target=="green" else "HC3"] - prev_distance
                prev_distance = HC_data["HC1" if target=="green" else "HC3"]

            with open(os.path.join(os.path.dirname(__file__), "Json", "CAM.json"), 'r', encoding='utf-8') as C:
                cam_data = json.load(C)

                GA = cam_data["GArea"]
                RA = cam_data["RArea"]

                GC = cam_data["GreenC"]
                RC = cam_data["RedC"]
            if phase == 0:
                if (GC < -100 and target == "green") or (RC < -100 and target == "red"):
                    MD.move(25, -100)
                elif (GC > 100 and target == "green") or (RC > 100 and target == "red"):
                    MD.move(25, 100)
                else:
                    MD.move(25, 0)
                if front_distance < 15:
                    phase = 1
            if phase == 1:
                
                if target == "red":
                    if RC < 20: # If it's on the left side
                            MD.move(25, 0) # Forward
                        else:
                            MD.move(25, 100) # Turn right
                
                elif target == "green":
                    if GC > 620: # If it's on the left side
                        MD.move(25, 0) # Forward
                    else:
                        MD.move(25, -100) # Turn left
                
                if (int(GA) <= 50 and target == "green") or (int(RA) <= 50 and target == "red")
                    phase = 2

                if phase == 3
                    if var_distance >= 30    
                        MD.move(25,0)
                    else:
                        break
                
                    
        except:
            pass

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
                Move = json.l  ad(f)
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
