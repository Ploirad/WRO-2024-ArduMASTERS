from External_Libraries import GPIO
from External_Libraries import time
from External_Libraries import threading

# Configuración de los pines GPIO para los sensores
TRIG = [23, 8, 17, 22]
ECHO = [24, 7, 27, 10]

# Configuración de GPIO
GPIO.setmode(GPIO.BCM)
for i in range(4):
    GPIO.setup(TRIG[i], GPIO.OUT)
    GPIO.setup(ECHO[i], GPIO.IN)

# Función para medir la distancia
def medir_distancia(trig, echo):
    GPIO.output(trig, False)
    
    while True:
        GPIO.output(trig, True)
        time.sleep(0.00001)
        GPIO.output(trig, False)

        while GPIO.input(echo) == 0:
            pulse_start = time.time()

        while GPIO.input(echo) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        yield distance

# Función que ejecuta cada hilo
def capturar_distancia(sensor_id):
    archivo = f"/tmp/sensor_{sensor_id}.txt"
    trig = TRIG[sensor_id]
    echo = ECHO[sensor_id]

    with open(archivo, "w") as f:
        for distancia in medir_distancia(trig, echo):
            f.write(distancia)

# Crear y empezar los hilos
threads = []
try:
    while True:
        for i in range(4):
            t = threading.Thread(target=capturar_distancia, args=(i,))
            t.start()
            threads.append(t)
        # Esperar a que los hilos terminen (aunque en este caso, no terminarán)
        for t in threads:
            t.join()
except Exception as e:
    print(f"eWRITE = {e}")
finally:
    # Limpiar los pines GPIO al finalizar
    GPIO.cleanup()