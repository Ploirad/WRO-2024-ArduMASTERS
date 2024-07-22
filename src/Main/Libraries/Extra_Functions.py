# Libraries
import time
from Libraries import MOTOR_DRIVER as MD                # MD.move(percent_vel, percent_dir)
from Libraries import Read_UltraSonic_sensors as RHC    # RHC.read_HC(i); 0/1/2/3 = FD/RD/BD/LD

# This function is for go backward in the MAIN code
def backward(traction, initial_direction):
    print("BACKWARD STARTED")
    traction = abs(traction)
    front_distance = RHC.read_HC(0)
    right_distance = RHC.read_HC(1)
    left_distance = RHC.read_HC(3)
    while front_distance < 30:
        if right_distance > left_distance:
            direction = -100
        else:
            direction = 100
        MD.move(-traction, -direction)
        front_distance = RHC.read_HC(0)
        right_distance = RHC.read_HC(1)
        left_distance = RHC.read_HC(3)

    MD.move(traction, direction)
    time.sleep(1)
    # while True:
    #     front_distance = RHC.read_HC(0)
    #     right_distance = RHC.read_HC(1)
    #     left_distance = RHC.read_HC(3)
    #     if right_distance <= 85 and left_distance <= 85:
    #         break
    #     elif right_distance > 86:
    #         MD.move(traction, -100)
    #     else:
    #         MD.move(traction, 100)
    MD.move(traction, 0)
    print("BACKWARD ENDED")

# This function is for turn 180 degrees the car
def change_direction():
    normal_traction = 100
    print("Backward and right")
    MD.move(-100, normal_traction)
    print("delay 5s")
    time.sleep(1.5)
    print("Forward and left")
    MD.move(100, -normal_traction)
    print("delay 2s")
    time.sleep(1.5)
    print("Direction changed")
