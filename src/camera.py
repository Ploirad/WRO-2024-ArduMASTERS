import time
import picamera2

with picamera2. Picamera2() as camera:
picamera2.start_and_record_video("test.mp4", duration=10)
