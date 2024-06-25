#PRUEBA_M.py
import time
from Libraries import Motor as M

while True:
    M.movement(1, 0, False)
    time.sleep(1)