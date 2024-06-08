# nombre del archivo: color_detection.py

import picamera
import picamera.array
import cv2
import numpy as np

def detectar_color(frame):
    R_bajo = np.array([175, 126, 68])
    R_alto = np.array([176, 212, 255])
    V_bajo = np.array([62, 147, 49])
    V_alto = np.array([65, 156, 255])
    M_bajo = np.array([138, 87, 25])
    M_alto = np.array([167, 185, 255])

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_r = cv2.inRange(hsv, R_bajo, R_alto)
    mask_v = cv2.inRange(hsv, V_bajo, V_alto)
    mask_m = cv2.inRange(hsv, M_bajo, M_alto)
    
    # Mostrar las imágenes binarias de cada color
    print("Mascara Roja:")
    print(mask_r)
    print("Mascara Verde:")
    print(mask_v)
    print("Mascara Magenta:")
    print(mask_m)
    
    # Calcular el centroide para cada color
    cr = calcular_centroide(mask_r)
    cv = calcular_centroide(mask_v)
    cm = calcular_centroide(mask_m)
    
    return cr, cv, cm

def calcular_centroide(mask):
    M = cv2.moments(mask)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        return cX, cY
    else:
        return None, None

def obtener_centroides(resolution=(640, 480)):
    with picamera.PiCamera() as camera:
        with picamera.array.PiRGBArray(camera) as stream:
            camera.resolution = resolution
            camera.start_preview()
            # Esperar un momento para que la cámara se estabilice
            camera.start_recording('/dev/null', format='h264', motion_output='/dev/null')
            camera.wait_recording(1)
            camera.stop_recording()
            
            while True:
                camera.capture(stream, 'bgr', use_video_port=True)
                frame = stream.array
                cr, cv, cm = detectar_color(frame)
                
                return cr, cv, cm
                
                stream.seek(0)
                stream.truncate()





def main():
    cr, cv, cm = obtener_centroides()
    print("Coordenadas del centroide Rojo:", cr)
    print("Coordenadas del centroide Verde:", cv)
    print("Coordenadas del centroide Magenta:", cm)

if __name__ == "__main__":
  try:  
    while True:
      main()
  except KeyboardInterrupt:
    pass
