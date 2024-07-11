# General Libraries
from External_Libraries import time

# Our general Libraries:
from Libraries import MOTOR_DRIVER as MD           # MD.move(percent_vel, percent_dir)
from Libraries import Ultrasonidos as HC

def backward(traction, initial_direction):
    print("BACKWARD STARTED")
    traction = abs(traction)
    front_distance = HC.measure_distance(1)
    while front_distance < 25:
        print(f"bkwrd: t:{-traction} and d:{-initial_direction}")
        MD.move(-traction, -initial_direction)
        front_distance = HC.measure_distance(1)
    MD.move(traction, initial_direction)
    print("BACKWARD ENDED")

def change_direction():
    print("Backward and right")
    MD.move(-100, 100)
    print("delay 5s")
    time.sleep(5)
    print("Forward and left")
    MD.move(100, -100)
    print("delay 2s")
    time.sleep(2)
    print("Direction changed")