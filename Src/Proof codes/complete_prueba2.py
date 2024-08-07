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

pwm_d = GPIO.PWM(servo_pin_direccion, 50)  # Frecuencia de PWM: 50Hz (estándar para servos)
pwm_t = GPIO.PWM(servo_pin_traccion, 50)  # Frecuencia de PWM: 50Hz (estándar para servos)

# Define variables
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
distancia_comienzo_derecha = 0
distancia_comienzo_izquierda = 0
DISTANCIA_de_ACCION = {"MENOR QUE": 15, "MAYOR QUE": 14}
TAvance = 12.5
TAtras = 2.5
GDer = 4.5
GIzq = 10.5
GCent = 5.9
valor_d = GCent
valor_t = TAvance
pulse_end = 0
v = 0
girando = 0
x = 4
comprobar_morado = False
numero_de_giros_para_acabar = x * 3
camera = PiCamera()
camera.resolution = (640, 480)
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)

def get_distance(trig_pin, echo_pin):
    # Envía un pulso al pin Trig
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
    distance = round(distance, 3)
    return distance

def update_distances():
    global distancia_delante, distancia_atras, distancia_izquierda, distancia_derecha, ant_d_d
    ant_d_d = distancia_delante
    distancia_delante = get_distance(TRIG_PIN_DELANTE, ECHO_PIN_DELANTE)
    distancia_atras = get_distance(TRIG_PIN_ATRAS, ECHO_PIN_ATRAS)
    distancia_izquierda = get_distance(TRIG_PIN_IZQUIERDA, ECHO_PIN_IZQUIERDA)
    distancia_derecha = get_distance(TRIG_PIN_DERECHA, ECHO_PIN_DERECHA)

def giro_linea(valor_t, valor_d):
    print("girando...")
    pwm_t.start(valor_t)
    pwm_d.start(valor_d)
    time.sleep(tiempo_de_giro_linea)
    pwm_t.start(valor_t)
    pwm_d.start(GCent)

def giro_tras(valor_t, valor_d):
    valor_t = TAtras
    if valor_d == GIzq:
        valor_d = GDer
    elif valor_d == GDer:
        valor_d = GIzq
    else:
        valor_d = GCent
    pwm_t.start(valor_t)
    pwm_d.start(valor_d)
    time.sleep(2)
    valor_t = TAvance
    if valor_d == GIzq:
        valor_d = GDer
    elif valor_d == GDer:
        valor_d = GIzq
    else:
        valor_d = GCent
    pwm_t.start(valor_t)
    pwm_d.start(valor_d)
    time.sleep(2)
    valor_t = TAvance
    valor_d = GCent
    pwm_t.start(valor_t)
    pwm_d.start(valor_d)

