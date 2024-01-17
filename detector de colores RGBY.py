# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 01:50:58 2024

@author: adriy
"""

# Empezamos incluyendo las librerías a emplear
import cv2
import numpy as np

# Definimos una función para detectar colores y graficar contornos
def draw(mask, color):
    contornos,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for c in contornos:
        area = cv2.contourArea(c)
        
        # Si el área de interés es mayor a
        if area > 5000:    
            M = cv2.moments(c)
            if (M["m00"] == 0):
                M["m00"] = 1
                
            x = int(M["m10"]/M["m00"])
            y = int(M["m01"]/M["m00"])
            
            #--- Dibujamos los contornos seleccionados ---
            newContorno = cv2.convexHull(c)
             
            #--- Dibujamos un punto de r=7 y color verde ---
            cv2.circle(frame, (x, y), 7, (255, 255, 255), -1)
                                 
            # Puntos, ubicación, fuente, grosor, color, tamaño
            cv2.putText(frame, '{}, {}'.format(x, y), (x+10, y), cv2.FONT_ITALIC, 0.75, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.drawContours(frame, [newContorno], 0, color, 3)

# Definimos el puerto de la cámara a emplear         
cap = cv2.VideoCapture(0)

#AMARILLO
amarillo_osc = np.array([25, 70, 920], np.uint8)
amarillo_cla = np.array([30, 255, 255], np.uint8)

#rojo
rojo_osc = np.array([0, 50, 120], np.uint8)
rojo_cla = np.array([10, 255, 255], np.uint8)

#verde
verde_osc = np.array([40, 70, 80], np.uint8)
verde_cla = np.array([70, 255, 255], np.uint8)

#azul
azul_osc = np.array([90, 68, 0], np.uint8)
azul_cla = np.array([121, 255, 255], np.uint8)


# Mientras está activada la captura de video
while True:
    # Obtenemos un valor booleano e imagen
    
    ret, frame = cap.read()

    # Si hay imagen capturada
    if ret == True:

        # Pasamos de BGR a HSV
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        amarillo = cv2.inRange(frameHSV, amarillo_osc, amarillo_cla)
        rojo = cv2.inRange(frameHSV, rojo_osc, rojo_cla)
        verde = cv2.inRange(frameHSV, verde_osc, verde_cla)
        azul = cv2.inRange(frameHSV, azul_osc, azul_cla)
        
        draw(azul, (255, 0, 0))
        draw(amarillo, (0, 255, 255))
        draw(rojo, (0, 0, 255))
        draw(verde, (255, 255, 0))
        
        # Mostramos la ventana de captura
        cv2.imshow("pantalla", frame)
        
        # Detenemos la visualización con la tecla 's'
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break

# Detenemos la captura de video
cap.release()
# Cerramos todas las ventanas
cv2.destroyAllWindows()