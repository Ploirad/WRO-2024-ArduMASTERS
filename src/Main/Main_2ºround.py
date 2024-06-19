import Libraries.Motor as M
import Libraries.Ultrasonidos as HC
import Libraries.Camera as C
import Libraries.tsc34725 as tsc
import time
import cv2
import numpy as np

# Define global variables
turns = 0
laps = 0
prev_distance = 0
var_distance = 0
fps = 5

def main():
    time.sleep(1/fps)
    
    if C.BM(5) >= 300 : # If detected rectangle is big enought
        target = C.BM(4)
        var_distance = HC.measure_distance(target) - prev_distance
        prev_distance = HC.measure_distance(target)

        if target == "green":
            
            while var_distance >= 30:
                time.sleep(0.1)
                var_distance = HC.measure_distance(target) - prev_distance
                prev_distance = HC.measure_distance(target)
                if C.BM(0) < 100: # If it's on the left side
                    M.movement(1,90) # Forward
                else:
                    M.movement(1,0) # Turn left
            
            else:
                last_color = target
        
        elif target == "red":
           
            while var_distance >= 30:
                time.sleep(1/fps)
                var_distance = HC.measure_distance(target) - prev_distance
                prev_distance = HC.measure_distance(target)
                if C.BM(0) > 540: # If it's on the left side
                    M.movement(1,90) # Forward
                else:
                        M.movement(1,180) # Turn right
            
            else:
                last_color = target
    
    else:
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
    main()