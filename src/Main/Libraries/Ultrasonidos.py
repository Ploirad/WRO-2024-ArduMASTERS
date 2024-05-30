import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.IN)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.IN)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.IN)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(10, GPIO.IN)

def measure_distance(position):
    
    # Definir los pines GPIO a utilizar
    if position == 1:
        GPIO_TRIGGER = 23
        GPIO_ECHO = 24
    elif position == 2:
        GPIO_TRIGGER = 5
        GPIO_ECHO = 6
    elif position == 3:
        GPIO_TRIGGER = 17
        GPIO_ECHO = 27
    elif position == 4:
        GPIO_TRIGGER = 22
        GPIO_ECHO = 10

    # Asegurarse de que el pin TRIG está limpio
    GPIO.output(GPIO_TRIGGER, False)
    time.sleep(2)

    # Enviar un pulso de 10µs para disparar el sensor
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    # Guardar el tiempo de inicio y fin del pulso
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()

    # Calcular la duración del pulso
    elapsed_time = stop_time - start_time

    # La velocidad del sonido es 34300 cm/s
    distance = (elapsed_time * 34300) / 2

    return distance

print(measure_distance(1))
print(measure_distance(2))
print(measure_distance(3))
print(measure_distance(4))
