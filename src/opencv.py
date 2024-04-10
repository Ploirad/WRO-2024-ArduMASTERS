import cv2
import numpy as np

# Definimos una función para detectar colores y graficar contornos
def draw(mask, color):
    contornos,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for c in contornos:
        area = cv2.contourArea(c)
        
        # Si el área de interés es mayor a
        if area > 5000:    
            M = cv2.moments(c)
            if (M["m00"] == 0):
                M["m00"] = 1
                
            x = int(M["m10"]/M["m00"])
            y = int(M["m01"]/M["m00"])
            
            #--- Dibujamos los contornos seleccionados ---
            newContorno = cv2.convexHull(c)
             
            #--- Dibujamos un punto de r=7 y color verde ---
            cv2.circle(frame, (x, y), 7, (0, 255, 0), -1)
                                 
            # Puntos, ubicación, fuente, grosor, color, tamaño
            cv2.putText(frame, '{}, {}'.format(x, y), (x+10, y), font, 0.75, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.drawContours(frame, [newContorno], 0, color, 3)

# Definimos el puerto de la cámara a emplear         
cap = cv2.VideoCapture(0)

# Máscara de colores a detectar
azulBajo = np.array([100, 100, 20], np.uint8)
azulAlto = np.array([125, 255, 255], np.uint8)

amarilloBajo = np.array([15, 100, 20], np.uint8)
amarilloAlto = np.array([45, 255, 255], np.uint8)

rojoBajo1 = np.array([0, 100, 20], np.uint8)
rojoAlto1 = np.array([5, 255, 255], np.uint8)

rojoBajo2 = np.array([175, 100, 20], np.uint8)
rojoAlto2 = np.array([179, 255, 255], np.uint8)

# Mientras está activada la captura de video
while True:
    # Obtenemos un valor booleano e imagen
    ret, frame = cap.read()

    # Si hay imagen capturada
    if ret == True:

        # Pasamos de BGR a HSV
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        maskAzul = cv2.inRange(frameHSV, azulBajo, azulAlto)

        maskAmarillo = cv2.inRange(frameHSV, amarilloBajo, amarilloAlto)
        
        maskRojo1 = cv2.inRange(frameHSV, rojoBajo1, rojoAlto1)
        maskRojo2 = cv2.inRange(frameHSV, rojoBajo2, rojoAlto2)
        maskRojo = cv2.add(maskRojo1, maskRojo2)
        
        draw(maskAzul, (255, 0, 0))
        draw(maskAmarillo, (0, 255, 255))
        draw(maskRojo, (0, 0, 255))
        
        # Mostramos la ventana de captura
        cv2.imshow('Captura de video', frame)
        
        # Detenemos la visualización con la tecla 's'
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break

# Detenemos la captura de video
cap.release()
# Cerramos todas las ventanas
cv2.destroyAllWindows()
