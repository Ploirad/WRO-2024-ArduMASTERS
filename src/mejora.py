import RPi.GPIO as GPIO
import time
import cv2
import numpy as np

# Define constants
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
IR_SENSOR = 8

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
DISTANCIA_de_ACCION = {"MENOR QUE": 25, "MAYOR QUE": 24}
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
numero_de_giros_para_acabar = x * 3
resolucion = (640,480)
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, resolucion[0])
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, resolucion[1])
bajoR, altoR = np.array([174, 175, 138]),np.array([176, 212, 163])
bajoG, altoG = np.array([57, 104, 114]),np.array([65, 156, 140])
bajoM, altoM = np.array([164, 148, 134]),np.array([167, 185, 168])

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SERVO_PIN_DIRECCION, GPIO.OUT)
    GPIO.setup(SERVO_PIN_TRACCION, GPIO.OUT)
    GPIO.setup(TRIG_PIN_DELANTE, GPIO.OUT)
    GPIO.setup(ECHO_PIN_DELANTE, GPIO.IN)
    GPIO.setup(TRIG_PIN_ATRAS, GPIO.OUT)
    GPIO.setup(ECHO_PIN_ATRAS, GPIO.IN)
    GPIO.setup(TRIG_PIN_IZQUIERDA, GPIO.OUT)
    GPIO.setup(ECHO_PIN_IZQUIERDA, GPIO.IN)
    GPIO.setup(TRIG_PIN_DERECHA, GPIO.OUT)
    GPIO.setup(ECHO_PIN_DERECHA, GPIO.IN)GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(IR_SENSOR, GPIO.IN)

def setup_servos():
    global pwm_d, pwm_t
    pwm_d = GPIO.PWM(SERVO_PIN_DIRECCION, 50) # Frecuencia de PWM: 50Hz (estándar para servos)
    pwm_t = GPIO.PWM(SERVO_PIN_TRACCION, 50) # Frecuencia de PWM: 50Hz (estándar para servos)

def test_color(frame, bajo, alto, color):
    frame2 = frame.copy()
    frameHSV = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(frameHSV, bajo, alto)
    cx, cy, w, h = obtener_centroide(mask)
    frame2[mask == 255] = color
    cv2.circle(frame2, (cx,cy), 5,(0,0,255), -1)
    return frame2, mask, cx,cy, w, h

def obtener_centroide(imgBin):
    cx = 0
    cy = 0
    cBlancas = cv2.findNonZero(imgBin)
    x, y, w, h = cv2.boundingRect(cBlancas)
    try:
        sumX, sumY = np.sum(cBlancas, axis=0).squeeze()
        nPuntos = len(cBlancas)
        cx = int(sumX / nPuntos)
        cy = int(sumY / nPuntos)
    except:
        pass
    return cx, cy, w, h

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

def main():
    global v
    setup_gpio()
    setup_servos()
    pwm_d.start(valor_d)
    try:
        while True:
            # Lee el estado del botón
            button_state = GPIO.input(BUTTON_PIN)
            if button_state == GPIO.HIGH:
                print("Botón presionado")
                v = 1
            if v == 1:
                ret, frame = camera.read()
                if ret:
                    f, mask1, cx1, cy1, w1, h1 = test_color(frame, bajoR, altoR, (355, 83, 93))
                    f, mask2, cx2, cy2, w2, h2 = test_color(frame, bajoG, altoG, (111, 79, 83))
                    f, mask3, cx3, cy3, w3, h3 = test_color(frame, bajoM, altoM, (300, 100, 100))
                    print([cx1,cy1], [cx2, cy2], [cx3, cy3])
                    print([w1, h1], [w2, h2], [w3, h3])
                    cv2.imshow("frame: Rojo", mask1)
                    cv2.imshow("frame: Verde", mask2)
                    cv2.imshow("frame: Morado", mask3)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                    update_distances()
                    if distancia_delante < DISTANCIA_de_ACCION["MENOR QUE"] and distancia_izquierda < DISTANCIA_de_ACCION["MENOR QUE"] and distancia_derecha < DISTANCIA_de_ACCION["MENOR QUE"]:
                        valor_t = TAtras
                        valor_d = GCent
                    else:
                        if girando == 0:
                            if distancia_delante < DISTANCIA_de_ACCION["MENOR QUE"] and distancia_derecha > DISTANCIA_de_ACCION["MAYOR QUE"] and distancia_derecha > distancia_izquierda:
                                #DERECHA
                                valor_t = TAvance
                                valor_d = GDer
                                girando = 1
                                vueltas += 1
                                giro_linea(valor_t, valor_d)
                            elif distancia_delante < DISTANCIA_de_ACCION["MENOR QUE"] and distancia_izquierda > DISTANCIA_de_ACCION["MAYOR QUE"] and distancia_izquierda > distancia_derecha:
                                #IZQUIERDA
                                valor_t = TAvance
                                valor_d = GIzq
                                girando = 1
                                vueltas += 1
                                giro_linea(valor_t, valor_d)
                    elif distancia_delante > DISTANCIA_de_ACCION["MAYOR QUE"]:
                        #AVANCE
                        valor_t = TAvance
                        valor_d = GCent
                        girando = 0

                    if distancia_izquierda < 6:
                        #DERECHA
                        valor_t = TAvance
                       valor_d = GDer
                        giro_linea(valor_t, valor_d)

                    if distancia_derecha < 6:
                        #IZQUIERDA
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
                            e = 0
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
                linea = GPIO.input(IR_SENSOR)
                if vueltas == numero_de_giros_para_acabar:
                    v = 0
                    GPIO.cleanup()
                print(f"NumberLinea:{numberlinea}")
                print(f"Linea:{linea}")
                print(f"Vueltas:{float(vueltas/x)} es decir {vueltas} giros")
    except KeyboardInterrupt:
        GPIO.cleanup()
    except:
        pass

if __name__ == "__main__":
    main()
