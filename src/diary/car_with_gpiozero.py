from gpiozero import Servo, DistanceSensor, Button
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
IRsensor = 8

# Define variables
numberlinea = 0
vueltas = 0
distancia_delante = 0
distancia_atras = 0
distancia_izquierda = 0
distancia_derecha = 0
valor_d = 0.0
valor_t = 0.0
DISTANCIA_de_ACCION = {"MENOR QUE": 15, "MAYOR QUE": 14}

# Inicializar dispositivos
servo_direccion = Servo(servo_pin_direccion)
servo_traccion = Servo(servo_pin_traccion)
button = Button(button_pin)
sensor_delante = DistanceSensor(TRIG_PIN_DELANTE, ECHO_PIN_DELANTE)
sensor_atras = DistanceSensor(TRIG_PIN_ATRAS, ECHO_PIN_ATRAS)
sensor_izquierda = DistanceSensor(TRIG_PIN_IZQUIERDA, ECHO_PIN_IZQUIERDA)
sensor_derecha = DistanceSensor(TRIG_PIN_DERECHA, ECHO_PIN_DERECHA)

def update_distances():
    global distancia_delante, distancia_atras, distancia_izquierda, distancia_derecha
    distancia_delante = sensor_delante.distance * 100  # Convertir a cm
    distancia_atras = sensor_atras.distance * 100  # Convertir a cm
    distancia_izquierda = sensor_izquierda.distance * 100  # Convertir a cm
    distancia_derecha = sensor_derecha.distance * 100  # Convertir a cm

def giro(valor_t, valor_d):
    servo_traccion.value = valor_t
    servo_direccion.value = valor_d
    time.sleep(2)
    servo_traccion.value = 0.0  # Detener tracción
    servo_direccion.value = 0.0  # Centrar dirección
    time.sleep(2)
    servo_traccion.value = valor_t
    if valor_d == -1.0:
        servo_direccion.value = 1.0
    elif valor_d == 1.0:
        servo_direccion.value = -1.0
    else:
        servo_direccion.value = 0.0
    time.sleep(2)
    servo_traccion.value = 0.0  # Detener tracción
    servo_direccion.value = 0.0  # Centrar dirección

while True:
    if button.is_pressed:
        print("Botón presionado")
        time.sleep(0.2)  # Debounce
        
        # Obtener valores del servo
        valor_d = 1.0  # Valor para girar a la derecha
        valor_t = 1.0  # Valor para avanzar
        
        giro(valor_t, valor_d)
    
    try:
        # Actualizar distancias
        update_distances()
        
        # Lógica de control aquí
        if distancia_delante < DISTANCIA_de_ACCION["MENOR QUE"]:
            valor_t = -1.0  # Retroceder
            valor_d = 0.0  # Centrar dirección
            giro(valor_t, valor_d)
        elif distancia_izquierda < DISTANCIA_de_ACCION["MENOR QUE"]:
            valor_t = 1.0  # Avanzar
            valor_d = 1.0  # Girar a la derecha
            giro(valor_t, valor_d)
        elif distancia_derecha < DISTANCIA_de_ACCION["MENOR QUE"]:
            valor_t = 1.0  # Avanzar
            valor_d = -1.0  # Girar a la izquierda
            giro(valor_t, valor_d)
        else:
            valor_t = 1.0  # Avanzar
            valor_d = 0.0  # Centrar dirección
            giro(valor_t, valor_d)
        
        # Muestra las distancias
        print(f"Distancia hacia delante: {distancia_delante} cm")
        print(f"Distancia hacia atrás: {distancia_atras} cm")
        print(f"Distancia hacia izquierda: {distancia_izquierda} cm")
        print(f"Distancia hacia derecha: {distancia_derecha} cm")
        print("")
    
    except KeyboardInterrupt:
        break

# Detener todos los servos y limpiar GPIO al salir
servo_direccion.close()
servo_traccion.close()
GPIO.cleanup()
