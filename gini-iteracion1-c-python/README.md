# TP1 Sistemas de Computación: Índice GINI (Iteración 1)

Python + C, sin ensamblador.

## Qué hace

1. gini.py consulta la API del Banco Mundial (indicador SI.POV.GINI, Argentina)
   y se queda con el último año que tenga dato (algunos vienen en null).
2. Le pasa el valor (float) a gini_mas_uno(), en C, mediante ctypes.
3. gini_mas_uno() trunca el float a entero y le suma 1 (42.7 -> 42 -> 43).
4. Python imprime el resultado.

## Uso

bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
gcc -g -O0 -shared -fPIC -o libgini.so gini.c
python3 gini.py


Salida esperada (el año y el valor dependen del último dato publicado):


GINI Argentina 2020: 42.7 -> 43
