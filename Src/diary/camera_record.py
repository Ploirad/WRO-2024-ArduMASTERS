import picamera
from time import sleep

# Inicializa la cámara
camera = picamera.PiCamera()

# Inicia la vista previa en directo en la pantalla
camera.start_preview()

# Inicia la grabación de video en directo y guarda el archivo como "video_en_vivo.h264"
camera.start_recording('video_en_vivo.h264')

# Espera durante 30 segundos mientras se graba el video en directo
sleep(30)

# Detiene la grabación y la vista previa en directo
camera.stop_recording()
camera.stop_preview()

# Libera los recursos de la cámara
camera.close()
