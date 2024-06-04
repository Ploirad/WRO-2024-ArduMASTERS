import Libraries.Motor as M
import Libraries.Ultrasonidos as HC
import Libraries.Camara
import RPi.GPIO as GPIO
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import cv2
import numpy as np

GPIO.setmode(GPIO.BCM)

#Definir rangos de color ROJO
R_bajo = np.array([175, 126, 68], np.uint8)
R_alto = np.array([176, 212, 255], np.uint8)
#Definir rangos de color VERDE
V_bajo = np.array([62, 147, 49], np.uint8)
V_alto = np.array([65, 156, 255], np.uint8)
#Definir rangos de color MORADO
M_bajo = np.array([138, 87, 25], np.uint8)
M_alto = np.array([167, 185, 255], np.uint8)

#Dfinir camara y resolucion
resolucion = (640,480)

camera = PiCamera()
camera.resolution = resolucion
rawCapture = PiRGBArray(camera, size=resolucion)
time.sleep(0.5)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True).array:
    
    #Capturar frame segmentado por umbral de todos los colores
    FR = Camara.testColor(frame, R_bajo, R_alto)[1]
    FV = Camara.testColor(frame, V_bajo, V_alto)[1]
    FM = Camara.testColor(frame, M_bajo, M_alto)[1]
    
    #Definir una bounding box al frame segmentado
    BR = cv2.boundingRect(FR)
    BV = cv2.boundingRect(FV)
    BM = cv2.boundingRect(FM)
    
    #Comparar restangulos y definir el mas grande como pincipal
    if BR[2]*BR[3] > BV[2]*BV[3]:
        BP = BR
        side = "izq" #Si es rojo se rebasa por la izquierda
    else:
        BP = BV
        side = "der" #Si si es verde se rebasa por la derecha

    if side == "der":
        cx = BP[0] + 40
        if cx < 210:
            M.movimiento(1, 0, 0)
        else:
            M.movimiento(1, -1, 0)
    else:
        cx = BP[0] - 40
        if cx > 420:
            M.movimiento(1, 0, 0)
        else:
            M.movimiento(1, 1, 0)
