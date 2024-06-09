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
    masks = {
        'red': cv2.inRange(hsv, R_bajo, R_alto),
        'green': cv2.inRange(hsv, V_bajo, V_alto),
        'magenta': cv2.inRange(hsv, M_bajo, M_alto)
    }
    
    areas = {color: cv2.countNonZero(mask) for color, mask in masks.items()}
    centroids = {color: calcular_centroide(mask) for color, mask in masks.items()}
    
    return areas['green'], areas['red'], areas['magenta'], centroids['green'], centroids['red'], centroids['magenta']


def calcular_centroide(mask):
    M = cv2.moments(mask)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        return cX, cY
    else:
        return None, None

def obtener_centroides(resolution=(320, 240)):
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
                green_area, red_area, magent_area, cv, cr, cm = detectar_color(frame)
                return green_area, red_area, magent_area, cv, cr, cm
