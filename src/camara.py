import picamera

# Set up the camera
camera = picamera.PiCamera()
camera.resolution = (1024, 768)
camera.framerate = 30

# Set up the video recording
start_time = time.time()
output = '/home/pi/video.h264'
camera.start_recording(output, format='h264')

# Wait for 30 seconds
while time.time() - start_time < 30:
    pass

# Stop recording and release the camera
camera.stop_recording()
camera.release()
