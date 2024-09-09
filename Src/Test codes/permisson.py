import os
import stat

# Ruta del archivo
file_1 = "../Main/Camera_Main.py"
info_1 = os.stat(file_1)

# Verificar permisos de lectura
if info_1.st_mode & stat.S_IRUSR:
    print("Tienes permisos de lectura")
else:
    print("No tienes permisos de lectura")

# Verificar permisos de escritura
if info_1.st_mode & stat.S_IWUSR:
    print("Tienes permisos de escritura")
else:
    print("No tienes permisos de escritura")

# Verificar permisos de ejecución
if info_1.st_mode & stat.S_IXUSR:
    print("Tienes permisos de ejecución")
else:
    print("No tienes permisos de ejecución")

file_2 = "../Main/Movement_Main.py"
info_2 = os.stat(file_2)

if info_1.st_mode & stat.S_IRUSR:
    print("Tienes permisos de lectura")
else:
    print("No tienes permisos de lectura")

# Verificar permisos de escritura
if info_2.st_mode & stat.S_IWUSR:
    print("Tienes permisos de escritura")
else:
    print("No tienes permisos de escritura")

# Verificar permisos de ejecución
if info_2.st_mode & stat.S_IXUSR:
    print("Tienes permisos de ejecución")
else:
    print("No tienes permisos de ejecución")

file_3 = "../Main/tcs_Main.py"
info_3 = os.stat(file_3)

if info_3.st_mode & stat.S_IRUSR:
    print("Tienes permisos de lectura")
else:
    print("No tienes permisos de lectura")

# Verificar permisos de escritura
if info_3.st_mode & stat.S_IWUSR:
    print("Tienes permisos de escritura")
else:
    print("No tienes permisos de escritura")

# Verificar permisos de ejecución
if info_3.st_mode & stat.S_IXUSR:
    print("Tienes permisos de ejecución")
else:
    print("No tienes permisos de ejecución")