# Libraries
from External_Libraries import *
from Our_Libraries import *

# This function is for go backward in the MAIN code
def backward(traction, initial_direction):
    print("BACKWARD STARTED")
    traction = abs(traction)
    front_distance = RHC.read_HC(0)
    while front_distance < 25:
        print(f"bkwrd: t:{-traction} and d:{-initial_direction}")
        MD.move(-traction, -initial_direction)
        front_distance = RHC.read_HC(0)
    MD.move(traction, initial_direction)
    print("BACKWARD ENDED")

# This function is for turn 180 degrees the car
def change_direction():
    print("Backward and right")
    MD.move(-100, 25)
    print("delay 5s")
    time.sleep(1.5)
    print("Forward and left")
    MD.move(100, -25)
    print("delay 2s")
    time.sleep(1.5)
    print("Direction changed")