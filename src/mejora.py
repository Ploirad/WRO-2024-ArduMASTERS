import RPi.GPIO as GPIO
import time
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2
import numpy as np

# Definición de pines GPIO
TRIG_PIN_DELANTE = 23
ECHO_PIN_DELANTE = 24
TRIG_PIN_ATRAS = 17
ECHO_PIN_ATRAS = 27
TRIG_PIN_IZQUIERDA = 22
ECHO_PIN_IZQUIERDA = 10
TRIG_PIN_DERECHA = 5
ECHO_PIN_DERECHA = 6
servo_pin_direccion = 2
servo_pin_traccion = 3
button_pin = 9
IRsensor = 8

# Configuración de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN_DELANTE, GPIO.OUT)
GPIO.setup(ECHO_PIN_DELANTE, GPIO.IN)
GPIO.setup(TRIG_PIN_ATRAS, GPIO.OUT)
GPIO.setup(ECHO_PIN_ATRAS, GPIO.IN)
GPIO.setup(TRIG_PIN_IZQUIERDA, GPIO.OUT)
GPIO.setup(ECHO_PIN_IZQUIERDA, GPIO.IN)
GPIO.setup(TRIG_PIN_DERECHA, GPIO.OUT)
GPIO.setup(ECHO_PIN_DERECHA, GPIO.IN)
GPIO.setup(servo_pin_direccion, GPIO.OUT)
GPIO.setup(servo_pin_traccion, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Inicialización de la cámara
camera = PiCamera()
camera.resolution = (640, 480)
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)

# Funciones de detección de colores y análisis de imágenes
def detect_colors(frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Rangos de color para detección
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    lower_green = np.array([40, 100, 100])
    upper_green = np.array([80, 255, 255])
    lower_magenta = np.array([125, 100, 100])
    upper_magenta = np.array([150, 255, 255])

    # Detección de colores
    mask_red = cv2.inRange(hsv_frame, lower_red, upper_red)
    mask_green = cv2.inRange(hsv_frame, lower_green, upper_green)
    mask_magenta = cv2.inRange(hsv_frame, lower_magenta, upper_magenta)

    # Aplicar operaciones morfológicas para mejorar la detección
    kernel = np.ones((5, 5), np.uint8)
    mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)
    mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel)
    mask_magenta = cv2.morphologyEx(mask_magenta, cv2.MORPH_OPEN, kernel)

    # Encontrar contornos y calcular centroides y dimensiones
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_magenta, _ = cv2.findContours(mask_magenta, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    centroids_red = []
    centroids_green = []
    centroids_magenta = []

    dimensions_red = []
    dimensions_green = []
    dimensions_magenta = []

    for contour in contours_red:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            centroids_red.append((cx, cy))
            x, y, w, h = cv2.boundingRect(contour)
            dimensions_red.append((w, h))

    for contour in contours_green:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            centroids_green.append((cx, cy))
            x, y, w, h = cv2.boundingRect(contour)
            dimensions_green.append((w, h))

    for contour in contours_magenta:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            centroids_magenta.append((cx, cy))
            x, y, w, h = cv2.boundingRect(contour)
            dimensions_magenta.append((w, h))

    return [mask_red, mask_green, mask_magenta], [centroids_red, centroids_green, centroids_magenta], [dimensions_red, dimensions_green, dimensions_magenta]

# Bucle principal
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array

    # Detectar colores
    masks, centroids, dimensions = detect_colors(image)

    # Mostrar imágenes y máscaras
    cv2.imshow("Frame", image)
    cv2.imshow("Red Mask", masks[0])
    cv2.imshow("Green Mask", masks[1])
    cv2.imshow("Magenta Mask", masks[2])

    # Mostrar información de centroides y dimensiones
    for color, centroid_list, dimension_list in zip(["Red", "Green", "Magenta"], centroids, dimensions):
        for centroid, dimension in zip(centroid_list, dimension_list):
            print(f"{color} Centroid: {centroid}, Dimension: {dimension}")

    # Limpiar el buffer de la cámara para la siguiente captura
    rawCapture.truncate(0)

    # Espera por la tecla 'q' para salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Limpieza de GPIO y cierre de ventanas
GPIO.cleanup()
cv2.destroyAllWindows()
