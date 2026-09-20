# TP1 Sistemas de Computación: Índice GINI (Iteración 2)

Python + C + ensamblador x86-64 (System V AMD64 ABI).

## Qué hace

Igual que la iteración 1, pero la conversión float -> int (+1) la hace una
rutina en ensamblador (gini_asm) que recibe el dato *por el stack*.

Como en System V AMD64 los primeros 6 argumentos enteros van en registros
(rdi, rsi, rdx, rcx, r8, r9) y los floats van en xmm0, se usa este truco:

- C pasa 6 ceros dummy, que ocupan los 6 registros.
- El 7mo argumento son los 32 bits crudos del float, copiados con memcpy
  a un int32_t, así viaja como entero por el stack y no por xmm0.
- En ASM, después del prólogo, ese argumento queda en 0x10(%rbp).
- cvttss2si convierte a entero (trunca), se suma 1 y el resultado queda en %eax.

## Uso

bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

as --64 -g -o gini_asm.o gini_asm.s
gcc -g -O0 -shared -fPIC -o libgini.so gini.c gini_asm.o
python3 gini.py


## Demo en GDB (C puro)

bash
gcc -g -O0 -o gini_test main_gdb.c gini.c gini_asm.o
gdb ./gini_test

