import Libraries.End_rounds as ER
import json

while True:
  with open ("Libraries/Json/CAM.json", "r", encoding = "utf-8") as d:
    data = json.load(d)
    M = d["MagentaC"]
    if M == not None:
      ER.parking(False)
