# This code is a library for the camera to take the color centroid and area of a specific frame given

# Libraries
from External_Libraries import *

camera = PiCamera()

#This function is used to take the green centroid respect to the X edge and the green area all about the frame gived and they are integer variables
def detect_green(frame):
    G_bajo = np.array([0, 110, 0])
    G_alto = np.array([100, 255, 100])
    return detect_color(frame, G_bajo, G_alto)

def detect_red(frame):
    R_bajo = np.array([150, 50, 50])
    R_alto = np.array([255, 200, 200])
    return detect_color(frame, R_bajo, R_alto)

def detect_magenta(frame):
    M_bajo = np.array([150, 0, 150])
    M_alto = np.array([255, 250, 255])
    return detect_color(frame, M_bajo, M_alto)

#This function is used to take the centroid and the area of the color gived (color_low, color_high) in the respective frame
def detect_color(frame, color_low, color_high):
    # Create a mask for the specified color range in RGB
    mask = cv2.inRange(frame, color_low, color_high)

    # Find contours in the mask
    _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # If no contours are found, return None
    if not contours:
        return None, 0

    # Find the largest contour
    largest_contour = max(contours, key=cv2.contourArea)

    # Compute the center and area of the largest contour
    M = cv2.moments(largest_contour)
    if M["m00"] == 0:
        return None, 0
    cX = int(M["m10"] / M["m00"])
    area = cv2.contourArea(largest_contour)

    return cX, area

def detect_dominant_color(frame):
    height, width, _ = frame.shape
    # Coordenadas del centro del cuadro
    center_x = width // 2
    center_y = height // 2
    # Color en el centro del cuadro
    center_color_bgr = frame[center_y, center_x]
    # Convertir de BGR a RGB
    center_color_rgb = center_color_bgr[::-1]
    return center_color_rgb


##Code to try the camera
#green_centroid = None
#red_centroid = None
#magenta_centroid = None
#green_area = 0
#red_area = 0
#magenta_area = 0
#camera.framerate = 30 #65
#camera.resolution = (640, 480)
#raw_capture = PiRGBArray(camera, size=(640, 480))
#
#raw_capture.truncate(0)
#for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
#    image = frame.array
#    height, width = image.shape[:2]
#    lower_half = image[height//2:, :]
#    green_centroid, green_area = detect_green(lower_half)
#    red_centroid, red_area = detect_red(lower_half)
#    magenta_centroid, magenta_area = detect_magenta(lower_half)
#    dom_col = detect_dominant_color(lower_half)
#    print(f"Green Area: {green_area}; Red Area: {red_area}; Magenta Area: {magenta_area}")
#    print(f"Green Centroid: {green_centroid}; Red Centroid: {red_centroid}; Magenta Centroid: {magenta_centroid}")
#    print(f"Dominante color: {dom_col}")
#    print("")
#    raw_capture.truncate(0)  # Limpiar el búfer para la siguiente captura