from Libraries import MOTOR_DRIVER as M
import json
import os
import time

def parking(half_turn): 
    phase = 0
    first_color = ""
    direction = ""
    prev_right_dis = 0
    prev_left_dis = 0
    with open(os.path.join(os.path.dirname(__file__), "Json", "tcs_color_detection.json")) as d:
        data = json.load(d)
        first_color = data["first_color_obteined"]
    if (first_color == "orange" and half_turn == False) or (first_color == "blue" and half_turn == True):
        direction = "right"
    elif (first_color == "orange" and half_turn == True) or (first_color == "blue" and half_turn == False):
        direction = "left"
    
    while True:
        try:
            with open(os.path.join(os.path.dirname(__file__), "Json", "Move.json"), "r", encoding="utf-8") as d:
                data = json.load(d)
                Fdis = data["HC0"]
                Rdis = data["HC1"]
                Bdis = data["HC2"]
                Ldis = data["HC3"]
                print(f" Front distance: {Fdis}, Right distance: {Rdis}")

                var_right_dis = prev_right_dis - Rdis
                prev_right_dis = Rdis

                var_left_dis = prev_left_dis - Ldis
                prev_left_dis = Ldis

            with open(os.path.join(os.path.dirname(__file__), "Json", "CAM.json"), "r", encoding="utf-8") as d: 
                data = json.load(d)
                Cen = data["MagentaC"]
            
            if phase == 0:
                print("phase 0")
                if Cen == None:
                    M.move(0,0)
                elif Cen <= 300:
                    M.move(25,-100)
                elif Cen >= 340:
                    M.move(25,100)
                else:
                    if Fdis <= 30:
                        M.move(25,0)
                    else:
                        phase = 1
            
            if phase == 1:
                print("phase 1")
                if direction == "right":
                    if var_right_dis <= 15:
                        if Cen >= 40:
                            M.move(25,100)
                        else:
                            M.move(25,0)
                    else:
                        phase = 2
                else:
                    if var_left_dis <= 15:
                        if Cen <=600:
                            M.move(25,-100)
                        else:
                            M.move(25,0)
                    else:
                        phase = 2
            
            if phase == 2:
                print("phase 2")
                if direction == "right":
                    M.move(25,100)
                    time.sleep(2)
                    phase = 3
                else:
                    M.move(25,-100)
                    time.sleep(2)
                    phase = 3

            if phase == 3:
                if Bdis >= 1:
                    M.move(-25,0)
                else:
                    phase = 4

            if phase == 4:
                print("phase 3")
                M.move(0,0)
                print("YOU'VE WON :)")
        
        except Exception as e:
            if e == KeyboardInterrupt:
                break
            print(e)
            print(e.__traceback__.tb_lineno)

def home_sweet_home(first_front_distance, first_right_distance):
    traction = 0
    direction = 0
    while True:
        with open(os.path.join(os.path.dirname(__file__), "Json", "Move.json"), "r", encoding='utf-8') as f:
            Move = json.load(f)
            front_distance = Move["HC0"]
            right_distance = Move["HC1"]

        if front_distance < first_front_distance:
            traction = 25

        else:
            traction = -25


        if right_distance > first_right_distance:
            direction = 100

        else:
            direction = -100

        M.move(traction, direction)

        if (first_front_distance - 10) < front_distance < (first_front_distance + 10):
            if (first_right_distance - 10) < right_distance < (first_right_distance + 10):
                M.move(0, 0)
                break

    print("YOU'VE WON :)")
