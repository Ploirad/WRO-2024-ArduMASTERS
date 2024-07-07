# General Libraries of we:
from Libraries import MOTOR_DRIVER as MD           # MD.move(percent_vel, percent_dir)
from Libraries import Ultrasonidos as HC

def backward(traction, initial_direction):
    print("BACKWARD STARTED")
    traction = abs(traction)
    front_distance = HC.measure_distance(1)
    while front_distance < 30:
        print(f"bkwrd: t:{-traction} and d:{-initial_direction}")
        MD.move(-traction, -initial_direction)
        front_distance = HC.measure_distance(1)
    MD.move(traction, initial_direction)
    print("BACKWARD ENDED")