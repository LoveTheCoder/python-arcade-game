; filepath: solution.asm
; Assemble with: nasm -f macho64 solution.asm -o solution.o
; Link with: ld solution.o -lSystem -macosx_version_min 10.7 -o solution
; Then run: ./solution

global _main
extern _printf, _scanf

section .data
    prompt      db "Enter number of Fibonacci numbers: ", 0
    scanf_fmt   db "%d", 0
    print_fmt   db "%d", 10, 0     ; "%d\n"

section .bss
    n   resd 1

section .text
_main:
    ; Print prompt
    lea rdi, [rel prompt]   
    xor eax, eax           ; Number of floating point registers used = 0
    call _printf

    ; Read integer input using scanf
    lea rdi, [rel scanf_fmt]
    lea rsi, [rel n]
    xor eax, eax
    call _scanf

    ; Load count value into eax and ecx (loop counter)
    mov eax, [n]
    mov ecx, eax          ; ecx = count
    cmp ecx, 0
    je end_program        ; if count is 0, exit

    ; Initialize Fibonacci values:  a = 0, b = 1
    xor r8d, r8d          ; r8d = a = 0
    mov r9d, 1            ; r9d = b = 1

    ; Print first Fibonacci number: 0
    lea rdi, [rel print_fmt]
    mov rsi, r8d          ; print a (0)
    xor eax, eax
    call _printf

    dec ecx               ; one number printed
    cmp ecx, 0
    je end_program

    ; Print second Fibonacci number: 1
    lea rdi, [rel print_fmt]
    mov rsi, r9d          ; print b (1)
    xor eax, eax
    call _printf

    dec ecx               ; two numbers printed

fib_loop:
    ; Compute next = a + b
    mov eax, r8d
    add eax, r9d         ; eax = a + b

    ; Update: a = b, b = next
    mov r8d, r9d
    mov r9d, eax

    ; Print next Fibonacci number
    lea rdi, [rel print_fmt]
    mov rsi, eax
    xor eax, eax
    call _printf

    dec ecx
    cmp ecx, 0
    jne fib_loop

end_program:
    xor eax, eax
    ret