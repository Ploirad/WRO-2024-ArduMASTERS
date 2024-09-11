import Libraries.End_rounds as ER
import json
import os
import time

while True:
  with open(os.path.join(os.path.dirname(__file__), "Libraries", "Json", "CAM.json"), "r", encoding = "utf-8") as d:
    data = json.load(d)
    M = data["MagentaC"]
    print(M)
  if M != None:
    print("Imma park")
    ER.parking(False)
    break
  time.sleep(0.1)  
