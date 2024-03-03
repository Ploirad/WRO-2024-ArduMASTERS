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
servo_pin_direccion = 18
servo_pin_traccion = 17

# Define variables
empezado = 0
distancia_delante = 0
distancia_atras = 0
distancia_izquierda = 0
distancia_derecha = 0
distancia_comienzo_derecha = 0
distancia_comienzo_izquierda = 0
valor_d = 7.5 #Direccion 2.5=izq; 7.5=centro; 12.5=der
valor_t = 7   #Traccion 6=Atras;  8=Alante;  7=stop

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

#Iniciar servos
pwm_d = GPIO.PWM(servo_pin_direccion, 50) # Frecuencia de PWM: 50Hz (estándar para servos)
pwm_t = GPIO.PWM(servo_pin_traccion, 50) # Frecuencia de PWM: 50Hz (estándar para servos)

def get_distance(trig_pin, echo_pin):
    # Envía un pulso al pin Trig
    GPIO.output(trig_pin, True)
    time.sleep(0.00001)
    GPIO.output(trig_pin, False)

    # Mide el tiempo transcurrido del pulso de eco
    while GPIO.input(echo_pin) == 0:
        pulse_start = time.time()

    while GPIO.input(echo_pin) == 1:
        pulse_end = time.time()

    # Calcula la duración del pulso de eco
    pulse_duration = pulse_end - pulse_start

    # Calcula la distancia en centímetros
    distance = pulse_duration * 17150

    # Redondea la distancia a dos decimales
    distance = round(distance, 2)

    return distance

def update_distances():
    global distancia_delante, distancia_atras, distancia_izquierda, distancia_derecha
    distancia_delante = get_distance(TRIG_PIN_DELANTE, ECHO_PIN_DELANTE)
    distancia_atras = get_distance(TRIG_PIN_ATRAS, ECHO_PIN_ATRAS)
    distancia_izquierda = get_distance(TRIG_PIN_IZQUIERDA, ECHO_PIN_IZQUIERDA)
    distancia_derecha = get_distance(TRIG_PIN_DERECHA, ECHO_PIN_DERECHA)

def cleanup():
    # Limpia los pines GPIO
    GPIO.cleanup()

def primeras_medidas_paredes():
    global distancia_comienzo_izquierda, distancia_comienzo_derecha
    distancia_comienzo_izquierda = get_distance(TRIG_PIN_IZQUIERDA, ECHO_PIN_IZQUIERDA)
    distancia_comienzo_derecha = get_distance(TRIG_PIN_DERECHA, ECHO_PIN_DERECHA)

if __name__ == '__main__':
    try:
        # Configura los pines GPIO
        setup()

        while True:
            if empezado == 0:
                primeras_medidas_paredes()
                empezado = 1
            else:
                valor_t = 12.5
                pwm_t.start(valor_t)
                
                # Actualiza las distancias
                update_distances()

                #if distancia_delante 
                
                # Muestra las distancias
                print(f"Distancia hacia delante: {distancia_delante} cm")
                print(f"Distancia hacia atras: {distancia_atras} cm")
                print(f"Distancia hacia izquierda: {distancia_izquierda} cm")
                print(f"Distancia hacia derecha: {distancia_derecha} cm")
        
                time.sleep(1)

    except KeyboardInterrupt:
        # Maneja la interrupción del teclado
        print("Programa interrumpido por el usuario")

    finally:
        # Limpia los pines GPIO
        cleanup()
