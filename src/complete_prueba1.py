import RPi.GPIO as GPIO
import time

# Define los pines
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

# Define variables
tiempo_de_giro_linea = 1
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
DISTANCIA_de_ACCION = {"MENOR QUE": 20, "MAYOR QUE": 19}
TAvance = 12.5
TAtras = 2.5
GDer = 2.5
GIzq = 12.5
GCent = 10#9.5#5.9
valor_d = GCent
valor_t = TAvance
pulse_end = 0
v = 0
girando = 0
x = 4
arrancar = False
numero_de_giros_para_acabar = x * 3

# Configura los pines GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin_direccion, GPIO.OUT)
GPIO.setup(servo_pin_traccion, GPIO.OUT)
GPIO.setup(TRIG_PIN_DELANTE, GPIO.OUT)
GPIO.setup(ECHO_PIN_DELANTE, GPIO.IN)
GPIO.setup(TRIG_PIN_ATRAS, GPIO.OUT)
GPIO.setup(ECHO_PIN_ATRAS, GPIO.IN)
GPIO.setup(TRIG_PIN_IZQUIERDA, GPIO.OUT)
GPIO.setup(ECHO_PIN_IZQUIERDA, GPIO.IN)
GPIO.setup(TRIG_PIN_DERECHA, GPIO.OUT)
GPIO.setup(ECHO_PIN_DERECHA, GPIO.IN)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Iniciar servos
pwm_d = GPIO.PWM(servo_pin_direccion, 50) # Frecuencia de PWM: 50Hz (estándar para servos)
pwm_t = GPIO.PWM(servo_pin_traccion, 50) # Frecuencia de PWM: 50Hz (estándar para servos)

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
        if distancia_izquierda > distancia_derecha:
            valor_d = GIzq
        elif distancia_izquierda < distancia_derecha:
            valor_d = GDer
        else:
            valor_d = GCent
    pwm_t.start(valor_t)
    pwm_d.start(valor_d)
    time.sleep(2)
    valor_t = TAvance
    valor_d = GCent
    pwm_t.start(valor_t)
    pwm_d.start(valor_d)

while True:
    button_state = GPIO.input(button_pin)
    pwm_d.start(valor_d)
    
    if button_state == GPIO.HIGH:
        print("Botón presionado")
        arrancar = True

    if button_state == GPIO.LOW and arrancar:
        v = 1
        arrancar = False

    try:
        if v == 1:
            pwm_t.start(valor_t)
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

                #if ant_d_d == distancia_delante:
                #    vueltas_e += 1
                #    if vueltas_e == 1:
                #        giro_tras(valor_t, valor_d)
                #        e = 0
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
                valor_t = TAvance
            elif valor_t < 6:
                print("back")
                valor_t = TAtras
            else:
                print("stop")
            if valor_d > 11:
                print("izquierda")
                valor_d = GIzq
            elif valor_d < 4:
                print("derecha")
                valor_d = GDer
            else:
                print("centro")
                valor_d = GCent
            if vueltas == numero_de_giros_para_acabar:
                v = 0
                GPIO.cleanup()
            print(f"Vueltas:{float(vueltas/x)} es decir {vueltas} giros")
    except KeyboardInterrupt:
        GPIO.cleanup()
    except:
        pass
