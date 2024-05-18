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
SERVO_PIN_DIRECCION = 2
SERVO_PIN_TRACCION = 3
BUTTON_PIN = 9

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
GPIO.setup(SERVO_PIN_DIRECCION, GPIO.OUT)
GPIO.setup(SERVO_PIN_TRACCION, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Configuración de PWM para los servos
pwm_d = GPIO.PWM(SERVO_PIN_DIRECCION, 50)  # Frecuencia de PWM: 50Hz (estándar para servos)
pwm_t = GPIO.PWM(SERVO_PIN_TRACCION, 50)  # Frecuencia de PWM: 50Hz (estándar para servos)

# Variables globales
tiempo_de_giro_linea = 1
numberlinea = 0
vueltas = 0
empezado = 0
distancia_delante = 0
ant_d_d = 0
vueltas_e = 0
distancia_atras = 0
distancia_izquierda = 0
distancia_derecha = 0
DISTANCIA_DE_ACCION = {"MENOR QUE": 15, "MAYOR QUE": 14}
T_AVANCE = 12.5
T_ATRAS = 2.5
G_DER = 4.5
G_IZQ = 10.5
G_CENT = 5.9
valor_d = G_CENT
valor_t = T_AVANCE
pulse_end = 0
v = 0
girando = 0
x = 4
numero_de_giros_para_acabar = x * 3

# Configuración de la cámara
camera = PiCamera()
camera.resolution = (640, 480)
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)

def get_distance(trig_pin, echo_pin):
    GPIO.output(trig_pin, True)
    time.sleep(0.00001)
    GPIO.output(trig_pin, False)
    pulse_end = 0
    pulse_start = 0
    while GPIO.input(echo_pin) == 0:
        pulse_start = time.time()
    while GPIO.input(echo_pin) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

def update_distances():
    global distancia_delante, distancia_atras, distancia_izquierda, distancia_derecha, ant_d_d
    ant_d_d = distancia_delante
    distancia_delante = get_distance(TRIG_PIN_DELANTE, ECHO_PIN_DELANTE)
    distancia_atras = get_distance(TRIG_PIN_ATRAS, ECHO_PIN_ATRAS)
    distancia_izquierda = get_distance(TRIG_PIN_IZQUIERDA, ECHO_PIN_IZQUIERDA)
    distancia_derecha = get_distance(TRIG_PIN_DERECHA, ECHO_PIN_DERECHA)

def giro_linea(valor_t, valor_d):
    print("Girando...")
    pwm_t.start(valor_t)
    pwm_d.start(valor_d)
    time.sleep(tiempo_de_giro_linea)
    pwm_d.start(G_CENT)

def giro_tras(valor_t, valor_d):
    valor_t = T_ATRAS
    valor_d = G_DER if valor_d == G_IZQ else G_IZQ
    pwm_t.start(valor_t)
    pwm_d.start(valor_d)
    time.sleep(2)
    pwm_t.start(T_AVANCE)
    pwm_d.start(valor_d)
    time.sleep(2)
    pwm_d.start(G_CENT)

