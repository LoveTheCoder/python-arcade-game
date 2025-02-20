; filepath: fibonacci.asm
section .data
    prompt db "Enter number of Fibonacci terms: "
    prompt_len equ $ - prompt
    newline db 10
    space db " "

section .bss
    input resb 2
    num resb 2

section .text
    global _main

_main:
    ; Print prompt
    mov rax, 0x2000004    ; write syscall
    mov rdi, 1            ; stdout
    mov rsi, prompt
    mov rdx, prompt_len
    syscall

    ; Read input
    mov rax, 0x2000003    ; read syscall
    mov rdi, 0            ; stdin
    mov rsi, input
    mov rdx, 2
    syscall

    ; Convert ASCII to number
    movzx ecx, byte [input]
    sub ecx, '0'          ; Convert from ASCII

    ; Initialize Fibonacci
    mov rax, 0           ; First number
    mov rbx, 1           ; Second number
    
    ; Print first number
    push rcx
    push rbx
    call print_num
    pop rbx
    pop rcx

print_loop:
    push rcx
    mov rdi, space       ; Print space
    call print_char
    pop rcx

    push rcx
    push rax
    push rbx
    
    ; Calculate next number
    mov rdx, rax        ; Save first number
    mov rax, rbx        ; Move second to first
    add rbx, rdx        ; Add first to second
    
    call print_num
    
    pop rbx
    pop rax
    pop rcx
    
    loop print_loop

exit:
    mov rax, 0x2000001    ; exit syscall
    xor rdi, rdi          ; status 0
    syscall

print_num:
    ; Convert number to ASCII and print
    add rax, '0'
    mov [num], al
    mov rax, 0x2000004
    mov rdi, 1
    mov rsi, num
    mov rdx, 1
    syscall
    ret

print_char:
    mov rax, 0x2000004
    mov rsi, rdi
    mov rdi, 1
    mov rdx, 1
    syscall
    ret