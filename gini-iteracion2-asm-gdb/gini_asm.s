 .text
    .globl gini_asm
    .type gini_asm, @function
gini_asm:
    pushq %rbp
    movq  %rsp, %rbp
    movss 0x10(%rbp), %xmm0      # 7mo argumento (el float) desde el stack
    cvttss2si %xmm0, %eax        # float -> int (trunca)
    addl  $1, %eax               # +1
    popq  %rbp
    ret

    .section .note.GNU-stack,"",@progbits
