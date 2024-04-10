 import cv2
import numpy as np

# Definimos una función para detectar colores y obtener coordenadas
def detect_colors(frame):
    # Convertimos de BGR a HSV
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Definimos los rangos de color en HSV
    azul_bajo = np.array([100, 100, 20], np.uint8)
    azul_alto = np.array([125, 255, 255], np.uint8)

    amarillo_bajo = np.array([15, 100, 20], np.uint8)
    amarillo_alto = np.array([45, 255, 255], np.uint8)

    rojo_bajo1 = np.array([0, 100, 20], np.uint8)
    rojo_alto1 = np.array([5, 255, 255], np.uint8)
    rojo_bajo2 = np.array([175, 100, 20], np.uint8)
    rojo_alto2 = np.array([179, 255, 255], np.uint8)

    # Detectamos los colores en las máscaras
    mask_azul = cv2.inRange(frame_hsv, azul_bajo, azul_alto)
    mask_amarillo = cv2.inRange(frame_hsv, amarillo_bajo, amarillo_alto)
    mask_rojo1 = cv2.inRange(frame_hsv, rojo_bajo1, rojo_alto1)
    mask_rojo2 = cv2.inRange(frame_hsv, rojo_bajo2, rojo_alto2)
    mask_rojo = cv2.add(mask_rojo1, mask_rojo2)

    # Buscamos contornos y obtenemos el centro de cada objeto detectado
    colors = []
    contours, _ = cv2.findContours(mask_azul, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        area = cv2.contourArea(c)
        if area > 5000:
            M = cv2.moments(c)
            if M["m00"] == 0:
                M["m00"] = 1
            x = int(M["m10"] / M["m00"])
            y = int(M["m01"] / M["m00"])
            colors.append((frame[y, x, 0], frame[y, x, 1], frame[y, x, 2], 'azul'))

    contours, _ = cv2.findContours(mask_amarillo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        area = cv2.contourArea(c)
        if area > 5000:
            M = cv2.moments(c)
            if M["m00"] == 0:
                M["m00"] = 1
            x = int(M["m10"] / M["m00"])
            y = int(M["m01"] / M["m00"])
            colors.append((frame[y, x, 0], frame[y, x, 1], frame[y, x, 2], 'amarillo'))

    contours, _ = cv2.findContours(mask_rojo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        area = cv2.contourArea(c)
        if area > 5000:
            M = cv2.moments(c)
            if M["m00"] == 0:
                M["m00"] = 1
            x = int(M["m10"] / M["m00"])
            y = int(M["m01"] / M["m00"])
            colors.append((frame[y, x, 0], frame[y, x, 1], frame[y, x, 2], 'rojo'))

    return colors

# Definimos el puerto de la cámara a emplear
cap = cv2.VideoCapture(0)

# Mientras está activada la captura de video
while True:
    # Obtenemos un valor booleano e imagen
    ret, frame = cap.read()

    # Si hay imagen capturada
    if ret == True:
        # Detectamos colores y obtenemos RGB
        detected_colors = detect_colors(frame)
        
        # Imprimimos los colores detectados en RGB
        for color in detected_colors:
            print(f"Color {color[3]}: R={color[0]}, G={color[1]}, B={color[2]}")

        # Detenemos la visualización con la tecla 's'
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break

# Detenemos la captura de video
cap.release()
# Cerramos todas las ventanas
cv2.destroyAllWindows()
