import tcs34725 as tcs

while True:
  r, g, b, c = tcs.read_color()
  if r > b and r > g and r > 100:
    print("NARANJA")
  elif b > r and b > g and b > 100:
    print("AZUL")
  elif b > 100 and g > 100 and r > 100:
    print("GRIS")
  else:
    print("---")
  print(f"r = {r}, g = {g}", b = {b}, c = {c})
