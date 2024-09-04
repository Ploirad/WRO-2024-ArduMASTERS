import time
from Libraries import MOTOR_DRIVER as MD

while True:
    vel_r = float(input("PERCENT VEL FOR THE RIGHT: "))
    vel_l = float (input("PERCENT VEL FOR THE LEFT: "))
    vel = (vel_l, vel_r)
    dir = float(input("PERCENT DIR: "))
    MD.move(vel, dir)
    time.sleep(4)