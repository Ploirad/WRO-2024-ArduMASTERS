# This code is a library for the camera to take the color centroid and area of a specific frame given

# Libraries
import cv2
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray

camera = PiCamera()

# This function is used to take the green centroid respect to the X edge and the green area all about the frame gived and they are integer variables
def detect_green(frame):
    G_bajo = np.array([76, 171, 130])  # HSV values for green
    G_alto = np.array([80, 255, 176])
    return detect_color(frame, G_bajo, G_alto)

def detect_red(frame):
    R_bajo = np.array([154, 101, 24])  # HSV values for red
    R_alto = np.array([177, 255, 184])
    return detect_color(frame, R_bajo, R_alto)

def detect_magenta(frame):
    M_bajo = np.array([142, 117, 49])  # HSV values for magenta
    M_alto = np.array([150, 230, 208])
    return detect_color(frame, M_bajo, M_alto)

# This function is used to take the centroid and the area of the color gived (color_low, color_high) in the respective frame
def detect_color(frame, color_low, color_high):
    # Convert the frame from BGR to HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask for the specified color range in HSV
    mask = cv2.inRange(hsv_frame, color_low, color_high)

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