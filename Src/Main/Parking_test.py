import Libraries.End_rounds as ER
import json

while True:
  with open ("Libraries/Json/CAM.json", "r", encoding = "utf-8") as d:
    data = json.load(d)
    M = data["MagentaC"]
    if M != None:
      ER.parking(False)
      Break
