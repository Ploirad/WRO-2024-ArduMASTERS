# This code is for execute the codes

# We import the libraries
import subprocess
import cv2

# We define the commands
cmd1 = "python3 Movement.py"
cmd2 = "python3 Camera.py"
cmd3 = "python3 MAIN.py"

# We execute the first command in background
proc1 = subprocess.Popen(cmd1, shell=True)
proc2 = subprocess.Popen(cmd2, shell=True)

# Finnaly we execute the second command
proc3 = subprocess.run(cmd3, shell=True)

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break