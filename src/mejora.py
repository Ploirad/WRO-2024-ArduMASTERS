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
    cx_r = None
    Ar = None
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
            Ar = w*h
            cx_r = cx

    centroids_green = None
    dimensions_green = None
    cx_v = None
    Av = None
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
            Av = w*h
            cx_v = cx

    centroids_magenta = None
    dimensions_magenta = None
    cx_m = None
    Am = None
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
            Am = w*h
            cx_m = cx

    return [mask_red, mask_green, mask_magenta], [cx_r, cx_v, cx_m], [dimensions_red, dimensions_green, dimensions_magenta], [Ar, Av, Am]


# Bucle principal
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Captura de imagen
    image = frame.array

    # Detección de colores y análisis de imagen
    masks, cx, dimensions, A = detect_colors(image)

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

    Am, Ar, Av = A[2], A[0], A[1]
    cx_v, cx_r, cx_m = cx[1], cx[0], cx[2]
    
    print(f"C: R:{cx[0]}, V:{cx[1]}, M:{cx[2]}")
    print(f"D: R:{Ar}, V:{Av}, M:{Am}")
    # Limpiar el búfer de captura para la siguiente imagen
    rawCapture.truncate(0)
    if cx_v != None:
        if cx_v < 170:
            print("V a la IZQ")
        elif cx_v > 170 and cx_v < 470:
            print("V al CENT")
        else:
            print("V a la DER")
    if cx_r != None:
        if cx_r < 170:
            print("R a la IZQ")
        elif cx_r > 170 and cx_v < 470:
            print("R al CENT")
        else:
            print("R a la DER")
    if cx_m != None:
        if cx_m < 170:
            print("M a la IZQ")
        elif cx_m > 170 and cx_v < 470:
            print("M al CENT")
        else:
            print("M a la DER")
    # Esperar una tecla para salir (salida si se presiona 'q')
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# Limpiar y cerrar las ventanas
cv2.destroyAllWindows()

# Limpiar configuraciones de GPIO
GPIO.cleanup()
