import RPi.GPIO as GPIO

# Define los pines
servo_pin_direccion = 2
servo_pin_traccion = 3
button_pin = 9

# Define variables
TAvance = 12.5
TAtras = 2.5
GDer = 4.5
GIzq = 10.5
GCent = 7.5
valor_d = GCent
valor_t = TAvance
arrancar = False

# Configura los pines GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin_direccion, GPIO.OUT)
GPIO.setup(servo_pin_traccion, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Iniciar servos
pwm_d = GPIO.PWM(servo_pin_direccion, 50) # Frecuencia de PWM: 50Hz (estándar para servos)
pwm_t = GPIO.PWM(servo_pin_traccion, 50) # Frecuencia de PWM: 50Hz (estándar para servos)

while True:
    button_state = GPIO.input(button_pin)
    if button_state == GPIO.HIGH:
        print("Botón presionado")
        arrancar = True

    if button_state == GPIO.LOW and arrancar:
        v = 1
        arrancar = False

    try:
      if arrancar:
        valor_d = GCent
        valor_t = TAvance
        pwm_d.start(valor_d)
        pwm_t.start(valor_t)
    except KeyboardInterrupt:
        GPIO.cleanup()
    except:
        pass
