from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2
import numpy as np
import time
resolucion = (640,480)

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
camera.capture(rawCapture, format="bgr")
imagen = rawCapture.array

# Definir los rangos de color bajo y alto en formato HSV
bajo = np.array([0, 100, 100])
alto = np.array([20, 255, 255])

# Probar el color en la imagen capturada
imagen_procesada = testColor(imagen, bajo, alto)

# Mostrar la imagen original y la imagen procesada
cv2.imshow("Original", imagen)
cv2.imshow("Procesada", imagen_procesada)
cv2.waitKey(0)
cv2.destroyAllWindows()
