#!/usr/bin/python3
import time

from picamera2 import Picamera2
from picamera2.encoders import Encoder

picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)

encoder = Encoder()

picam2.start_recording(encoder,'test.mp4')
time.sleep(10)
picam2.stop_recording()