from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import cv2
import numpy as np

def testColor(frame, bajo, alto):
    frame2 = frame.copy()
    frameHSV = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(frameHSV, bajo, alto)
    return frame2, mask

resolucion = (640,480)

bajo, alto = [(),()]

camera = PiCamera()
camera.resolution = resolucion
rawCapture = PiRGBArray(camera, size=resolucion)
time.sleep(1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array

    f, mask = testColor(image, bajo, alto)
    cv2.imshow("frame", mask)

    F = testColor(frame,min,max)[1]
    B = cv2.boundingRect(F)

    print(B[2]*B[3])
    
    rawCapture.truncate(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()