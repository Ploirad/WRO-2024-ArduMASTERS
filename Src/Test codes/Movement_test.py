import time
from Libraries import MOTOR_DRIVER as MD

try:
    while True:
        vel_l = float (input("PERCENT VEL FOR THE LEFT: "))
        vel_r = float(input("PERCENT VEL FOR THE RIGHT: "))
        vel = (vel_l, vel_r)
        dir = float(input("DIRECTION FOR THE CAR: "))
        MD.move(vel, dir)
        time.sleep(4)
except:
    MD.move((0,0), 0)