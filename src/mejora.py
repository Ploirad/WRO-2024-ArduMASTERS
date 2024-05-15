import RPi.GPIO as GPIO
import time
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2
import numpy as np

GPIO.setmode(GPIO.BCM)

class Robot:
    def __init__(self):
        self.TRIG_PIN_DELANTE = 23
        self.ECHO_PIN_DELANTE = 24
        self.TRIG_PIN_ATRAS = 17
        self.ECHO_PIN_ATRAS = 27
        self.TRIG_PIN_IZQUIERDA = 22
        self.ECHO_PIN_IZQUIERDA = 10
        self.TRIG_PIN_DERECHA = 5
        self.ECHO_PIN_DERECHA = 6
        self.SERVO_PIN_DIRECCION = 2
        self.SERVO_PIN_TRACCION = 3
        self.BUTTON_PIN = 9
        self.IRSENSOR_PIN = 8

        self.SERVO_FREQ = 50

        self.DISTANCIA_DE_ACCION = {"MENOR QUE": 25, "MAYOR QUE": 24}

        self.BAJO_R, self.ALTO_R = np.array([174, 175, 138]), np.array([176, 212, 163])
        self.BAJO_G, self.ALTO_G = np.array([57, 104, 114]), np.array([65, 156, 140])
        self.BAJO_M, self.ALTO_M = np.array([164, 148, 134]), np.array([167, 185, 168])

        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.raw_capture = PiRGBArray(self.camera, size=(640, 480))

        self.pwm_d = GPIO.PWM(self.SERVO_PIN_DIRECCION, self.SERVO_FREQ)
        self.pwm_t = GPIO.PWM(self.SERVO_PIN_TRACCION, self.SERVO_FREQ)

    def get_distance(self, trig_pin: int, echo_pin: int) -> float:
        """Get the distance from the ultrasonic sensor"""
        # Send a pulse to the trig pin
        GPIO.output(trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(trig_pin, False)
        pulse_end = 0
        pulse_start = 0
        while GPIO.input(echo_pin) == 0:
            pulse_start = time.time()
        while GPIO.input(echo_pin) == 1:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 3)
        return distance

    def update_distances(self):
        """Update the distances from the ultrasonic sensors"""
        self.distancia_delante = self.get_distance(self.TRIG_PIN_DELANTE, self.ECHO_PIN_DELANTE)
        self.distancia_atras = self.get_distance(self.TRIG_PIN_ATRAS, self.ECHO_PIN_ATRAS)
        self.distancia_izquierda = self.get_distance(self.TRIG_PIN_IZQUIERDA, self.ECHO_PIN_IZQUIERDA)
        self.distancia_derecha = self.get_distance(self.TRIG_PIN_DERECHA, self.ECHO_PIN_DERECHA)

    def giro_linea(self, valor_t: float, valor_d: float):
        """Turn the robot"""
        print("girando...")
        self.pwm_t.start(valor_t)
        self.pwm_d.start(valor_d)
        time.sleep(1)
        self.pwm_t.start(valor_t)
        self.pwm_d.start(GCent)

    def giro_tras(self, valor_t: float, valor_d: float):
        """Reverse the robot and turn it"""
        valor_t = TAtras
        if valor_d == GIzq:
            valor_d = GDer
        elif valor_d == GDer:
            valor_d = GIzq
        else:
            valor_d = GCent
        self.pwm_t.start(valor_t)
        self.pwm_d.start(valor_d)
        time.sleep(2)
        valor_t = TAvance
        if valor_d == GIzq:
            valor_d = GDer
        elif valor_d == GDer:
            valor_d = GIzq
        else:
            valor_d = GCent
        self.pwm_t.start(valor_t)
        self.pwm_d.start(valor_d)
        time.sleep(2)
        valor_t = TAvance
        valor_d = GCent
        self.pwm_t.start(valor_t)
        self.pwm_d.start(valor_d)

    def detect_color(self, frame: np.ndarray) -> (np.ndarray, np.ndarray, int, int, int, int):
        """Detect the color of the object in front of the robot"""
        frame2 = frame.copy()
        frameHSV = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
        mask1 = cv2.inRange(frameHSV, self.BAJO_R, self.ALTO_R)
        mask2 = cv2.inRange(frameHSV, self.BAJO_G, self.ALTO_G)
        mask3 = cv2.inRange(frameHSV, self.BAJO_M, self.ALTO_M)
        mask = cv2.bitwise_or(mask1, cv2.bitwise_or(mask2, mask3))
        cx, cy, w, h = cv2.boundingRect(mask)
        frame2[mask == 255] = (355, 83, 93)
        cv2.circle(frame2, (cx, cy), 5, (0, 0, 255), -1)
        return frame2, mask, cx, cy, w, h

    def run(self):
        """Run the robot"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SERVO_PIN_DIRECCION, GPIO.OUT)
        GPIO.setup(self.SERVO_PIN_TRACCION, GPIO.OUT)
        GPIO.setup(self.TRIG_PIN_DELANTE, GPIO.OUT)
        GPIO.setup(self.ECHO_PIN_DELANTE, GPIO.IN)
        GPIO.setup(self.TRIG_PIN_ATRAS, GPIO.OUT)
        GPIO.setup(self.ECHO_PIN_ATRAS, GPIO.IN)
        GPIO.setup(self.TRIG_PIN_IZQUIERDA, GPIO.OUT)
        GPIO.setup(self.ECHO_PIN_IZQUIERDA, GPIO.IN)
        GPIO.setup(self.TRIG_PIN_DERECHA, GPIO.OUT)
        GPIO.setup(self.ECHO_PIN_DERECHA, GPIO.IN)
        GPIO.setup(self.BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.IRSENSOR_PIN, GPIO.IN)

        self.pwm_d.start(GCent)
        self.pwm_t.start(TAvance)

        try:
            while True:
                button_state = GPIO.input(self.BUTTON_PIN)
                if button_state == GPIO.HIGH:
                    print("Botón presionado")
                    self.v = 1
                if self.v == 1:
                    self.update_distances()
                    if self.distancia_delante < self.DISTANCIA_DE_ACCION["MENOR QUE"]:
                        self.giro_tras(TAtras, GCent)
                    elif self.distancia_delante > self.DISTANCIA_DE_ACCION["MAYOR QUE"]:
                        self.giro_tras(TAvance, GCent)
                    else:
                        self.giro_tras(TAvance, GCent)
                        frame = self.camera.capture(self.raw_capture, format="bgr", use_video_port=True)
                        self.raw_capture.truncate(0)
                        frame = np.frombuffer(frame.tobytes(), dtype=np.uint8)
                        frame = np.reshape(frame, (480, 640, 3))
                        frame, mask, cx, cy, w, h = self.detect_color(frame)
                        if cx > 0 and cy > 0 and w > 0 and h > 0:
                            if cx < 320:
                                self.giro_linea(TAvance, GIzq)
                            elif cx > 320:
                                self.giro_linea(TAvance, GDer)
                            else:
                                self.giro_linea(TAvance, GCent)
                        else:
                            self.giro_linea(TAvance, GCent)
                else:
                    self.pwm_t.start(TAvance)
                    self.pwm_d.start(GCent)
                    time.sleep(1)
                    self.pwm_t.stop()
                    self.pwm_d.stop()
                    GPIO.cleanup()
                    break
        except KeyboardInterrupt:
            self.pwm_t.stop()
            self.pwm_d.stop()
            GPIO.cleanup()

if __name__ == "__main__":
    robot = Robot()
    robot.run()
