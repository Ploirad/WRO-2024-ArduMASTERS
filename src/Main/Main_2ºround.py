import Libraries.Motor as M
import Libraries.Ultrasonidos as HC
import Libraries.Camera as C
import Libraries.tsc34725 as tsc
import time
import cv2
import numpy as np

# Define range of HSV for RED
R_min = np.array([0 ,0  ,0 ], np.uint8)
R_max = np.array([0 ,0  ,0 ], np.uint8)
# Define range of HSV for GREEN
G_min = np.array([0 ,0  ,0 ], np.uint8)
G_max = np.array([0 ,0  ,0 ], np.uint8)
# Define range of HSV for PURPLE
P_min = np.array([0 ,0  ,0 ], np.uint8)
P_max = np.array([0 ,0  ,0 ], np.uint8)

# Define global variables
turns = 0
laps = 0
prev_distance = 0
var_distance = 0
fps = 5
target = ""

def main():

    for frame in C.capture_continuous(C.rawCapture, format="bgr", use_video_port=True).array:
            
        # Capture umbral segmented frame for all colors
        FR = C.testColor(frame,R_min,R_max)[1]
        FG = C.testColor(frame,G_min,G_max)[1]
        FP = C.testColor(frame,P_min,P_max)[1]
            
        # Define a bounding box in the segmented frame
        BR = cv2.boundingRect(FR)
        BG = cv2.boundingRect(FG)
        BP = cv2.boundingRect(FP)

        # Compare boxes and set the biggest as main and add color info, index 4
        if BR[2]*BR[3] > BG[2]*BG[3]:
            BM = BR + "red"
        else:
            BM = BG + "green"
        # Move xy coords to centroid coords
        BM[0] = BM[0] + BM[2]/2 # x coords 
        BM[1] = BM[1] + BM[3]/2 # y coords

        # Add area info, index 5
        BM = BM + BM[2]*BM[3]    

        FD = HC.measure_distance("front")
        RD = HC.measure_distance("right")
        BD = HC.measure_distance("back")
        LD = HC.measure_distance("left")
        TD = RD + LD
        
        if BM[2]*BM[3] >= 300 : # If detected rectangle is big enought
            if target == "":
                target = BM[4]            
            
            var_distance = HC.measure_distance(target) - prev_distance
            prev_distance = HC.measure_distance(target)

            if target == "green":
                
                if var_distance >= 30:

                    if BM(0) < 100: # If it's on the left side
                        M.movement(1,90) # Forward
                    else:
                        M.movement(1,0) # Turn left
                
                else:
                    last_color = target
                    taget = ""
            
            elif target == "red":
            
                if var_distance >= 30:
                    
                    if BM(0) > 540: # If it's on the left side
                        M.movement(1,90) # Forward
                    else:
                            M.movement(1,180) # Turn right
                
                else:
                    last_color = target
                    taget = ""
                    
        else:
            # If total distance to the walls is less than 1'5m
            if TD <=150: 
                # If to much to the right
                if RD <= TD/2-10: 
                    M.movement(1,180) # Turn left
                # If to much to the left
                elif LD <= TD/2-10: 
                    M.movement(1,0) # Turn right
                else:
                    M.movement(1,90) # Continue forward
                    
            else:
                # If there is more distance to the right than the left
                if RD > LD: 
                    prev_front = FD # Save distance to front walls
                    M.movement(1,0) # Turn to right until the front walls it's at the left
                    while not LD == range(prev_front-30,prev_front):  time.sleep(.25)
                    M.movement(1,90) # Continue forward until abandoning the corner
                    while TD >= 150: time.sleep(.25)
                    turns += 1
                    
                # If there is more distance to the left than the right
                elif RD < LD: 
                    prev_front = FD # Save distance to front walls
                    M.movement(1,180) # Turn to right until the front walls it's at the right
                    while not LD <= prev_front:  time.sleep(.25)
                    M.movement(1,90) # Continue forward until abandoning the corner
                    while TD >= 150: time.sleep(.25)
                    turns += 1
