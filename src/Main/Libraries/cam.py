import numpy as np
import cv2

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

# Captura de video desde la cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir de BGR a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold para cada rango de color
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_magenta = cv2.inRange(hsv, lower_magenta, upper_magenta)

    # Encuentra los centroides
    centroid_red = find_centroid(mask_red)
    centroid_green = find_centroid(mask_green)
    centroid_magenta = find_centroid(mask_magenta)

    # Dibuja los centroides en el marco original
    if centroid_red:
        cv2.circle(frame, centroid_red, 5, (0, 0, 255), -1)
    if centroid_green:
        cv2.circle(frame, centroid_green, 5, (0, 255, 0), -1)
    if centroid_magenta:
        cv2.circle(frame, centroid_magenta, 5, (255, 0, 255), -1)

    # Muestra el marco
    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera la cámara y cierra todas las ventanas
cap.release()
cv2.destroyAllWindows()
