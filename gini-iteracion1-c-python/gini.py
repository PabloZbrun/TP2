import ctypes
import requests

URL = ("https://api.worldbank.org/v2/country/ARG/indicator/SI.POV.GINI"
       "?format=json&date=2011:2020&per_page=100")


def ultimo_gini(url):
    res = requests.get(url, timeout=10)
    res.raise_for_status()
    datos = res.json()[1]
    for d in datos:
        if d["value"] is not None:
            return d["date"], d["value"]
    return None, None


lib = ctypes.CDLL("./libgini.so")
lib.gini_mas_uno.argtypes = (ctypes.c_float,)
lib.gini_mas_uno.restype = ctypes.c_int

anio, valor = ultimo_gini(URL)
if valor is None:
    print("Sin datos")
else:
    resultado = lib.gini_mas_uno(valor)
    print(f"GINI Argentina {anio}: {valor} -> {resultado}")
