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
    res_r = cv2.bitwise_and(frame, frame, mask=mask_r)
    res_v = cv2.bitwise_and(frame, frame, mask=mask_v)
    res_m = cv2.bitwise_and(frame, frame, mask=mask_m)

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
            camera.capture(stream, 'bgr')
            frame = stream.array

            cr, cv, cm = detectar_color(frame)
            
            camera.stop_preview()
            
    return cr, cv, cm




def main():
    cr, cv, cm = color_detection.obtener_centroides()
    print("Coordenadas del centroide Rojo:", cr)
    print("Coordenadas del centroide Verde:", cv)
    print("Coordenadas del centroide Magenta:", cm)

if __name__ == "__main__":
  try:  
    while True:
      main()
  except KeyboardInterrupt:
    pass
