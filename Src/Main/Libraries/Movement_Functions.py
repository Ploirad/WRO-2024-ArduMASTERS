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
                
                if (int(GA) <= 50 and target == "green") or (int(RA) <= 50 and target == "red"):
                    phase = 2

                if phase == 3:
                    if var_distance >= 30:
                        MD.move(25,0)
                    else:
                        return target
                    
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
                Move = json.load(f)
                front_distance = Move["HC0"]
                back_distance = Move["HC2"]

        MD.move(traction, initial_direction)
        time.sleep(1)

        if front_distance > 50:
            break

# This function is for turn 180 degrees the car
def change_direction():
    phase = 0 
    with open(os.path.join(os.path.dirname(__file__), "Json", "Move.json"), "r", encoding='utf-8') as M:       
        Ultrasonic_data = json.load(M)
        left_distance = Ultrasonic_data["HC3"]
        right_distance = Ultrasonic_data["HC1"]
    with open(os.path.join(os.path.dirname(__file__), "Json", "tcs_color_detection.json"), "r", encoding='utf-8') as T:
        Tcs_data = json.load(T)
        orientation = Tcs_data["first_color_obteined"]
    if (left_distance  < 60 and  orientation == "orange") or (right_distance  < 60 and  orientation == "blue"):
        zone = "left"
    else:
        zone = "right"
    while True:
        with open(os.path.join(os.path.dirname(__file__), "Json", "Move.json"), "r", encoding='utf-8') as M:       
            Ultrasonic_data = json.load(M)
            front_distance = Ultrasonic_data["HC0"]
            right_distance = Ultrasonic_data["HC1"]
            back_distance = Ultrasonic_data["HC2"]
            left_distance = Ultrasonic_data["HC3"]

        with open(os.path.join(os.path.dirname(__file__), "Json", "tcs_color_detection.json"), "r", encoding='utf-8') as T:
            Tcs_data = json.load(T)
            color = Tcs_data["color_obteined"]
            orientation = Tcs_data["first_color_obteined"]
        
        with open(os.path.join(os.path.dirname(__file__), "Json", "CAM.json"), "r", encoding='utf-8') as C:
            cam_data = json.load(C)
            ignore = cam_data["Ignore"]
       
        if phase == 0:
            if orientation == "blue":
                if zone ==  "left":
                    MD.move(25, -100)
                else:
                    MD.move(25, 100)
            else:
                if zone ==  "left":
                    MD.move(25, 100)
                else:
                    MD.move(25, -100)
            if zone == "left":
                if color == "Gray":
                    phase = 1
            else:
                if front_distance <= 5:
                    phase = 1

        if phase == 1:
            MD.move(-25, 0)
            if zone == "left":
                if back_distance <= 5:
                    phase = 2
            else: 
                if (color == "Blue" and orientation == "Orange") or (color == "Orange" and orientation == "Blue"):
                    phase = 2
        
        if phase == 2:
            if zone == "left":
                if orientation == "blue":
                    MD.move(25,-100)
                else:
                    MD.move(25,100)
            else:
                if orientation == "blue":
                    MD.move(25,100)
                else:
                    MD.move(25,-100)


            if color == "Gray":
                break
