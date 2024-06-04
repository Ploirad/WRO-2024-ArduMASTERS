import numpy as np
import picamera

# Capture an image using the Picamera
camera = picamera.PiCamera()
camera.capture('image.jpg')

# Load the image
image = np.array(camera.capture('image.jpg'))

# Define the color ranges
lower_red = np.array([175, 126, 68])
upper_red = np.array([176, 212, 255])

lower_green = np.array([62, 147, 49])
upper_green = np.array([65, 156, 255])

lower_magenta = np.array([138, 87, 25])
upper_magenta = np.array([167, 185, 255])

# Initialize lists to store the positions of each color
red_positions = []
green_positions = []
magenta_positions = []

# Iterate over the pixels in the image
for i in range(image.shape[0]):
    for j in range(image.shape[1]):
        pixel = image[i, j]
        if (lower_red <= pixel).all() and (pixel <= upper_red).all():
            red_positions.append((i, j))
        elif (lower_green <= pixel).all() and (pixel <= upper_green).all():
            green_positions.append((i, j))
        elif (lower_magenta <= pixel).all() and (pixel <= upper_magenta).all():
            magenta_positions.append((i, j))

# Calculate the centroid of each list of positions
def calculate_centroid(positions):
    if len(positions) == 0:
        return None
    else:
        return np.mean(positions, axis=0)

centroid_red = calculate_centroid(red_positions)
centroid_green = calculate_centroid(green_positions)
centroid_magenta = calculate_centroid(magenta_positions)

print("Centroid of Red:", centroid_red)
print("Centroid of Green:", centroid_green)
print("Centroid of Magenta:", centroid_magenta)
