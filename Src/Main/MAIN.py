import json
import time
from Libraries import MOTOR_DRIVER as MD
from Libraries import Boton as B
import Libraries.Movement_Functions as F
import Libraries.End_rounds as End
import math as M

Phase = 0 # initial phase, unknown direcction
direction = ""
alpha = 30 # Car turning angle
phase = 0
button_pressed = False
time_to_90_degrees = 5
color_has_been_detected = False

def TD(): # turn distance
    return (M.pi * (11 / M.sin(alpha)))/2

def DFL(): # distance to first line
    return M.tan(alpha) * Wall_dist

def AD(): # aproximation distance
    return Wall_dist - TD()

if __name__ == "__main__":
    while True:
        if button_pressed:
            with open("Libraries/Json/CAM.json","r", encoding="utf-8") as C:
                cam_data = json.load(C)

                color = cam_data["Color"]
                ignore = cam_data["Ignore"]
                
                RC = cam_data["RedC"]
                GC = cam_data["GreenC"]
                MC = cam_data["MagentaC"]
            
                RA = cam_data["MArea"]
                GC = cam_data["GArea"]
                MA = cam_data["MArea"]

                parking = cam_data["Parking"]

            with open("Libraries/Json/tsc_color_detection.json", "r", encoding="utf-8") as T:
                tcs_data = json.load(T)

                direction = tcs_data["first_color_obteined"]
                Color = tcs_data["color_obteined"]
                turns = tcs_data["turns"]
                laps = tcs_data["laps"]

            with open("Libraries/Json/Move.json", "r", encoding="utf-8") as M:
                HC_data = json.load(M)

                HC0 = HC_data["HC0"]
                HC1 = HC_data["HC1"]
                HC2 = HC_data["HC2"]
                HC3 = HC_data["HC3"]

                if direction == "blue":
                    Wall_dist = 95 - HC1
                    print("Anticlockways direccion")
                elif direction == "orange":
                    Wall_dist = 95 - HC3
                    print("Clockways direccion")
                else:
                    print("Unknown direcction") 
    
            if ignore == True:
                if round == 3:
                    if color_has_been_detected:
                        if parking == True:
                            End.parking()
                    else:
                        End.home_sweet_home()

                if Color == "unknown" or Color == "gray":
                    if HC1+HC3 > ((HC1+HC3)/2)-15:
                        # If there is more distance to the right than the left
                        if HC1 > HC3: 
                            prev_front = HC0 # Save distance to front walls
                            MD.move(25, 100) # Turn to right until the front walls it's at the left
                            while not HC3 == range(prev_front-30,prev_front):  time.sleep(0.25)
                            MD.move(25, 0) # Continue forward until abandoning the corner
                            while HC1 + HC3 >= 150: time.sleep(0.25)
                            turns += 1

                        # If there is more distance to the left than the right
                        elif HC1 < HC3: 
                            prev_front = HC0 # Save distance to front walls
                            MD.move(25, -100) # Turn to right until the front walls it's at the right
                            while not HC3 <= prev_front:  time.sleep(0.25)
                            MD.move(25, 0) # Continue forward until abandoning the corner
                            while HC1 + HC3 >= 150: time.sleep(0.25)
                else:
                    if Color == "blue":
                        MD.move(25, -100)
                        time.sleep(time_to_90_degrees)
                        color_has_been_detected = True
                    elif Color == "orange":
                        MD.move(25, 100)
                        time.sleep(time_to_90_degrees)
                        color_has_been_detected = True
            else:
                if color == "green" or color== "red":
                    F.pivot_aproximation(color)
        else:
            if B.button_state() == True:
                print("Button pressed")
                button_pressed = True