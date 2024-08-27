import time
from Libraries import MOTOR_DRIVER as MD

while True:
    vel = float(input("PERCENT VEL: "))
    dir = float(input("PERCENT DIR: "))
    MD.move(vel, dir)
    time.sleep(4)