#PRUEBA_M.py
import time
import MOTOR_DRIVER as MD

vel = int(input("PERCENT VEL: "))
dir = int(input("PERCENT DIR: "))

while True:
    MD.move(vel, dir)