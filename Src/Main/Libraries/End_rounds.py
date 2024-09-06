from Libraries import MOTOR_DRIVER as M
import json

def parking(half_turn): 
    phase = 0
    prev_right_dis = 0
    prev_left_dis = 0

    with open("Json/tcs_color_detection.json") as d:
            data = json.load(d)
            first_color = data["first_color_obteined"]
            if (first_color == "orange" and half_turn == False) or (first_color == "blue" and half_turn == True):
                direction = "der"
            elif (first_color == "orange" and half_turn == True) or (first_color == "blue" and half_turn == False):
                direction = "izq"
    
    while True:
        with open("Json/Move.json", "r", encoding="utf-8") as d:
            data = json.load(d)
            Fdis = data["HC0"]
            Rdis = data["HC1"]
            Bdis = data["HC2"]
            Ldis = data["HC3"]

            var_right_dis = prev_right_dis - Rdis
            prev_right_dis = var_right_dis

            var_left_dis = prev_left_dis - Rdis
            prev_left_dis = var_left_dis

        with open("Json/CAM.json", "r", encoding="utf-8") as d: 
            data = json.load(d)
            Cen = data["MagentaC"]
        
        if phase == 0:
            if Cen <= 300:
                M.move(30,-100)
            elif Cen >= 340:
                M.move(30,100)
            else:
                if Fdis <= 30:
                    M.move(50,0)
                else:
                    phase = 1
        if phase == 1:
            
            if direction == "right":
                if var_right_dis <= 15:
                    if Cen >=40:
                        M.move(30,100)
                    else:
                        M.move(50,0)
                else:
                    phase = 2
            else:
                if var_left_dis <= 15:
                    if Cen <=600:
                        M.move(30,-100)
                    else:
                        M.move(50,0)
                else:
                    phase = 2
        if phase == 2:
            if Fdis >= 10:
                if direction == "right":
                    M.move(100,-100)
                else:
                    M.move(100,100)
            else:
                phase = 3
        if phase == 3:
            M.move(0,0)
            print("YOU'VE WON :)")

def home_sweet_home(first_front_distance, first_right_distance):
    traction = 0
    direction = 0
    while True:
        with open("Json/Move.json", "r", encoding='utf-8') as f:
            Move = json.load(f)
            front_distance = Move["HC0"]
            right_distance = Move["HC1"]

        if front_distance < first_front_distance:
            traction = 100

        else:
            traction = -100


        if right_distance > first_right_distance:
            direction = 100

        else:
            direction = -100

        M.move(traction, direction)

        if (first_front_distance - 3) < front_distance < (first_front_distance + 3):
            if (first_right_distance - 3) < right_distance < (first_right_distance + 3):
                M.move(0, 0)
                break

    print("YOU'VE WON :)")
