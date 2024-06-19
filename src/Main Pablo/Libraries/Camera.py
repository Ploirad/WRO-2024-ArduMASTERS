from picamera.array import PiRGBArray
from picamera import PiCamera
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

# Define resolution
resolucion = (640,480)

# Define camera
camera = PiCamera()
camera.resolution = resolucion
rawCapture = PiRGBArray(camera, size=resolucion)
time.sleep(0.3)

def testColor(frame, bajo, alto):
    frame2 = frame.copy()
    frameHSV = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(frameHSV, bajo, alto)
    cx, cy = obtenerCentroide(mask)
    frame2[mask == 255] = (0,255,0)
    cv2.circle(frame2, (cx,cy), 5,(0,0,255), -1)
    return frame2, mask, cx,cy

def obtenerCentroide(imgBin):
    cx = 0
    cy = 0
    cBlancas = cv2.findNonZero(imgBin)
    
    try:
        sumX, sumY = np.sum(cBlancas, axis=0).squeeze()
        nPuntos = len(cBlancas)
        cx = int(sumX / nPuntos)
        cy = int(sumY / nPuntos)
    except:
        pass
    
    return cx, cy

def BM(index):
    frame = camera.capture_continuous(rawCapture, format="bgr", use_video_port=True).array
        
    # Capture umbral segmented frame for all colors
    FR = testColor(frame,R_min,R_max)[1]
    FG = testColor(frame,G_min,G_max)[1]
    FP = testColor(frame,P_min,P_max)[1]
        
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

    return BM[index]