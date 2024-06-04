import cv2
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
import time

# Define los rangos de color en HSV
lower_red = np.array([175, 126, 68])
upper_red = np.array([176, 212, 255])
lower_green = np.array([62, 147, 49])
upper_green = np.array([65, 156, 255])
lower_magenta = np.array([138, 87, 25])
upper_magenta = np.array([167, 185, 255])

def find_centroid(mask):
    # Encuentra los contornos en la máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        # Calcula el momento del contorno
        M = cv2.moments(contour)
        if M["m00"] != 0:
            # Calcula las coordenadas del centroide
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            return (cX, cY)
    return None

def process_frame(frame):
    # Convierte la imagen a espacio de color HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Detecta los colores
    masks = {
        "red": cv2.inRange(hsv, lower_red, upper_red),
        "green": cv2.inRange(hsv, lower_green, upper_green),
        "magenta": cv2.inRange(hsv, lower_magenta, upper_magenta)
    }
    
    centroids = {}
    for color, mask in masks.items():
        centroid = find_centroid(mask)
        if centroid:
            centroids[color] = centroid
            # Dibuja el centroide en la imagen
            cv2.circle(frame, centroid, 5, (0, 255, 0), -1)
            cv2.putText(frame, color, (centroid[0] - 25, centroid[1] - 25), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    return frame, centroids

def main():
    # Inicializa la cámara
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))
    
    time.sleep(0.1)  # Deja que la cámara se inicialice

    # Captura de imágenes continuamente
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        
        # Procesa la imagen
        processed_frame, centroids = process_frame(image)
        
        # Guarda la imagen procesada
        cv2.imwrite('processed_image.jpg', processed_frame)
        
        # Muestra la información de los centroides en la consola
        for color, centroid in centroids.items():
            print(f"Color: {color}, Centroide: {centroid}")
        
        # Limpia el buffer de la cámara para la siguiente imagen
        rawCapture.truncate(0)
        
        # Salida después de un número específico de frames o por una condición
        # Aquí simplemente se muestra un ejemplo con una pausa para no llenar la consola
        time.sleep(1)

if __name__ == "__main__":
    main()
