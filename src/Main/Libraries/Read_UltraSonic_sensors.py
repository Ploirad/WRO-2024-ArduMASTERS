from External_Libraries import threading
from External_Libraries import time

distance = 0.0

# Definir una función para leer las distancias desde los archivos
def leer_distancias(sensor_id):
    archivo = f"/tmp/sensor_{sensor_id}.txt"
    while True:
        try:
            with open(archivo, "r") as f:
                # Leer todas las líneas del archivo y obtener la última distancia registrada
                lineas = f.readlines()
                if lineas:
                    ultima_distancia = lineas[-1].strip()
                    print(f"Sensor {sensor_id}: {ultima_distancia} cm")
                    distance = ultima_distancia
        except FileNotFoundError:
            print(f"Archivo para el sensor {sensor_id} no encontrado.")
        except Exception as e:
            print(f"eREAD = {e}")

# Crear y empezar los hilos para leer las distancias
threads = []
for i in range(4):
    t = threading.Thread(target=leer_distancias, args=(i,))
    print(f"t = {t}")
    print(f"d = {distance}")
    t.start()
    threads.append(t)

# Esperar a que los hilos terminen (aunque en este caso, no terminarán)
for t in threads:
    t.join()
