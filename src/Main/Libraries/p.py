import cv2

# Abre la cámara
cap = cv2.VideoCapture(0)

while True:
    # Lee un fotograma de la cámara
    ret, frame = cap.read()

    # Muestra el fotograma en una ventana
    cv2.imshow('Camera', frame)

    # Espera a que se presione la tecla 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera la cámara y cierra todas las ventanas
cap.release()
cv2.destroyAllWindows()
