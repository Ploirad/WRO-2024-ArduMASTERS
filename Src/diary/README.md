<p align="center">
  <img width="200" height="200" Src="https://github.com/Ploirad/WRO-2024-ArduMASTERS/assets/148375115/122c7233-1e41-4727-894d-9d810f12458b">
</p> 

# Files:
  - [Camera_color_detection_v1.0.0](#Camera_color_detection_v1.0.0.py)
  - [Camera_color_detection_v1.1.0](#Camera_color_detection_v1.1.0.py)
  - [Camera_color_detection_v1.1.1](#Camera_color_detection_v1.1.1.py)
  - [Camera_color_detection_v2.0.0](#Camera_color_detection_v2.0.0.py)
  - [Camera_color_extractor](#camera_color_extractor.py)
  - [Color_detector_with_movement](#camera_detector_with_movement.py)
  - [Engine](#engine.py)
  - [Servos_test_v1.0.0](#servos_test_v1.0.0.py)
  - [Servos_test_v1.1.0](#servos_test_v1.1.0.py)
  - [Ultrasound_v1.0.0](#ultrasound_v1.0.0.py)
  - [Ultrasound_v1.1.0](#ultrasound_v1.1.0.py)

## [Camera_color_detection_v1.0.0.py](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/Src/diary/camera_color_detection_v1.0.0.py)
This code is a library used to find the range of a color in an image and return another image with the color painted white as its center.

## [Camera_color_detection_v1.1.0.py](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/Src/diary/camera_color_detection_v1.1.0.py)
This code does the same thing as its [previous version](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/Src/diary/camera_color_detection_v1.0.0.py), but use a different way in order to calculate the center and its less modulated.

## [Camera_color_detection_v1.1.1.py](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/Src/diary/camera_color_detection_v1.1.1.py)
This code, unlike its [last version](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/Src/diary/camera_color_detection_v1.1.0.py), does everything in its own code and shows how it sees the different colors in real time.

## [Camera_color_detection_v2.0.0.py](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/Src/diary/camera_color_detection_v2.0.0.py)
This code is simpler than the [previous version](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/Src/diary/camera_color_detection_v1.1.1.py) and works with the computer's camera instead of the Raspberry Pi's.

## [camera_color_extractor.py](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/Src/diary/camera_color_extractor.py)
This code let us select a section of a camera, and it highlights evry part of the camera between these range.
>We had made it with HSV instead of RGB becouse with HSV we can detect the saturation and the tone.

## [Color_detector_with_movement.py](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/Src/diary/color_detector_with_movement.py)
That code is our first of combining the use of the motors and the camera.
>Its so raw that we don't consider it as a main code.

## [Engine.py](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/Src/diary/engine.py)
This code is a library that was used to control the motors of our car.

## [Servos_test_v1.0.0.py](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/Src/diary/servos_test_v1.0.0.py)
This code is in order to test the servos movement 

## [Servos_test_v1.1.0.py](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/Src/diary/servos_test_v1.1.0.py)
This code is the same than [its previous version](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/Src/diary/servos_test_v1.0.0.py), but we add a button.

## [Ultrasound_v1.0.0.py](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/Src/diary/ultrasound_v1.0.0.py)
That code is an ultrasound test.

## [Ultrasound_v1.1.0.py](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/Src/diary/ultrasound_v1.1.0.py)
This code its the same than its [previous version](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/Src/diary/ultrasound_v1.0.0.py) but everything its in a functions, making it as a library.