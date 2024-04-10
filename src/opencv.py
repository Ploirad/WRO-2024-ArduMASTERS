import picamera2
import time
import numpy as np

# Initialize the camera
camera = picamera2.PiCamera()

# Set the camera configuration
config = picamera2.PreviewDefinition(width=1920, height=1080, format='RGB888')
camera.configure(config)

# Start the camera preview
camera.start()

# Allow the camera to warm up
time.sleep(2)

# Capture an image
image = camera.capture_array()

# Stop the camera preview
camera.stop()

# Convert the image data to a NumPy array
img_data = np.array(image)

# Reshape the image data into a height x width x 3 array
img_data = img_data.reshape((1080, 1920, 3))

# Print the RGB values of the first 10 pixels
for i in range(10):
    r, g, b = img_data[i, i]
    print(f'RGB: {r}, {g}, {b}')
