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
def detect_colors(frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Nuevos rangos de color
    lower_red = np.array([174, 175, 120])
    upper_red = np.array([176, 212, 170])
    lower_green = np.array([57, 104, 100])
    upper_green = np.array([65, 156, 150])
    lower_magenta = np.array([164, 148, 120])
    upper_magenta = np.array([167, 185, 170])

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
    centroids_red = None
    dimensions_red = None
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours_red:
        contour = max(contours_red, key=cv2.contourArea)
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            centroids_red = [(cx, cy)]
            x, y, w, h = cv2.boundingRect(contour)
            dimensions_red = [(w, h)]

    centroids_green = None
    dimensions_green = None
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours_green:
        contour = max(contours_green, key=cv2.contourArea)
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            centroids_green = [(cx, cy)]
            x, y, w, h = cv2.boundingRect(contour)
            dimensions_green = [(w, h)]

    centroids_magenta = None
    dimensions_magenta = None
    contours_magenta, _ = cv2.findContours(mask_magenta, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours_magenta:
        contour = max(contours_magenta, key=cv2.contourArea)
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            centroids_magenta = [(cx, cy)]
            x, y, w, h = cv2.boundingRect(contour)
            dimensions_magenta = [(w, h)]

    return [mask_red, mask_green, mask_magenta], [centroids_red, centroids_green, centroids_magenta], [dimensions_red, dimensions_green, dimensions_magenta]


# Bucle principal
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Captura de imagen
    image = frame.array

    # Detección de colores y análisis de imagen
    masks, centroids, dimensions = detect_colors(image)

    # Mostrar las máscaras de color y la imagen original en ventanas separadas con tamaños personalizados
    cv2.namedWindow("Original", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Original", 400, 300)
    cv2.imshow("Original", image)
    
    cv2.namedWindow("Red Mask", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Red Mask", 400, 300)
    cv2.imshow("Red Mask", masks[0])
    
    cv2.namedWindow("Green Mask", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Green Mask", 400, 300)
    cv2.imshow("Green Mask", masks[1])
    
    cv2.namedWindow("Magenta Mask", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Magenta Mask", 400, 300)
    cv2.imshow("Magenta Mask", masks[2])

    Am = dimensions[2]
    Am = Am[0] * Am[1]

    Ar = dimensions[0]
    Ar = Ar[0] * Ar[1]

    Av = dimensions[0]
    Av = Av[0] * Av[0]
    
    print(f"C: R:{centroids[0]}, V:{centroids[1]}, M:{centroids[2]}")
    print(f"D: R:{Ar}, V:{Av}, M:{Am}")
    # Limpiar el búfer de captura para la siguiente imagen
    rawCapture.truncate(0)

    # Esperar una tecla para salir (salida si se presiona 'q')
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# Limpiar y cerrar las ventanas
cv2.destroyAllWindows()

# Limpiar configuraciones de GPIO
GPIO.cleanup()
