#!/usr/bin/env python3


import webbrowser
import random
import os


script_dir = os.path.dirname(os.path.abspath(__file__))
ruta_enlaces = os.path.join(script_dir,"enlaces.txt")

try:
    with open(ruta_enlaces, "r") as f:
        lineas = f.readlines()

    if lineas:
        url = random.choice(lineas).strip()
        webbrowser.open(url)
    else:
        print('No hay URLs en el archivo seleccionado')
except Exception as e:
    print("Error: ",e)