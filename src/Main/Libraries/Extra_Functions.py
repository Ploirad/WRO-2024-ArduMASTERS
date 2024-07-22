# Libraries
import time
from Libraries import MOTOR_DRIVER as MD                # MD.move(percent_vel, percent_dir)
from Libraries import Read_UltraSonic_sensors as RHC    # RHC.read_HC(i); 0/1/2/3 = FD/RD/BD/LD

# This function is for go backward in the MAIN code
def backward(traction, initial_direction):
    print("BACKWARD STARTED")
    traction = abs(traction)
    while True:
        front_distance = RHC.read_HC(0)
        right_distance = RHC.read_HC(1)
        left_distance = RHC.read_HC(3)
        back_distance = RHC.read_HC(2)
        direction = 0

        if right_distance > left_distance:
            direction = 100
        else:
            direction = -100

        while back_distance > 20:
            MD.move(-traction, -direction)
            back_distance = RHC.read_HC(2)

        MD.move(traction, 0)
        time.sleep(2)

        if right_distance < 90 and left_distance < 90:
            break

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
