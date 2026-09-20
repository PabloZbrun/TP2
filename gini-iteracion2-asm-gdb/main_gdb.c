main


#include <stdio.h>

int gini_mas_uno(float valor);

int main(void) {
    float x;
    int resultado;

    x = 42.7f;
    resultado = gini_mas_uno(x);
    printf("gini_mas_uno(%.1f) = %d\n", x, resultado);

    return 0;
}
