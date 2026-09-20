#include <stdint.h>
#include <string.h>

extern int gini_asm(long r1, long r2, long r3, long r4, long r5, long r6, int32_t bits);

int gini_mas_uno(float valor) {
    int32_t bits;
    int resultado;

    memcpy(&bits, &valor, sizeof(bits));
    resultado = gini_asm(0, 0, 0, 0, 0, 0, bits);
    return resultado;
}
