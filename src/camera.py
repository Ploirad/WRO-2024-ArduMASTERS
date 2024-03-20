import time
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder

def record_video(): 
    with Picamera2() as picam2: 
        picam2.resolution = (640, 480) 
        picam2.framerate = 3 
        preview = picam2.create_video_preview() 
        picam2.start_preview(preview) 
        encoder = H264Encoder() 
        picam2.start_recording(encoder, 'output.h264') 
        time.sleep(5) 
        picam2.stop_recording() 
        picam2.stop_preview()
if  __name__ == "__main__":
    try:
        record_video()
    except KeyboardInterrupt:
        print("Stopping recording...")