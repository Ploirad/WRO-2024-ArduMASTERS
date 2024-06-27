import RPi.GPIO as GPIO

# Inicializa la librería GPIO
GPIO.setmode(GPIO.BCM)

# Define los pines del motor
ENA = 26
IN1 = 19
IN2 = 13
IN3 = 6
IN4 = 5
ENB = 27
cicloTrabajo = 0
frecuencia = 1000

# Configura los pines del motor como salida
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

# Configura PWM en los pines ENA y ENB
pwmENA = GPIO.PWM(ENA, frecuencia)
pwmENB = GPIO.PWM(ENB, frecuencia)

# Inicializa PWM con un ciclo de trabajo de 0%
pwmENA.start(cicloTrabajo)
pwmENB.start(cicloTrabajo)

Direccion = GPIO.PWM(18, 50)

# Define la función de movimiento
# Ambos valores (percent_vel y percent_dir) van de -100% a 100%
def move(percent_vel, percent_dir):
    d = ((0.7 * pow((percent_dir/100), 2)) - (5 * (percent_dir/100)) + 6.8) # Fórmula que se debe cambiar según cual sea el centro
    Direccion.start(d)

    if percent_vel > 0:
        print("AVANCE")
        duty_cycle = percent_vel
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
        pwmENA.ChangeDutyCycle(duty_cycle)
        pwmENB.ChangeDutyCycle(duty_cycle)
    elif percent_vel < 0:
        print("RETROCESO")
        duty_cycle = abs(percent_vel)
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
        pwmENA.ChangeDutyCycle(duty_cycle)
        pwmENB.ChangeDutyCycle(duty_cycle)
    else:
        print("STOP")
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.LOW)
        pwmENA.ChangeDutyCycle(0)
        pwmENB.ChangeDutyCycle(0)