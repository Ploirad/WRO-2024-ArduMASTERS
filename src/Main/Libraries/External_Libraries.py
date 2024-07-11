# There we have all the libraries of the car codes

# General Libraries
import time
import RPi.GPIO as GPIO

# MAIN.py, parking.py and some of the New_Color_Detector.py Libraries
from picamera import PiCamera
from picamera.array import PiRGBArray

# The rest of the New_Color_Detector.py Libraries
import cv2
import numpy as np

# Tsc34725.py Libraries
import adafruit_tcs34725
import busio
import board

# Threading.py Libraries
import threading