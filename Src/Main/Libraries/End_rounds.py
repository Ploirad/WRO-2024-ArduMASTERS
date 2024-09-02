from Libraries import MOTOR_DRIVER as Motor
import json
import os

cam_json = os.path.join(os.path.dirname(__file__), "..", "Json", "CAM.json")
move_json = os.path.join(os.path.dirname(__file__), "..","../Json", "Move.json")



def parking(): 
    starting_back_distance = 0.0
    left_distance = 0.0
    right_distance = 0.0
    back_distance = 0.0
    color = ""
    parking_position = 0
    
    with open("move_json", "r", encoding='utf-8') as f:
        Move = json.load(f)
        print(Move)
        left_distance = float(Move["HC3"])
        right_distance = float(Move["HC1"])
        back_distance = float(Move["HC2"])

    with open("cam_json", "r", encoding='utf-8') as f:
        CAM = json.load(f)
        print(CAM)
        color = CAM["Color"]
        magenta_centroid = CAM["MagentaC"]
    
    if magenta_centroid <= 320:
        parking_position = -100
    else:
        parking_position = 100
    
    while left_distance < 30:
        Motor.move(100, -parking_position)
        with open("move_json", "r", encoding='utf-8') as f:
            Move = json.load(f)
            left_distance = float(Move["HC3"])
    
    while right_distance < 30:
        Motor.move(100, -100)
        with open("move_json", "r", encoding='utf-8') as f:
            Move = json.load(f)
            right_distance = float(Move["HC1"])

    while color == "Magenta":
        with open("cam_json", "r", encoding='utf-8') as f:
            color = CAM["Color"]
        Motor.move(100, 0)
    
    with open("move_json", "r", encoding='utf-8') as f:
        Move = json.load(f)
        starting_back_distance = float(Move["HC2"])

    while (starting_back_distance + 27) <= back_distance: # 27 is the car lenght (+1)
        Motor.move(100, 0)
        with open("move_json", "r", encoding='utf-8') as f:
            Move = json.load(f)
            back_distance = float(Move["HC2"])

    while back_distance > 10:
        Motor.move(-100, parking_position)
        with open("move_json", "r", encoding='utf-8') as f:
            Move = json.load(f)
            back_distance = float(Move["HC2"])

    while back_distance < 25:
        Motor.move(100, -parking_position)
        with open("move_json", "r", encoding='utf-8') as f:
            Move = json.load(f)
            back_distance = float(Move["HC2"])

    while back_distance > 5:
        Motor.move(100, parking_position)
        with open("move_json", "r", encoding='utf-8') as f:
            Move = json.load(f)
            back_distance = float(Move["HC2"])


def home_sweet_home(first_front_distance, first_right_distance):
    traction = 0
    direction = 0
    while True:
        with open("move_json", "r", encoding='utf-8') as f:
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

        Motor.move(traction, direction)

        if (first_front_distance - 3) < front_distance < (first_front_distance + 3):
            if (first_right_distance - 3) < right_distance < (first_right_distance + 3):
                Motor.move(0, 0)
                break

    print("YOU WON :)")
