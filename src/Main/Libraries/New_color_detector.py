#This code is a library for the camera to take the color centroid and area of a specific frame given

#Import the necessary libraries
import cv2
import numpy as np
import time
from picamera import PiCamera
from picamera.array import PiRGBArray

camera = PiCamera()

#This function is used to take the green centroid respect to the X edge and the green area all about the frame gived and they are integer variables
def detect_green(frame):
    #t1g = time.time()
    V_bajo = np.array([31, 147, 66])
    V_alto = np.array([35, 255, 255])
    #print(f"Camara: detect_green(): {time.time()-t1g}")
    return detect_color(frame, V_bajo, V_alto)

#This function is used to take the red centroid respect to the X edge and the red area all about the frame gived
def detect_red(frame):
    #t1r = time.time()
    R_bajo = np.array([175, 126, 68])
    R_alto = np.array([176, 212, 255])
    #print(f"Camara: detect_red(): {time.time()-t1r}")
    return detect_color(frame, R_bajo, R_alto)

#This function is used to take the magenta centroid respect to the X edge and the magenta area all about the frame gived
def detect_magenta(frame):
    #t1m = time.time()
    M_bajo = np.array([138, 87, 25])
    M_alto = np.array([167, 185, 255])
    #print(f"Camara: detect_magenta(): {time.time()-t1m}")
    cm, am = detect_color(frame, M_bajo, M_alto)
    cr, ar = detect_red(frame, np.array([175, 126, 68]), np.array([176, 212, 255]))
    if ar > am:
        return None, 0
    else:
        return cm, am
#This function is used to take the centroid and the area of the color gived (color_low, color_high) in the respective frame
def detect_color(frame, color_low, color_high):
    #t1 = time.time()
    # Convert the frame to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask for the specified color range
    mask = cv2.inRange(hsv, color_low, color_high)

    # Find contours in the mask
    _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # If no contours are found, return None
    if not contours:
        return None, 0

    # Find the largest contour
    largest_contour = max(contours, key=cv2.contourArea)

    # Compute the center and area of the largest contour
    M = cv2.moments(largest_contour)
    if M["m00"] == 0:
        return None, 0
    cX = int(M["m10"] / M["m00"])
    area = cv2.contourArea(largest_contour)
    #print(f"Camara: detect_color(): {time.time()-t1}")
    return cX, area



def detect_dominant_color(frame):
    # Convertir el cuadro a espacio de color HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Definir los límites bajos y altos para la detección de colores
    lower_bound = np.array([0, 50, 50])  # Bajos valores de H, S, V
    upper_bound = np.array([179, 255, 255])  # Altos valores de H, S, V

    # Crear una máscara para los colores dentro del rango especificado
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Encontrar contornos en la máscara
    _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Inicializar variables para el color dominante y el área máxima
    dominant_color = None
    max_area = 0

    # Iterar sobre todos los contornos encontrados
    for contour in contours:
        # Calcular el área del contorno actual
        area = cv2.contourArea(contour)

        # Si el área actual es mayor que el área máxima encontrada hasta ahora
        if area > max_area:
            max_area = area
            # Calcular el centroide del contorno para obtener el color dominante
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                # Convertir el color dominante a RGB
                dominant_color = cv2.cvtColor(np.uint8([[hsv[cY, cX]]]), cv2.COLOR_HSV2RGB)[0][0]

    return dominant_color

#EXAMPLE
green_centroid = None
red_centroid = None
magenta_centroid = None
green_area = 0
red_area = 0
magenta_area = 0
camera.framerate = 30 #65
camera.resolution = (640, 480)
raw_capture = PiRGBArray(camera, size=(640, 480))

raw_capture.truncate(0)
for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    image = frame.array
    height, width = image.shape[:2]
    lower_half = image[height//2:, :]
    green_centroid, green_area = detect_green(lower_half)
    red_centroid, red_area = detect_red(lower_half)
    magenta_centroid, magenta_area = detect_magenta(lower_half)
    dom_col = detect_dominant_color(lower_half)
    print(f"Green Area: {green_area}; Red Area: {red_area}; Magenta Area: {magenta_area}")
    print(f"Green Centroid: {green_centroid}; Red Centroid: {red_centroid}; Magenta Centroid: {magenta_centroid}")
    print(f"Dominante color: {dom_col}")
    print("")
    raw_capture.truncate(0)  # Limpiar el búfer para la siguiente captura