def detect_colors(frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # 238, 39, 55 ///  68, 214, 44 /// 255, 0, 255
    # Nuevos rangos de color
    lower_red = np.array([175, 126, 68])
    upper_red = np.array([176, 212, 255])
    lower_green = np.array([62, 147, 49])
    upper_green = np.array([65, 156, 255])
    lower_magenta = np.array([138, 87, 25])
    upper_magenta = np.array([167, 185, 255])

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

AmV = True
z = True
def compM(Am):
    global cx_m, distancia_derecha, distancia_izquierda, distancia_atras, distancia_delante, AmV
    p = 0
    print(f"p = {p}; AmV = {AmV}")
    if AmV == False:
        if cx_m < 266:
            print(f"M a la IZQ y {mf}")
            p = 1
        elif cx_m > 266 and cx_m < 374:
            print(f"M al CENT y {mf}")
            if distancia_derecha >= distancia_izquierda:
                p = 2
            elif distancia_derecha < distancia_izquierda:
                p = 1
        else:
            print(f"M a la DER y {mf}")
            p = 2
    if p != 0:
        pwm_t.start(TAvance)
        pwm_d.start(GCent)
        time.sleep(3.5)
        if p == 1:
            while distancia_atras > 5 or distancia_delante > 5:
                pwm_t.start(TAtras)
                pwm_d.start(GIzq)
            if distancia_atras <= 5 or distancia_delante <= 5:
                v = 0
                z = False
        if p == 2:
            while distancia_atras > 5 or distancia_delante > 5:
                pwm_t.start(TAtras)
                pwm_d.start(GDer)
            if distancia_atras <= 5 or distancia_delante <= 5:
                v = 0
                z = False
        
# Bucle principal
while z:
    try:
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            update_distances()
            # Captura de imagen
            image = frame.array
    
            # Detección de colores y análisis de imagen
            masks, cx, dimensions, A = detect_colors(image)
    
            # Mostrar las máscaras de color y la imagen original en ventanas separadas con tamaños personalizados
            #cv2.namedWindow("Original", cv2.WINDOW_NORMAL)
            #cv2.resizeWindow("Original", 200, 150)
            #cv2.imshow("Original", image)
    
            #cv2.namedWindow("Red Mask", cv2.WINDOW_NORMAL)
            #cv2.resizeWindow("Red Mask", 200, 150)
            #cv2.imshow("Red Mask", masks[0])
    
            #cv2.namedWindow("Green Mask", cv2.WINDOW_NORMAL)
            #cv2.resizeWindow("Green Mask", 200, 150)
            #cv2.imshow("Green Mask", masks[1])
    
            #cv2.namedWindow("Magenta Mask", cv2.WINDOW_NORMAL)
            #cv2.resizeWindow("Magenta Mask", 200, 150)
            #cv2.imshow("Magenta Mask", masks[2])
    
            # Lee el estado del botón
            button_state = GPIO.input(button_pin)
            pwm_d.start(valor_d)
    
            if button_state == GPIO.HIGH:
                print("Botón presionado")
                v = 1
    
            if v == 1:
                pwm_t.start(valor_t)
                if distancia_delante < DISTANCIA_de_ACCION["MENOR QUE"] and distancia_izquierda < DISTANCIA_de_ACCION["MENOR QUE"] and distancia_derecha < DISTANCIA_de_ACCION["MENOR QUE"]:
                        valor_t = TAtras
                        valor_d = GCent
                else:
                    if girando == 0:
                        if distancia_delante < DISTANCIA_de_ACCION["MENOR QUE"] and distancia_derecha > DISTANCIA_de_ACCION["MAYOR QUE"] and distancia_derecha > distancia_izquierda:
                            # DERECHA
                            valor_t = TAvance
                            valor_d = GDer
                            girando = 1
                            vueltas += 1
                            giro_linea(valor_t, valor_d)
                        elif distancia_delante < DISTANCIA_de_ACCION["MENOR QUE"] and distancia_izquierda > DISTANCIA_de_ACCION["MAYOR QUE"] and distancia_izquierda > distancia_derecha:
                            # IZQUIERDA
                            valor_t = TAvance
                            valor_d = GIzq
                            girando = 1
                            vueltas += 1
                            giro_linea(valor_t, valor_d)
                    elif distancia_delante > DISTANCIA_de_ACCION["MAYOR QUE"]:
                        # AVANCE
                        valor_t = TAvance
                        valor_d = GCent
                        girando = 0
    
                    if distancia_izquierda < 6:
                        # DERECHA
                        valor_t = TAvance
                        valor_d = GDer
                        giro_linea(valor_t, valor_d)
    
                    if distancia_derecha < 6:
                        # IZQUIERDA
                        valor_t = TAvance
                        valor_d = GIzq
                        giro_linea(valor_t, valor_d)
    
                    if distancia_atras < DISTANCIA_de_ACCION["MAYOR QUE"]:
                        valor_t = TAvance
                    else:
                        if distancia_delante < 5:
                            giro_tras(valor_t, valor_d)
    
                    if ant_d_d == distancia_delante:
                        vueltas_e += 1
                        if vueltas_e == 1:
                            giro_tras(valor_t, valor_d)
                            vueltas_e = 0
                # Muestra las distancias
                print(f"Distancia hacia delante: {distancia_delante} cm")
                print(f"Distancia hacia atras: {distancia_atras} cm")
                print(f"Distancia hacia izquierda: {distancia_izquierda} cm")
                print(f"Distancia hacia derecha: {distancia_derecha} cm")
                print("")
                pwm_t.start(valor_t)
                pwm_d.start(valor_d)
                if valor_t > 8:
                    print("avanti")
                elif valor_t < 6:
                    print("back")
                else:
                    print("stop")
                if valor_d > 11:
                    print("izquierda")
                elif valor_d < 4:
                    print("derecha")
                else:
                    print("centro")
                if vueltas == 9:
                    comprobar_morado = True
                if vueltas == numero_de_giros_para_acabar:
                    v = 0
                    GPIO.cleanup()
                print(f"NumberLinea:{numberlinea}")
                print(f"Vueltas:{float(vueltas/x)} es decir {vueltas} giros")
    
            Am, Ar, Av = A[2], A[0], A[1]  # Cambiar el orden
            if Am is None:
                AmV = True
                Am = 0
            else:
                AmV = False
            if Ar is None:
                Ar = 0
            if Av is None:
                Av = 0
    
            cx_v, cx_r, cx_m = cx[1], cx[0], cx[2]
            if cx_v is None:
                cx_v = 320
                vf = True
            else:
                vf = False
            if cx_r is None:
                cx_r = 320
                rf = True
            else:
                rf = False
            if cx_m is None:
                cx_m = 320
                mf = True
            else:
                mf = False
    
            print(f"C: R:{cx_r}, V:{cx_v}, M:{cx_m}")
            print(f"D: R:{Ar}, V:{Av}, M:{Am}")
            # Limpiar el búfer de captura para la siguiente imagen
            rawCapture.truncate(0)
            if cx_v < 266:
                print("V a la IZQ")
                if (not vf) and v == 1:
                    valor_d = GCent
                    
            elif cx_v > 266 and cx_v < 374:
                print("V al CENT")
                if (not vf) and v == 1:
                    valor_d = GIzq
                
            else:
                print("V a la DER")
                if (not vf) and v == 1:
                    valor_d = GIzq
                
            if cx_r < 266:
                print("R a la IZQ")
                if (not rf) and v == 1:
                    valor_d = GDer
                
            elif cx_r > 266 and cx_r < 374:
                print("R al CENT")
                if (not rf) and v == 1:
                    valor_d = GCent
                
            else:
                print("R a la DER")
                if (not rf) and v == 1:
                    valor_d = GDer
            if comprobar_morado:   
                compM(Am)
            # Esperar una tecla para salir (salida si se presiona 'q')
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                z = False
                break
    
    except KeyboardInterrupt:
        pass

# Limpiar y cerrar las ventanas
cv2.destroyAllWindows()

# Limpiar configuraciones de GPIO
GPIO.cleanup()
