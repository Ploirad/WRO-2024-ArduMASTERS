import time
import picamera2

with picamera2. Picamera2() as camera:
    camera.start()
    time.sleep(5) 
    camera.stop_recording() 
    camera.stop_preview()