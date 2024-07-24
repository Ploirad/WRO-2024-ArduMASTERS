import json
from Libraries import MOTOR_DRIVER as Motor

while True:
    with open("Move.json", "r") as f:
        data = json.load(f)
        print(data)

        traction = int(data["TRACTION"])
        direction = int(data ["DIRECTION"])

        Motor.move(traction, direction)