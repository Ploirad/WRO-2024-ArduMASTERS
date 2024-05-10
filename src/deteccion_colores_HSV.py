from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import cv2
import numpy as np

def testColor(frame, bajo, alto):
    frame2 = frame.copy()
    frameHSV = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(frameHSV, bajo, alto)
    cx, cy = obtenerCentroide(mask)
    frame2[mask == 255] = (0,0,100)
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

resolucion = (640,480)

camera = PiCamera()
camera.resolution = resolucion
rawCapture = PiRGBArray(camera, size=resolucion)
time.sleep(0.3)
bajoR, altoR = np.array([355, 169, 55]),np.array([0, 198, 51])
bajoG, altoG = np.array([111, 134, 51]),np.array([120, 198, 51])
bajoM, altoM = np.array([300, 198, 28]),np.array([300, 198, 51])
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    f, mask1, cx, cy = testColor(image, bajoR, altoR)
    f, mask2, cx, cy = testColor(image, bajoG, altoG)
    f, mask3, cx, cy = testColor(image, bajoM, altoM)
    mask = cv2.bitwise_or(mask1, mask2, mask3)
    print(cx,cy)
    cv2.imshow("frame", f)
    cv2.imshow("frame2", mask)
    rawCapture.truncate(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break