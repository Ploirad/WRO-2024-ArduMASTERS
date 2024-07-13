import time
import MOTOR_DRIVER as MD

vel = float(input("PERCENT VEL: "))
dir = float(input("PERCENT DIR: "))

while True:
    MD.move(vel, dir)
    time.sleep(1)