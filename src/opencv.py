import picamera
import picamera.array
import cv2
import numpy as np

# Rangos de color para los colores que queremos detectar en formato HSV
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])

lower_green = np.array([40, 100, 100])
upper_green = np.array([80, 255, 255])

lower_blue = np.array([100, 100, 100])
upper_blue = np.array([140, 255, 255])

# Función para procesar cada fotograma y detectar los colores
def process_frame(frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Convertimos a espacio de color HSV
    red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)  # Máscara para el color rojo
    green_mask = cv2.inRange(hsv_frame, lower_green, upper_green)  # Máscara para el color verde
    blue_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)  # Máscara para el color azul
    
    # Encuentra los contornos de los objetos de cada color
    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    green_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Imprimir los valores RGB de los píxeles detectados
    for contour in red_contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            print(f"Color rojo detectado en RGB: {frame[cy, cx]}")

    for contour in green_contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            print(f"Color verde detectado en RGB: {frame[cy, cx]}")

    for contour in blue_contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            print(f"Color azul detectado en RGB: {frame[cy, cx]}")

# Inicializamos la cámara de la Raspberry Pi
with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)  # Establecemos la resolución de la cámara

    # Creamos un objeto para capturar fotogramas
    with picamera.array.PiRGBArray(camera) as stream:
        # Capturamos cada fotograma de la cámara
        for frame in camera.capture_continuous(stream, format='bgr', use_video_port=True):
            image = frame.array  # Obtenemos la imagen como un array numpy
            process_frame(image)  # Procesamos el fotograma para detectar colores
            
            # Limpiamos el stream para el siguiente fotograma
            stream.truncate(0)
