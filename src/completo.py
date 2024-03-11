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
empezado = 0
distancia_delante = 0
distancia_atras = 0
distancia_izquierda = 0
distancia_derecha = 0
distancia_comienzo_derecha = 0
distancia_comienzo_izquierda = 0
valor_d = 7.5
valor_t = 7   #Traccion 2.5=Atras;  12.5=Alante;  7=stop
DISTANCIA_de_ACCION = {"MENOR QUE": 15, "MAYOR QUE": 14}
TAvance = 12
TAtras = 3
GDer = 3.5
GIzq = 11.5
GCent = 6.2
pulse_end = 0

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
    
    # Mide el tiempo transcurrido del pulso de eco
    while GPIO.input(echo_pin) == 0:
        pulse_start = time.time()

    while GPIO.input(echo_pin) == 1:
        pulse_end = time.time()

    # Calcula la duración del pulso de eco
    pulse_duration = pulse_end - pulse_start

    # Calcula la distancia en centímetros
    distance = pulse_duration * 17150

    # Redondea la distancia a tres decimales
    distance = round(distance, 3)

    return distance

def update_distances():
    global distancia_delante, distancia_atras, distancia_izquierda, distancia_derecha
    distancia_delante = get_distance(TRIG_PIN_DELANTE, ECHO_PIN_DELANTE)
    distancia_atras = get_distance(TRIG_PIN_ATRAS, ECHO_PIN_ATRAS)
    distancia_izquierda = get_distance(TRIG_PIN_IZQUIERDA, ECHO_PIN_IZQUIERDA)
    distancia_derecha = get_distance(TRIG_PIN_DERECHA, ECHO_PIN_DERECHA)

while True:
    try:
        pwm_t.start(valor_t)
        pwm_d.start(valor_d)
        # Lee el estado del botón
        button_state = GPIO.input(button_pin)
        
        # Si el botón está presionado (estado HIGH)
        if button_state == GPIO.HIGH:
            print("Botón presionado")
        
        # Actualiza las distancias
        update_distances()

        if distancia_delante < DISTANCIA_de_ACCION["MENOR QUE"] and distancia_derecha > DISTANCIA_de_ACCION["MAYOR QUE"]:
            #DERECHA
            valor_t = TAvance
            valor_d = GDer
        elif distancia_delante < DISTANCIA_de_ACCION["MENOR QUE"] and distancia_derecha < DISTANCIA_de_ACCION["MENOR QUE"] and distancia_izquierda > DISTANCIA_de_ACCION["MAYOR QUE"]:
            #IZQUIERDA
            valor_t = TAvance
            valor_d = GIzq
        elif distancia_delante < DISTANCIA_de_ACCION["MENOR QUE"] and distancia_derecha < DISTANCIA_de_ACCION["MENOR QUE"] and distancia_izquierda < DISTANCIA_de_ACCION["MENOR QUE"]:
            #ATRAS
            valor_t = TAtras
            valor_d = GCent
        elif distancia_delante > DISTANCIA_de_ACCION["MAYOR QUE"]:
            #AVANCE
            valor_t = TAvance
            valor_d = GCent
        
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
            print("izuierda")
        elif valor_d < 4:
            print("derecha")
        else:
            print("centro")
    except KeyboardInterrupt:
        GPIO.cleanup()
        
