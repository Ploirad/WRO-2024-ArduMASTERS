import cv2
import serial
import numpy as np

ser = serial.Serial('/dev/ttyACM0', 9600)

def detectar_color(frame):
	#1ro = oscuro y el 2do = claro
	rangos_colores = {
		'rojo':  [(0, 0, 145), (84, 84, 255)],
		'azul': [(112, 0, 0), (255, 232, 150)],
		'verde': [(0, 115, 0), (118, 255, 157)],
		'amarillo': [(20, 100, 100), (30, 255, 255)],
	}
	for color, (lower, upper) in rangos_colores.items():
		lower = np.array(lower, dtype=np.uint8)
		upper = np.array(upper, dtype=np.uint8)

		mask = cv2.inRange(frame, lower, upper)
		if cv2.countNonZero(mask) > 1000:
			return color
	return None

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

while True:
	ret, frame = cap.read()

	color_detectado = detectar_color(frame)

	if color_detectado:
		print(f"color detectado: {color_detectado}")
		ser.write(str(color_detectado).encode())

	if color_detectado == "rojo":
		ser.write(b'1')
	if color_detectado == "azul":
		ser.write(b'2')
	if color_detectado == "verde":
		ser.write(b'3')
	if color_detectado == "amarillo":
		ser.write(b'4')

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
