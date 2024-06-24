#This code is a library for the camera to take the color centroid and area of a specific frame given

#Import the necessary libraries
import cv2
import numpy as np
import time

#This function is used to take the green centroid respect to the X edge and the green area all about the frame gived and they are integer variables
def detect_green(frame):
    t1g = time.time()
    V_bajo = np.array([31, 147, 66])
    V_alto = np.array([35, 255, 255])
    print(f"Camara: detect_green(): {time.time()-t1g}")
    return detect_color(frame, V_bajo, V_alto)

#This function is used to take the red centroid respect to the X edge and the red area all about the frame gived
def detect_red(frame):
    t1r = time.time()
    R_bajo = np.array([175, 126, 68])
    R_alto = np.array([176, 212, 255])
    print(f"Camara: detect_red(): {time.time()-t1r}")
    return detect_color(frame, R_bajo, R_alto)

#This function is used to take the magenta centroid respect to the X edge and the magenta area all about the frame gived
def detect_magenta(frame):
    t1m = time.time()
    M_bajo = np.array([138, 87, 25])
    M_alto = np.array([167, 185, 255])
    print(f"Camara: detect_magenta(): {time.time()-t1m}")
    return detect_color(frame, M_bajo, M_alto)

#This function is used to take the centroid and the area of the color gived (color_low, color_high) in the respective frame
def detect_color(frame, color_low, color_high):
    t1 = time.time()
    # Obtener las dimensiones del frame
    height, width, _ = frame.shape

    # Cubrir la mitad superior del frame con negro
    frame[:height//2, :] = 0

    # Convertir el frame a espacio de color HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Crear una máscara para el rango de color especificado
    mask = cv2.inRange(hsv, color_low, color_high)

    # Encontrar contornos en la máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Si no se encuentran contornos, devolver None
    if not contours:
        return None, 0

    # Encontrar el contorno más grande
    largest_contour = max(contours, key=cv2.contourArea)

    # Calcular el centro y el área del contorno más grande
    M = cv2.moments(largest_contour)
    if M["m00"] == 0:
        return None, 0
    cX = int(M["m10"] / M["m00"])
    area = cv2.contourArea(largest_contour)
    print(f"Camara: detect_color(): {time.time()-t1}")
    
    return cX, area