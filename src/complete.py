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
IRsensor = 8

# Define variables
tiempo_de_giro_linea = 1
numberlinea = 0
vueltas = 0
empezado = 0
distancia_delante = 0
distancia_atras = 0
distancia_izquierda = 0
distancia_derecha = 0
distancia_comienzo_derecha = 0
distancia_comienzo_izquierda = 0
DISTANCIA_de_ACCION = {"MENOR QUE": 25, "MAYOR QUE": 24}
TAvance = 12.5
TAtras = 2.5
GDer = 3.5
GIzq = 11.5
GCent = 5.9
valor_d = GCent
valor_t = TAvance
pulse_end = 0
v = 0
girando = 0

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
GPIO.setup(IRsensor, GPIO.IN)

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

def giro(valor_t, valor_d):
    print("girando...")
    pwm_t.start(valor_t)
    pwm_d.start(valor_d)
    time.sleep(1)
    pwm_t.start(valor_t)
    pwm_d.start(GCent)
    time.sleep(0.5)
    pwm_t.start(valor_t)
    if valor_d == GIzq:
        pwm_d.start(GDer)
    elif valor_d == GDer:
        pwm_d.start(GIzq)
    else:
        pwm_d.start(GCent)
    time.sleep(1)
    valor_t = TAvance
    valor_d = GCent
    print("...girado")

def giro_linea(valor_t, valor_d):
    print("girando...")
    pwm_t.start(valor_t)
    pwm_d.start(valor_d)
    time.sleep(tiempo_de_giro_linea)
    pwm_t.start(valor_t)
    pwm_d.start(GCent)

while True:
    # Lee el estado del botón
    button_state = GPIO.input(button_pin)
    pwm_d.start(valor_d)
    
    if button_state == GPIO.HIGH:
        print("Botón presionado")
        if v == 0:
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
            GPIO.setup(IRsensor, GPIO.IN)
        v = 1

    try:
        if v == 1:
            try:
                pwm_t.start(valor_t)
                # Lee el estado del botón
                button_state = GPIO.input(button_pin)
                
                # Si el botón está presionado (estado HIGH)
                if button_state == GPIO.HIGH:
                    print("Botón presionado")
                
                # Actualiza las distancias
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
                    elif distancia_delante < DISTANCIA_de_ACCION["MENOR QUE"] and distancia_derecha < DISTANCIA_de_ACCION["MENOR QUE"] and distancia_izquierda < DISTANCIA_de_ACCION["MENOR QUE"]:
                        #ATRAS
                        valor_t = TAtras
                        valor_d = GCent
                    elif distancia_delante > DISTANCIA_de_ACCION["MAYOR QUE"]:
                        #AVANCE
                        valor_t = TAvance
                        valor_d = GCent
                        girando = 0
                
                    #if distancia_izquierda < 7 and distancia_derecha > distancia_izquierda:
                        #DERECHA
                     #   valor_t = TAvance
                      #  valor_d = GDer
                       # giro(valor_t, valor_d)
            
#                    if distancia_derecha < 7 and distancia_izquierda > distancia_derecha:
 #                       #IZQUIERDA
  #                      valor_t = TAvance
   #                     valor_d = GIzq
    #                    giro(valor_t, valor_d)
            
     #               if distancia_atras < DISTANCIA_de_ACCION["MAYOR QUE"]:
      #                  valor_t = TAvance
                
                #print()
                print(f"NumberLinea:{numberlinea}")
                print(f"Linea:{linea}")
                print(f"Vueltas:{float(vueltas/8)} es decir {vueltas} giros")
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
                
                linea = GPIO.input(IRsensor)
     #           if linea == 1:
      #              numberlinea = numberlinea + 1
       #             vueltas = vueltas + 1
              #      if distancia_derecha > distancia_izquierda:
                        #DERECHA
       #                 valor_t = TAvance
        #                valor_d = GDer
         #               giro_linea(valor_t, valor_d)
            
             #       elif distancia_izquierda > distancia_derecha:
                        #IZQUIERDA
          #              valor_t = TAvance
           #             valor_d = GIzq
            #            giro_linea(valor_t, valor_d)
                if vueltas == 24:
                    v = 0
                    GPIO.cleanup()
                    
            except:
                print("ERROR")
                if KeyboardInterrupt:
                    v = 0
                    GPIO.cleanup()
    except KeyboardInterrupt:
        GPIO.cleanup()
