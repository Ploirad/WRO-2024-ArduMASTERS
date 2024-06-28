#This code is a library for the camera to take the color centroid and area of a specific frame given

import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

# Función para detectar el color rojo
def detect_red(image):
    # Crear una máscara para los píxeles rojos
    mask = (image[:,:,2] > 100) & (image[:,:,2] > image[:,:,1]) & (image[:,:,2] > image[:,:,0])
    result = image.copy()
    result[~mask] = 0
    
    # Encontrar contornos de la máscara
    contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Calcular el centroide y el área del contorno más grande (si existe)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        area = cv2.contourArea(largest_contour)
        return cx, cy, area
    else:
        return None

# Función para detectar el color verde
def detect_green(image):
    # Crear una máscara para los píxeles verdes
    mask = (image[:,:,1] > 100) & (image[:,:,1] > image[:,:,2]) & (image[:,:,1] > image[:,:,0])
    result = image.copy()
    result[~mask] = 0
    
    # Encontrar contornos de la máscara
    contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Calcular el centroide y el área del contorno más grande (si existe)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        area = cv2.contourArea(largest_contour)
        return cx, cy, area
    else:
        return None

# Función para detectar el color azul
def detect_blue(image):
    # Crear una máscara para los píxeles azules
    mask = (image[:,:,0] > 100) & (image[:,:,0] > image[:,:,1]) & (image[:,:,0] > image[:,:,2])
    result = image.copy()
    result[~mask] = 0
    
    # Encontrar contornos de la máscara
    contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Calcular el centroide y el área del contorno más grande (si existe)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        area = cv2.contourArea(largest_contour)
        return cx, cy, area
    else:
        return None

# Configuración de la cámara
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))

# Permitir que la cámara se caliente
time.sleep(0.1)

# Capturar imágenes continuamente
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    
    # Detectar colores y obtener centroide y área
    red_info = detect_red(image)
    green_info = detect_green(image)
    blue_info = detect_blue(image)

    # Imprimir resultados si se detectó el color
    if red_info:
        cr, _, ra = red_info
        print(f"RedCX: {cr}; RedArea: {ra}")
    
    if green_info:
        cg, _, ga = green_info
        print(f"GreenCX: {cg}; GreenArea: {ga}")
    
    if blue_info:
        cb, _, ba = blue_info
        print(f"BlueCX: {cb}; BlueArea: {ba}")

    # Limpiar el rawCapture para el siguiente frame
    rawCapture.truncate(0)

# Liberar recursos
camera.close()
