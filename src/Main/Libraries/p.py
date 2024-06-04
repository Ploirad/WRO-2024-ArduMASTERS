import time
import picamera

# Inicializa la cámara
with picamera.PiCamera() as camera:
    # Captura una imagen
    camera.capture('captura.jpg')
