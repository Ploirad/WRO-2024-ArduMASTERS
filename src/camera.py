import time
import picamera2

with picamera2. Picamera2() as camera:
    camera.configure(picamera2.start_preview()(width=640, height=480))
    camera.start()
    time.sleep(5) 
    camera.stop_recording() 
    camera.stop_preview()