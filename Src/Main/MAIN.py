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

def TD(): # turn distance
    return (M.pi * (11 / M.sin(alpha)))/2

def DFL(): # distance to first line
    return M.tan(alpha) * Wall_dist

def AD(): # aproximation distance
    return Wall_dist - TD()

if __name__ == "__main__":
    while True:
        if B.button_state() == True:
            while True:
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

                with open("tsc_color_dtection.json", "r", encoding="utf-8") as T:
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
                    # If total distance to the walls is less than 1m
                    if HC1 + HC3 <=100: 
                        # If to much to the right
                        if HC1 <= (HC1 + HC3)/2-10: 
                            MD.move(1,-100) # Turn left
                        # If to much to the left
                        elif HC3 <= (HC1 + HC3)/2-10: 
                            MD.move(1,100) # Turn right
                        else:
                            MD.move(1,0) # Continue forward

                    # else:
                    #     # If there is more distance to the right than the left
                    #     if HC1 > HC3: 
                    #         prev_front = HC0 # Save distance to front walls
                    #         MD.move(1,100) # Turn to right until the front walls it's at the left
                    #         while not HC3 == range(prev_front-30,prev_front):  time.sleep(.25)
                    #         MD.move(1,0) # Continue forward until abandoning the corner
                    #         while HC1 + HC3 >= 150: time.sleep(.25)
                    #         turns += 1

                    #     # If there is more distance to the left than the right
                    #     elif HC1 < HC3: 
                    #         prev_front = HC0 # Save distance to front walls
                    #         MD.move(1,-100) # Turn to right until the front walls it's at the right
                    #         while not HC3 <= prev_front:  time.sleep(.25)
                    #         MD.move(1,0) # Continue forward until abandoning the corner
                    #         while HC1 + HC3 >= 150: time.sleep(.25)
                else:
                    if direction == "":
                        