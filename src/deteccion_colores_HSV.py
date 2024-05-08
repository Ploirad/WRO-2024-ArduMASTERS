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
    frame2[mask == 255] = (255,255,255)
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
bajo, alto = [345, 74, 83],[365, 94, 100]

cuenta = 0
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    f, mask, cx, cy = testColor(image, bajo, alto)
    print(cx,cy)
    cv2.imshow("frame", f)
    cv2.imshow("frame2", mask)
    rawCapture.truncate(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break