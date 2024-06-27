#PRUEBA_M.py
import time
import MOTOR_DRIVER as MD

while True:
    MD.move(int(input("PERCENT VEL: ")), int(input("PERCENT DIR")))
    time.sleep(int(input("SLEEP: ")))