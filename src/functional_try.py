import cv2
#import serial
import numpy as np

#ser = serial.Serial('/dev/ttyACM0', 9600)

def detectar_color(frame):
	#1ro = oscuro y el 2do = claro
	rangos_colores = {
		'poste_verde': [(37, 179, 57), (52, 255, 81)], #BGR  44, 214, 68
		'poste_rojo': [(54, 38, 235), (59, 42, 255)], #BGR  55, 39, 238
		'pared_magenta': [(255, 0, 255), (224, 0, 224)], #BGR  255, 0, 255
		'linea_naranja': [(0, 102, 255), (0, 94, 235)], #BGR  0, 102, 255
		'linea_azul': [(255, 51, 0), (199, 40, 0)], #BGR  255, 51, 0
		'linea_gris_contorno_de_aparcamiento': [(217, 217, 217), (163, 163, 163)], #BGR  179, 179, 179
		}
	for color, (lower, upper) in rangos_colores.items():
		lower = np.array(lower, dtype=np.uint8)
		upper = np.array(upper, dtype=np.uint8)

		#frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(frame, lower, upper)
		#mask = np.all(np.logical_and(frame_hsv >= lower, frame_hsv <= upper), axis=-1)
		if cv2.countNonZero(mask) > 1000:
			return color
	return None

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

while True:
	ret, frame = cap.read()

	color_detectado = detectar_color(frame)

	if color_detectado:
		print("color detectado: {}".format(color_detectado))
	#	ser.write(str(color_detectado).encode())

	#if color_detectado == "rojo":
	#	ser.write(b'1')

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
