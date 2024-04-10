import picamera2
import time
import numpy as np

# Initialize the camera
camera = picamera2.PiCamera2()

# Set the camera resolution
camera.sensor_mode = 'mode_1080p'

# Start the camera preview
camera.start_preview()

# Allow the camera to warm up
time.sleep(2)

# Capture an image
img = camera.capture()

# Stop the camera preview
camera.stop_preview()

# Convert the image data to a NumPy array
img_data = np.array(img.data)

# Reshape the image data into a height x width x 3 array
img_data = img_data.reshape((1080, 1920, 3))

# Print the RGB values of the first 10 pixels
for i in range(10):
    r, g, b = img_data[i, i]
    print(f'RGB: {r}, {g}, {b}')
