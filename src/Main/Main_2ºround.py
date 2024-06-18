import Libraries.Motor as M
import Libraries.Ultrasonidos as HC
import Libraries.Camera as cam
import Libraries.tsc34725 as tsc
import RPi.GPIO as GPIO
from picam import Picam
from picam.array import PiRGBArray
import time
import cv2
import numpy as np

GPIO.setmode(GPIO.BCM)

# Define range of HSV for RED
R_min = np.array([ ,  ,  ], np.uint8)
R_max = np.array([ ,  ,  ], np.uint8)
# Define range of HSV for GREEN
G_min = np.array([ ,  ,  ], np.uint8)
G_max = np.array([ ,  ,  ], np.uint8)
# Define range of HSV for PURPLE
P_min = np.array([ ,  ,  ], np.uint8)
P_max = np.array([ ,  ,  ], np.uint8)

# Define global variables
turns = 0
laps = 0

for frame in cam.capture_continuous(cam.rawCapture, format="bgr", use_video_port=True).array:
    
    # Capture umbral segmented frame for all colors
    FR = cam.testColor(frame,R_min,R_max)[1]
    FV = cam.testColor(frame,G_min,G_max)[1]
    FM = cam.testColor(frame,P_min,P_max)[1]
    
    # Define a bounding box in the segmented frame
    BR = cv2.boundingRect(FR)
    BV = cv2.boundingRect(FV)
    BM = cv2.boundingRect(FM)
    
    # Compare boxes and set the biggest as main
    if BR[2]*BR[3] > BV[2]*BV[3]:
        BM = BR
        side = "izq" # Si es rojo se rebasa por la izquierda
    else:
        BM = BV
        side = "der" # Si si es verde se rebasa por la derecha
    
    if BM[2]*BM[3] >= 300 :
        
        if side == "der":
            if BM[0] < 140:
                M.movement(1,90)
            else:
                M.movement(1,0)
        else:
            if BM[0] > 500:
                M.movement(1,90)
            else:
                M.movement(1,180)
    
    elif HC.measure_distance(2) + HC.measure_distance(4) <=100:
        
        if HC.measure_distance(2) <= 40: 
            M.movement(1,180)
    
        elif HC.measure_distance(4) <= 40: 
            M.movement(1,0)
        else:
            M.movement(1,90)
    
    # 2: distnace to the right  4: distance to the left
    elif HC.measure_distance(2) > HC.measure_distance(4): 
        prev_front = HC.measure_distance(1)
        M.movement(1,0)
        while not HC.measure_distance(4) <= prev_front:  time.sleep(.25)
        M.movement(1,90)
        while HC.measure_distance(2) + HC.measure_distance(4) >= 120: time.sleep(.25)
        turns += 1
    
    elif HC.measure_distance(2) < HC.measure_distance(4): 
        prev_front = HC.measure_distance(1)
        M.movement(1,180)
        while not HC.measure_distance(4) <= prev_front:  time.sleep(.25)
        M.movement(1,90)
        while HC.measure_distance(2) + HC.measure_distance(4) >= 120: time.sleep(.25)
        turns += 1