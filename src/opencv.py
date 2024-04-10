from picamera import PiCamera
from time import sleep

# Initialize the camera
camera = PiCamera()

# Start the camera preview
camera.start_preview()

# Allow the camera to warm up
sleep(2)

# Capture an image
camera.capture('/home/pi/image.jpg')

# Stop the camera preview
camera.stop_preview()

# Open the image file
with open('/home/pi/image.jpg', 'rb') as f:
    img = f.read()

# Decode the image data
img_data = np.frombuffer(img, dtype=np.uint8)

# Reshape the image data into a height x width x 3 array
img_data = img_data.reshape((480, 640, 3))

# Print the RGB values of the first 10 pixels
for i in range(10):
    r, g, b = img_data[i, i]
    print(f'RGB: {r}, {g}, {b}')
