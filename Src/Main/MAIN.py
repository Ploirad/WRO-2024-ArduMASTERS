import json
import time
from Libraries import MOTOR_DRIVER as MD
from Libraries import Boton as B
import Libraries.Movement_Functions as F
import Libraries.End_rounds as End
import math as M

button_pressed = False
time_to_90_degrees = 5
half_turn = False

if __name__ == "__main__":
    while True:
        if button_pressed:
            with open(os.path.join(os.path.dirname(__file__),"Libraries/Json/CAM.json","r", encoding="utf-8") as C:
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

                orientation = tcs_data["first_color_obteined"]
                floor_color = tcs_data["color_obteined"]
                turns = tcs_data["turns"]
                laps = tcs_data["laps"]

            with open("Libraries/Json/Move.json", "r", encoding="utf-8") as M:
                HC_data = json.load(M)

                HC0 = HC_data["HC0"]
                HC1 = HC_data["HC1"]
                HC2 = HC_data["HC2"]
                HC3 = HC_data["HC3"]

            if laps == 1 and  turns == 3 and orientation == floor_color:
                if last_sign == "red":
                    F.change_direction()
                    half_turn = True
            
            if laps >= 3:
                    if parking == True:
                        End.parking(half_turn)
                    else:
                        End.home_sweet_home()

            if ignore == True:

                if floor_color == "unknown" or floor_color == "gray":
                    
                    if HC1 <= (HC1 + HC3)/2 - 10:
                        MD.move(25,-100)
                    if HC3 <= (HC1 + HC3)/2 - 10:
                        MD.move(25,100)
                    else:
                        MD.move(25,0)
                
                else:
                    if floor_color == "blue":
                        MD.move(25, -100)
                        time.sleep(time_to_90_degrees)
                
                    elif floor_color == "orange":
                        MD.move(25, 100)
                        time.sleep(time_to_90_degrees)

            else:
                if color == "green" or color== "red":
                    last_sign = F.pivot_aproximation(color)
        else:
            if B.button_state() == True:
                print("Button pressed")
                button_pressed = True