# This code is for execute the codes

# We import the libraries
import subprocess
import cv2

# We define the commands
cmd1 = "python3 Libraries/Movement.py"
cmd2 = "python3 MAIN.py"

# We execute the first command in background
proc1 = subprocess.run(cmd1, shell=True)

# Finnaly we execute the second command
proc2 = subprocess.run(cmd2, shell=True)

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break