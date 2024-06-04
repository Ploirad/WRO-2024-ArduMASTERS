import cv2
import numpy as np

# Inicializa la captura de video desde la cámara
cap = cv2.VideoCapture(0)

# Define los rangos de colores
lower_red = np.array([175, 126, 68])
upper_red = np.array([176, 212, 255])

lower_green = np.array([62, 147, 49])
upper_green = np.array([65, 156, 255])

lower_magenta = np.array([138, 87, 25])
upper_magenta = np.array([167, 185, 255])

# Función para encontrar centroides
def find_centroid(mask):
    M = cv2.moments(mask)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        return cx, cy
    else:
        return None

while True:
    # Lee un fotograma de la cámara
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar el fotograma")
        break

    # Convierte el fotograma a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold para cada rango de color
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_magenta = cv2.inRange(hsv, lower_magenta, upper_magenta)

    # Encuentra los centroides
    centroid_red = find_centroid(mask_red)
    centroid_green = find_centroid(mask_green)
    centroid_magenta = find_centroid(mask_magenta)

    # Imprime las coordenadas de los centroides en la consola
    if centroid_red:
        print("Centroide rojo:", centroid_red)
    else:
        print("No se encontraron centroides rojos.")
    if centroid_green:
        print("Centroide verde:", centroid_green)
    else:
        print("No se encontraron centroides verdes.")
    if centroid_magenta:
        print("Centroide magenta:", centroid_magenta)
    else:
        print("No se encontraron centroides magenta.")

    # Sal del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera la captura de video
cap.release()
