from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import cv2
import numpy as np

def testColor(frame, bajo, alto, color):
    frame2 = frame.copy()
    frameHSV = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(frameHSV, bajo, alto)
    cx, cy, w, h = obtenerCentroide(mask)
    frame2[mask == 255] = color
    cv2.circle(frame2, (cx,cy), 5,(0,0,255), -1)
    return frame2, mask, cx,cy, w, h


def obtenerCentroide(imgBin):
    cx = 0
    cy = 0
    cBlancas = cv2.findNonZero(imgBin)
    x, y, w, h = cv2.boundingRect(cBlancas)
    
    try:
        sumX, sumY = np.sum(cBlancas, axis=0).squeeze()
        nPuntos = len(cBlancas)
        cx = int(sumX / nPuntos)
        cy = int(sumY / nPuntos)
    except:
        pass
    
    return cx, cy, w, h

resolucion = (640,480)

camera = PiCamera()
camera.resolution = resolucion
rawCapture = PiRGBArray(camera, size=resolucion)
time.sleep(0.3)
bajoR, altoR = np.array([174, 154, 136]),np.array([178, 209, 212])
bajoG, altoG = np.array([54, 155, 111]),np.array([60, 211, 135])
bajoM, altoM = np.array([142, 117, 49]),np.array([150, 230, 208])
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    f, mask1, cx1, cy1, w1, h1 = testColor(image, bajoR, altoR, (355, 83, 93))
    f, mask2, cx2, cy2, w2, h2= testColor(image, bajoG, altoG, (111, 79, 83))
    f, mask3, cx3, cy3, w3, h3 = testColor(image, bajoM, altoM, (300, 100, 100))
    print([cx1,cy1], [cx2, cy2], [cx3, cy3])
    print([w1, h1], [w2, h2], [w3, h3])
    cv2.imshow("frame: Rojo", mask1)
    cv2.imshow("frame: Verde", mask2)
    cv2.imshow("frame: Morado", mask3)
    rawCapture.truncate(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
