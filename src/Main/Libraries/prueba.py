import Ultrasonidos as HC
import Motor as M

v = int(input("V (-1, 0, 1): "))
d = int(input("D (-1, 0, 1): "))
s = int(input("S (0, 1): "))

while True:
  D1 = HC.measure_distance(1)
  D2 = HC.measure_distance(2)
  D3 = HC.measure_distance(3)
  D4 = HC.measure_distance(4)
  print(f"D1={D1}; D2={D2}; D3={D3}; D4={D4}")
  M.movimiento(v, d, s)
