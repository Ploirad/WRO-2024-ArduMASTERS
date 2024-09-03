from Libraries import New_color_detector as cam
from picamera import PiCamera
from picamera.array import PiRGBArray
import json
import time
from Libraries import Boton
from Libraries import Extra_Functions as F
from Libraries import End_rounds as End
import tcs_Main as TCS_M

green_centroid = None
red_centroid = None
magenta_centroid = None
green_area = 0
red_area = 0
magenta_area = 0
camera = PiCamera()
camera.framerate = 30 #65
camera.resolution = (640, 480)
raw_capture = PiRGBArray(camera, size=(640, 480))
raw_capture.truncate(0)
extra_lap = False
can_start = False
waiting_magenta = False
possible_changing_direction = False
last_pillar = ""
tcs_color = ""
first_front_distance = 0
first_right_distance = 0
first_loop_done = False
second_round = False
tim = 1.5
print("variables inizialiced")

def main_logic(areas):
    max_area = max(areas, key=areas.get)

    tract = 100
    direction = 0
    ignore = True
    if max_area == "green" and areas[max_area] > 0:
        direction = 100
        ignore = False
    elif max_area == "red" and areas[max_area] > 3000:
        direction = -100
        ignore = False
    elif max_area == "magenta" and areas[max_area] > 1000:
        ignore = False

    return tract, direction, max_area, ignore

park = False
for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    image = frame.array
    height, width = image.shape[:2]
    lower_half = image[height//2:, :]
    _, green_area = cam.detect_green(lower_half)
    _, red_area = cam.detect_red(lower_half)
    magenta_centroid, magenta_area = cam.detect_magenta(lower_half)

    color_areas = {"green": green_area, "red": red_area, "magenta": magenta_area}

    t, d, color, ignore = main_logic(color_areas)
    
    if color == "magenta":
        park = True
    else:
        park = False

    CAM = {
            "Ignore": ignore,
            "Color": color,
            "Parking": park,
            "TRACTION": t,
            "DIRECTION": d,
            "MagentaC": magenta_centroid,
            "GArea": green_area,
            "RArea": red_area,
            "MArea": magenta_area
        }

    try:
        if can_start:
            if not first_loop_done:
                with open("Libraries/Json/Distance.json", "r", encoding='utf-8') as f:
                    Move = json.load(f)
                    first_front_distance = Move["HC0"]
                    first_right_distance = Move["HC1"]
                first_loop_done = True

            traction = 0
            direction = 0

            if (color == "red" or color == "green" or color == "magenta") and not ignore:
                second_round = True

            if second_round and possible_changing_direction and not ignore:
                last_pillar = color

            if waiting_magenta:
                if second_round:
                    if color == "magenta":
                        End.parking()
                else:
                    if tcs_color == "Gray":
                        End.home_sweet_home(first_front_distance, first_right_distance)
                        break

            if ("TRACTION" in CAM and "DIRECTION" in CAM) and not CAM["Ignore"]:
                traction = int(CAM["TRACTION"])
                direction = int(CAM["DIRECTION"])
            
            else:
                if CAM["Ignore"]:
                    print("Ignore CAM")
                    with open("Libraries/Json/Move.json", "r", encoding='utf-8') as f:
                        Move = json.load(f)
                        print(Move)

                        if "TRACTION" in Move and "DIRECTION" in Move:
                            traction = int(Move["TRACTION"])
                            direction = int(Move["DIRECTION"])

                        else:
                            print("Invalid data format in JSON file")

            with open("Libraries/Json/tcs_color_detection.json", "r", encoding='utf-8') as f:
                tcs = json.load(f)
                print(tcs)

                laps = tcs["laps"]
                tcs_first_color = tcs["first_color_obteined"]
                turns = tcs["turns"]
                tcs_color = tcs["color_obteined"]

                if laps == 1 and turns == 3:
                    possible_changing_direction = True

                if tcs_first_color == tcs_color and possible_changing_direction:
                    if last_pillar == "red":
                        F.change_direction()
                    possible_changing_direction = False
                    TCS_M.extra_lap = True

                if laps >= 3:
                    print("OK")
                    waiting_magenta = True

            with open("Libraries/Json/Movement.json", "w", encoding='utf-8') as j:
                data_to_write = {"traccion": traction, "direccion": direction}
                json.dump(data_to_write, j, indent=4)


            if traction < 0:
                time.sleep(tim)

            print(CAM)

            with open("Libraries/Json/Movement.json", 'r') as jf:
                print(json.load(jf))

        else:
            print("Waiting for start signal")
            if Boton.button_state():
                can_start = True

    except FileNotFoundError:
        print("Move.json file not found. Make sure the file exists.")
    except json.JSONDecodeError:
        print("Error decoding JSON. Ensure the JSON format is correct.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    raw_capture.truncate(0)
