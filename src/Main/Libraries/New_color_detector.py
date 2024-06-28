#This code is a library for the camera to take the color centroid and area of a specific frame given

import cv2
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray

camera = PiCamera()

# Función para detectar el color rojo en un cuadro
def detect_red(frame):
    mask = (frame[:, :, 2] > 100) & (frame[:, :, 1] < frame[:, :, 2]) & (frame[:, :, 0] < frame[:, :, 2])
    return get_color_centroid_and_area(frame, mask)

# Función para detectar el color verde en un cuadro
def detect_green(frame):
    mask = (frame[:, :, 1] > 100) & (frame[:, :, 0] < frame[:, :, 1]) & (frame[:, :, 2] < frame[:, :, 1])
    return get_color_centroid_and_area(frame, mask)

# Función para detectar el color magenta en un cuadro
def detect_magenta(frame):
    mask = (frame[:, :, 2] > 100) & (frame[:, :, 0] > 100) & (frame[:, :, 1] < frame[:, :, 2]) & (frame[:, :, 1] < frame[:, :, 0])
    return get_color_centroid_and_area(frame, mask)

# Función para obtener el centroide y el área de la máscara de color
def get_color_centroid_and_area(frame, mask):
    # Convertir la máscara booleana a uint8
    mask = mask.astype(np.uint8) * 255

    # Encontrar contornos en la máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Si no se encuentran contornos, devolver None y área 0
    if not contours:
        return None, 0

    # Encontrar el contorno más grande
    largest_contour = max(contours, key=cv2.contourArea)

    # Calcular el centro y el área del contorno más grande
    M = cv2.moments(largest_contour)
    if M["m00"] == 0:
        return None, 0
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    area = cv2.contourArea(largest_contour)
    return (cX, cY), area

# Configuración de la cámara
camera.resolution = (640, 480)
camera.framerate = 30
raw_capture = PiRGBArray(camera, size=(640, 480))

# Captura y procesamiento de imágenes continuo
for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    image = frame.array
    height, width = image.shape[:2]
    lower_half = image[height//2:, :]

    # Detectar el color rojo, verde y magenta en la parte inferior del cuadro
    red_centroid, red_area = detect_red(lower_half)
    green_centroid, green_area = detect_green(lower_half)
    magenta_centroid, magenta_area = detect_magenta(lower_half)

    # Mostrar resultados
    print(f"Red Area: {red_area}, Red Centroid: {red_centroid}")
    print(f"Green Area: {green_area}, Green Centroid: {green_centroid}")
    print(f"Magenta Area: {magenta_area}, Magenta Centroid: {magenta_centroid}")

    # Limpiar el búfer para la siguiente captura
    raw_capture.truncate(0)
