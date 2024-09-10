import Libraries.End_rounds as ER
import json
import os

while True:
  with open (os.path.join(os.path.dirname(__file__), "Json", "CAM.json"), "r", encoding = "utf-8") as d:
    data = json.load(d)
    M = data["MagentaC"]
    if M != None:
      ER.parking(False)
      Break
