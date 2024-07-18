# This code is for execute the codes

# We import the libraries
from Libraries.External_Libraries import *

# We define the commands
cmd1 = "python3 Libraries/Write_with_UltraSonic_sensors.py"
cmd2 = "python3 MAIN.py"

# We execute the first command in background
proc1 = subprocess.Popen(cmd1, shell=True)

# Finnaly we execute the second command
proc2 = subprocess.run(cmd2, shell=True)
