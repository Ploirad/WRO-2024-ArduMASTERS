from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import cv2
import numpy as np

resolucion = (640,480)

camera = PiCamera()
camera.resolution = resolucion
rawCapture = PiRGBArray(camera, size=resolucion)

# allow the camera to warmup
time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    r = cv2.selectROI("frame", image, fromCenter=False, showCrosshair=True)
    r = tuple(map(int,r))

    frameHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    imagenNueva = frameHSV[r[1]:r[1]+r[3],r[0]:r[0]+r[2]]
    H,S,V = imagenNueva[:,:,0], imagenNueva[:,:,1], imagenNueva[:,:,2]
    hMin, hMax = np.min(H), np.max(H)
    sMin, sMax = np.min(S), np.max(S)
    vMin, vMax = np.min(V), np.max(V)
    
    bajo = np.array([hMin, sMin, vMin], np.uint8)
    alto = np.array([hMax, sMax, vMax], np.uint8)
    
    print(f"Min: {bajo} Max: {alto}")
    
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    
    # break the loop if you only want to process one frame
    break