def detect_colors(frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Rango de colores
    lower_red = np.array([174, 175, 100])
    upper_red = np.array([176, 212, 180])
    lower_green = np.array([57, 104, 100])
    upper_green = np.array([65, 156, 150])
    lower_magenta = np.array([164, 148, 120])
    upper_magenta = np.array([167, 185, 170])

    # Crear máscaras para cada color
    mask_red = cv2.inRange(hsv_frame, lower_red, upper_red)
    mask_green = cv2.inRange(hsv_frame, lower_green, upper_green)
    mask_magenta = cv2.inRange(hsv_frame, lower_magenta, upper_magenta)

    # Operaciones morfológicas
    kernel = np.ones((5, 5), np.uint8)
    mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)
    mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel)
    mask_magenta = cv2.morphologyEx(mask_magenta, cv2.MORPH_OPEN, kernel)

    def get_contour_data(mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                x, y, w, h = cv2.boundingRect(contour)
                area = w * h
                return (cx, cy), (w, h), area
        return None, None, None

    centroids_red, dimensions_red, Ar = get_contour_data(mask_red)
    centroids_green, dimensions_green, Av = get_contour_data(mask_green)
    centroids_magenta, dimensions_magenta, Am = get_contour_data(mask_magenta)

    return [mask_red, mask_green, mask_magenta], [centroids_red, centroids_green, centroids_magenta], [dimensions_red, dimensions_green, dimensions_magenta], [Ar, Av, Am]

try:
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array

        masks, centroids, dimensions, areas = detect_colors(image)

        cv2.imshow("Original", image)
        cv2.imshow("Red Mask", masks[0])
        cv2.imshow("Green Mask", masks[1])
        cv2.imshow("Magenta Mask", masks[2])

        button_state = GPIO.input(BUTTON_PIN)
        pwm_d.start(valor_d)

        if button_state == GPIO.HIGH:
            print("Botón presionado")
            v = 1

        if v == 1:
            pwm_t.start(valor_t)
            update_distances()

            if all(distance < DISTANCIA_DE_ACCION["MENOR QUE"] for distance in [distancia_delante, distancia_izquierda, distancia_derecha]):
                valor_t = T_ATRAS
                valor_d = G_CENT
            else:
                if not girando:
                    if distancia_delante < DISTANCIA_DE_ACCION["MENOR QUE"]:
                        if distancia_derecha > DISTANCIA_DE_ACCION["MAYOR QUE"] and distancia_derecha > distancia_izquierda:
                            valor_t = T_AVANCE
                            valor_d = G_DER
                            girando = 1
                            vueltas += 1
                            giro_linea(valor_t, valor_d)
                        elif distancia_izquierda > DISTANCIA_DE_ACCION["MAYOR QUE"] and distancia_izquierda > distancia_derecha:
                            valor_t = T_AVANCE
                            valor_d = G_IZQ
                            girando = 1
                            vueltas += 1
                            giro_linea(valor_t, valor_d)
                    elif distancia_delante > DISTANCIA_DE_ACCION["MAYOR QUE"]:
                        valor_t = T_AVANCE
                        valor_d = G_CENT
                        girando = 0

                if distancia_izquierda < 6:
                    valor_t = T_AVANCE
                    valor_d = G_DER
                    giro_linea(valor_t, valor_d)

                if distancia_derecha < 6:
                    valor_t = T_AVANCE
                    valor_d = G_IZQ
                    giro_linea(valor_t, valor_d)

                if distancia_atras < DISTANCIA_DE_ACCION["MAYOR QUE"]:
                    valor_t = T_AVANCE
                else:
                    if distancia_delante < 5:
                        giro_tras(valor_t, valor_d)

                if ant_d_d == distancia_delante:
                    vueltas_e += 1
                    if vueltas_e == 1:
                        giro_tras(valor_t, valor_d)
                        vueltas_e = 0

            print(f"Distancia hacia delante: {distancia_delante} cm")
            print(f"Distancia hacia atrás: {distancia_atras} cm")
            print(f"Distancia hacia izquierda: {distancia_izquierda} cm")
            print(f"Distancia hacia derecha: {distancia_derecha} cm")

            pwm_t.start(valor_t)
            pwm_d.start(valor_d)

            if vueltas == numero_de_giros_para_acabar:
                v = 0
                GPIO.cleanup()
            print(f"NumberLinea:{numberlinea}")
            print(f"Vueltas:{float(vueltas/x)} es decir {vueltas} giros")

        Am, Ar, Av = areas[2] or 0, areas[0] or 0, areas[1] or 0
        cx_r, cx_v, cx_m = centroids[0] and centroids[0][0] or 320, centroids[1] and centroids[1][0] or 320, centroids[2] and centroids[2][0] or 320

        print(f"C: R:{cx_r}, V:{cx_v}, M:{cx_m}")
        print(f"D: R:{Ar}, V:{Av}, M:{Am}")

        rawCapture.truncate(0)

        if cx_v < 266:
            print("V a la IZQ")
            if v == 1:
                valor_d = G_CENT
        elif cx_v > 266 and cx_v < 374:
            print("V al CENT")
            if v == 1:
                valor_d = G_IZQ
        else:
            print("V a la DER")
            if v == 1:
                valor_d = G_IZQ

        if cx_r < 266:
            print("R a la IZQ")
            if v == 1:
                valor_d = G_DER
        elif cx_r > 266 and cx_r < 374:
            print("R al CENT")
            if v == 1:
                valor_d = G_CENT
        else:
            print("R a la DER")
            if v == 1:
                valor_d = G_DER

        if cx_m < 266:
            print("M a la IZQ")
        elif cx_m > 266 and cx_m < 374:
            print("M al CENT")
        else:
            print("M a la DER")

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

except KeyboardInterrupt:
    pass

cv2.destroyAllWindows()
GPIO.cleanup()
