# Sesión de GDB: stack de gini_asm(0,0,0,0,0,0, 0x422acccd)

Valor de prueba: 42.7. En float de 32 bits (IEEE 754) es 0x422acccd
(GDB lo muestra como 42.7000008 por la precisión del float).

## 0. Código de la llamada (disassemble gini_mas_uno)


sub    $0x8,%rsp        # relleno para alinear el stack a 16 bytes
push   %rax             # 7mo argumento (bits del float)
mov    $0x0,%r9d        # 6 ceros dummy: r9, r8, rcx, rdx, rsi, rdi
mov    $0x0,%r8d
mov    $0x0,%ecx
mov    $0x0,%edx
mov    $0x0,%esi
mov    $0x0,%edi
call   0x5555555551dc <gini_asm>      # en 0x5555555551cb
add    $0x10,%rsp       # el caller limpia el stack (8 de relleno + 8 del push)


## 1. ANTES: parada en el call (0x5555555551cb)


(gdb) x/8xg $rsp
0x7fffffffddf0:	0x00000000422acccd	0x0000000000000000
0x7fffffffde00:	0x0000000000000000	0x422acccd00000000
0x7fffffffde10:	0x0000000000000000	0x00000000422acccd
0x7fffffffde20:	0x00007fffffffde40	0x000055555555515a
(gdb) info registers rdi rsi rdx rcx r8 r9
(todos valen 0)


- [rsp] = 0x422acccd: el 7mo argumento (bits de 42.7), recién pusheado.
- [rsp+8] = 0: relleno de alineación (el sub $0x8,%rsp).
- Los 6 registros de argumentos valen 0 (los ceros dummy).

## 2. AL ENTRAR: primera instrucción de gini_asm (0x5555555551dc)


(gdb) x/8xg $rsp
0x7fffffffdde8:	0x00005555555551d0	0x00000000422acccd
0x7fffffffddf8:	0x0000000000000000	0x0000000000000000
...
(gdb) info registers rsp rbp
rsp            0x7fffffffdde8
rbp            0x7fffffffde20


- rsp bajó 8 bytes (...ddf0 -> ...dde8): el call apiló la dirección de retorno.
- [rsp] = 0x5555555551d0: dirección de retorno (el call está en ...51cb y mide 5 bytes).
- [rsp+8] = 0x422acccd: el argumento, ahora 8 bytes más arriba.
- rbp todavía es el de gini_mas_uno (el prólogo no se ejecutó).

## 3. DURANTE: después del prólogo (push %rbp + mov %rsp,%rbp)


(gdb) info registers rsp rbp
rsp            0x7fffffffdde0
rbp            0x7fffffffdde0
(gdb) x/6xg $rbp
0x7fffffffdde0:	0x00007fffffffde20	0x00005555555551d0
0x7fffffffddf0:	0x00000000422acccd	0x0000000000000000
0x7fffffffde00:	0x0000000000000000	0x422acccd00000000


Stack frame de gini_asm (direcciones altas arriba):

| Dirección        | Contenido            | Desde rbp     |
|------------------|----------------------|-----------------|
| 0x7fffffffddf8   | 0 (relleno)          | rbp + 0x18      |
| 0x7fffffffddf0   | 0x422acccd (float)   | rbp + 0x10      |
| 0x7fffffffdde8   | 0x5555555551d0 (ret) | rbp + 0x08      |
| 0x7fffffffdde0   | 0x7fffffffde20 (rbp viejo) | rbp + 0x00 = rsp |

Por eso movss 0x10(%rbp),%xmm0 encuentra el float: los offsets son positivos
porque el argumento vive en el frame del llamador, "arriba" del nuevo rbp.

Ejecución de la conversión:


(gdb) stepi                     # movss
(gdb) print $xmm0.v4_float
$1 = {42.7000008, 0, 0, 0}
(gdb) stepi                     # cvttss2si
(gdb) print $eax
$2 = 42
(gdb) stepi                     # addl $1
(gdb) print $eax
$3 = 43


## 4. DESPUÉS: de vuelta en gini_mas_uno (tras pop %rbp y ret)


(gdb) x/4xg $rsp
0x7fffffffddf0:	0x00000000422acccd	0x0000000000000000
0x7fffffffde00:	0x0000000000000000	0x422acccd00000000
(gdb) print $eax
$4 = 43
(gdb) info registers rsp rbp
rsp            0x7fffffffddf0
rbp            0x7fffffffde20


- pop %rbp restauró el rbp de gini_mas_uno (...de20).
- ret sacó la dirección de retorno y volvió a 0x5555555551d0.
- rsp quedó en ...ddf0, apuntando al argumento que había pusheado C.
  Los datos siguen en memoria pero ya no son parte del frame: el caller los
  descarta con add $0x10,%rsp.
- El resultado (43) queda en %eax.
