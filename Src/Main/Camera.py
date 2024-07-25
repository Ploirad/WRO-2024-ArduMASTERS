from Libraries import New_color_detector as CAM
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import threading
import signal
import sys
import json


green_centroid = None
red_centroid = None
magenta_centroid = None
green_area = 0
red_area = 0
magenta_area = 0
camera = CAM.camera
camera.framerate = 30 #65
camera.resolution = (640, 480)
raw_capture = PiRGBArray(camera, size=(640, 480))
raw_capture.truncate(0)
park = False

def principal_logic(areas, centroids):
    max_area = max(areas, key=areas.get)

    traction = 100
    direction = 0
    ignore = True
    if max_area == "green" and areas[max_area] > 1000:
        direction = 100
        ignore = False
    elif max_area == "red" and areas[max_area] > 550:
        direction = -100
        ignore = False

    return traction, direction, max_area, ignore

def detect(stop_event):
    while not stop_event.is_set():
        for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
            image = frame.array
            height, width = image.shape[:2]
            lower_half = image[height//2:, :]
            green_centroid, green_area = CAM.detect_green(lower_half)
            red_centroid, red_area = CAM.detect_red(lower_half)
            magenta_centroid, magenta_area = CAM.detect_magenta(lower_half)
        
            color_areas = {"green": green_area, "red": red_area, "magenta": magenta_area}
            color_centroids = {"green": green_centroid, "red": red_centroid, "magenta": magenta_centroid}

            t, d, color, ignore = principal_logic(color_areas, color_centroids)
            
            if color == "magenta":
                park = True

            data = {
                    "Ignore": ignore,
                    "Color": color,
                    "Parking": park,
                    "TRACTION": t,
                    "DIRECTION": d
                }
            raw_capture.truncate(0)
            
            with open("CAM.json", "w", encoding='utf-8') as j:
                json.dump(data, j, indent=4)

def signal_handler(sig, frame):
    global stop_event
    stop_event.set()

# Create and start the threads
threads = []
stop_event = threading.Event()
signal.signal(signal.SIGINT, signal_handler)

try:
    t = threading.Thread(target=detect, args=(stop_event,))
    t.start()
    threads.append(t)

    # Wait for the end of the threads (in this case it doesn't happen unless interrupted)
    for t in threads:
        t.join()

except Exception as e:
    print(f"Error: {e}")
finally:
    # Clean the GPIO at the end
    GPIO.cleanup()
