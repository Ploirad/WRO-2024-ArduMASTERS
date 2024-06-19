import Libraries.Motor as M
import Libraries.Ultrasonidos as HC
import time
import cv2
import numpy as np

def main():
    turns = turns
    # If total distance to the walls is less than 1'5m
    if HC.measure_distance(2) + HC.measure_distance(4) <=150: 
        # If to much to the right
        if HC.measure_distance(2) <= (HC.measure_distance(2) + HC.measure_distance(4))/2-10: 
            M.movement(1,180) # Turn left
        # If to much to the left
        elif HC.measure_distance(4) <= (HC.measure_distance(2) + HC.measure_distance(4))/2-10: 
            M.movement(1,0) # Turn right
        else:
            M.movement(1,90) # Continue forward

    else:
        # If there is more distance to the right than the left
        if HC.measure_distance(2) > HC.measure_distance(4): 
            prev_front = HC.measure_distance(1) # Save distance to front walls
            M.movement(1,0) # Turn to right until the front walls it's at the left
            while not HC.measure_distance(4) == range(prev_front-30,prev_front):  time.sleep(.25)
            M.movement(1,90) # Continue forward until abandoning the corner
            while HC.measure_distance(2) + HC.measure_distance(4) >= 150: time.sleep(.25)
            turns += 1

         # If there is more distance to the left than the right
        elif HC.measure_distance(2) < HC.measure_distance(4): 
            prev_front = HC.measure_distance(1) # Save distance to front walls
            M.movement(1,180) # Turn to right until the front walls it's at the right
            while not HC.measure_distance(4) <= prev_front:  time.sleep(.25)
            M.movement(1,90) # Continue forward until abandoning the corner
            while HC.measure_distance(2) + HC.measure_distance(4) >= 150: time.sleep(.25)
            turns += 1
    
    if turns < 12:
        main()

main()