import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

# Variables globales para almacenar el punto seleccionado y la imagen
clicked_point = None
selected_hsv = None

# Callback del mouse
def mouse_callback(event, x, y, flags, param):
    global clicked_point
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_point = (x, y)
        print(f"Color seleccionado en (x={x}, y={y})")

# Función para convertir el color BGR a HSV
def bgr_to_hsv(bgr_color):
    bgr_color = np.uint8([[bgr_color]])
    hsv_color = cv2.cvtColor(bgr_color, cv2.COLOR_BGR2HSV)
    return hsv_color[0][0]

# Inicializar la cámara
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# Permitir que la cámara se caliente
time.sleep(0.1)

cv2.namedWindow('Image')
cv2.setMouseCallback('Image', mouse_callback)

try:
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        
        if clicked_point:
            bgr_color = image[clicked_point[1], clicked_point[0]].tolist()
            selected_hsv = bgr_to_hsv(bgr_color)
            print(f"Color BGR seleccionado: {bgr_color}")
            print(f"Color HSV correspondiente: {selected_hsv}")

            # Rango de colores HSV
            lower_bound = np.array([selected_hsv[0] - 10, 100, 100])
            upper_bound = np.array([selected_hsv[0] + 10, 255, 255])

            # Convertir la imagen a HSV
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Crear una máscara con el rango de color seleccionado
            mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
            
            # Mostrar la máscara
            cv2.imshow('Mask', mask)

        cv2.imshow('Image', image)

        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)

        if key == ord('q'):
            break

except KeyboardInterrupt:
    pass

# Limpiar y cerrar las ventanas
cv2.destroyAllWindows()
