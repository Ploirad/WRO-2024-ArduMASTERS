import cv2

# Abre la cámara
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


# Verifica si la cámara se ha abierto correctamente
if not cap.isOpened():
    print("Error al abrir la cámara")
    exit()

while True:
    # Lee un fotograma de la cámara
    ret, frame = cap.read()

    # Verifica si se ha leído correctamente el fotograma
    if not ret:
        print("Error al capturar el fotograma")
        break

    # Guarda el fotograma en el disco
    cv2.imwrite('captura.jpg', frame)

    # Sal del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera la cámara
cap.release()
