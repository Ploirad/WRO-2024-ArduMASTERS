from gpiozero import Servo, DistanceSensor, Button
import time

# Define los pines
servo_pin_direccion = 2
servo_pin_traccion = 3
button_pin = 9

# Define las constantes
TAvance = 12.5
TAtras = 2.5
GDer = 3.5
GIzq = 11.5
GCent = 6.0
DISTANCIA_de_ACCION = {"MENOR QUE": 15, "MAYOR QUE": 14}

# Configura el servo y el sensor de ultrasonidos
servo_direccion = Servo(servo_pin_direccion)
ultrasonido_delante = DistanceSensor(echo=24, trigger=23)
ultrasonido_atras = DistanceSensor(echo=27, trigger=17)
ultrasonido_izquierda = DistanceSensor(echo=10, trigger=22)
ultrasonido_derecha = DistanceSensor(echo=6, trigger=5)
boton = Button(button_pin)

# Función para el giro del servo
def giro(valor_t, valor_d):
    print("girando...")
    servo_direccion.value = valor_d
    time.sleep(2)
    servo_direccion.value = GCent
    time.sleep(2)
    servo_direccion.value = GIzq if valor_d == GIzq else GDer if valor_d == GDer else GCent
    time.sleep(2)
    print("...girado")

try:
    while True:
        boton.wait_for_press()
        print("Botón presionado")
        
        # Leer las distancias de los sensores de ultrasonidos
        distancia_delante = ultrasonido_delante.distance * 100  # Convertir a centímetros
        distancia_atras = ultrasonido_atras.distance * 100
        distancia_izquierda = ultrasonido_izquierda.distance * 100
        distancia_derecha = ultrasonido_derecha.distance * 100
        
        # Actualizar la dirección del servo
        servo_direccion.value = TAvance
        
        # Determinar la acción en función de las distancias medidas
        if (distancia_delante < DISTANCIA_de_ACCION["MENOR QUE"] and
            distancia_izquierda < DISTANCIA_de_ACCION["MENOR QUE"] and
            distancia_derecha < DISTANCIA_de_ACCION["MENOR QUE"]):
            servo_direccion.value = TAtras, GCent
        else:
            if (distancia_delante < DISTANCIA_de_ACCION["MENOR QUE"] and
                distancia_derecha > DISTANCIA_de_ACCION["MAYOR QUE"] and
                distancia_derecha > distancia_izquierda):
                # DERECHA
                giro(TAvance, GDer)
            elif (distancia_delante < DISTANCIA_de_ACCION["MENOR QUE"] and
                  distancia_izquierda > DISTANCIA_de_ACCION["MAYOR QUE"] and
                  distancia_izquierda > distancia_derecha):
                # IZQUIERDA
                giro(TAvance, GIzq)
            elif (distancia_delante < DISTANCIA_de_ACCION["MENOR QUE"] and
                  distancia_derecha < DISTANCIA_de_ACCION["MENOR QUE"] and
                  distancia_izquierda < DISTANCIA_de_ACCION["MENOR QUE"]):
                # ATRAS
                servo_direccion.value = TAtras, GCent
            elif distancia_delante > DISTANCIA_de_ACCION["MAYOR QUE"]:
                # AVANCE
                servo_direccion.value = TAvance, GCent
        
        # Mostrar las distancias y la dirección del servo
        print(f"Distancia hacia delante: {distancia_delante} cm")
        print(f"Distancia hacia atrás: {distancia_atras} cm")
        print(f"Distancia hacia izquierda: {distancia_izquierda} cm")
        print(f"Distancia hacia derecha: {distancia_derecha} cm")
        print("")
        
        # Mostrar la dirección del servo
        if 8 < servo_direccion.value < 12:
            print("avanti")
        elif servo_direccion.value < 6:
            print("back")
        else:
            print("stop")
        
        if servo_direccion.value > 11:
            print("izquierda")
        elif servo_direccion.value < 4:
            print("derecha")
        else:
            print("centro")
        
        # Leer el estado del sensor de línea
        if not IRsensor.is_pressed:
            numberlinea += 1
            vueltas += 1
            if distancia_derecha > distancia_izquierda:
                # DERECHA
                giro(TAvance, GDer)
            elif distancia_izquierda > distancia_derecha:
                # IZQUIERDA
                giro(TAvance, GIzq)

except KeyboardInterrupt:
    print("Programa detenido por el usuario")
finally:
    servo_direccion.detach()
