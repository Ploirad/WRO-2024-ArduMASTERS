import cv2
import numpy as np

# Variables globales para almacenar el punto seleccionado y la imagen
clicked_point = None
image = None

# Callback del mouse
def mouse_callback(event, x, y, flags, param):
    global clicked_point
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_point = (x, y)
        print(f"Color seleccionado en (x={x}, y={y})")

# Función para convertir el color BGR a HSV
def bgr_to_hsv(bgr_color):
    bgr_color = np.uint8([[bgr_color]])
    hsv_color = cv2.cvtColor(bgr_color, cv2.COLOR_BGR2HSV)
    return hsv_color[0][0]

# Cargar la imagen
image = cv2.imread('image.jpg')  # Cambia 'image.jpg' a la ruta de tu imagen
cv2.imshow('Image', image)
cv2.setMouseCallback('Image', mouse_callback)

while True:
    cv2.imshow('Image', image)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # Presiona 'q' para salir
        break
    if clicked_point:
        bgr_color = image[clicked_point[1], clicked_point[0]].tolist()
        hsv_color = bgr_to_hsv(bgr_color)
        print(f"Color BGR seleccionado: {bgr_color}")
        print(f"Color HSV correspondiente: {hsv_color}")
        
        # Rango de colores HSV
        lower_bound = np.array([hsv_color[0] - 10, 100, 100])
        upper_bound = np.array([hsv_color[0] + 10, 255, 255])

        # Convertir la imagen a HSV
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Crear una máscara con el rango de color seleccionado
        mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
        
        # Mostrar la máscara
        cv2.imshow('Mask', mask)

cv2.destroyAllWindows()
