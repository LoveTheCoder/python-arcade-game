; Assemble and link (for Linux x86_64) with:
;   nasm -f elf64 fibonacci.asm -o fibonacci.o
;   ld fibonacci.o -o fibonacci
; Usage:
;   ./fibonacci
; This program reads a single integer (1-digit, e.g. 5) from stdin,
; then prints the first N Fibonacci numbers (one per line).

section .data
prompt:     db  "Enter number of Fibonacci terms to generate (1-9): ", 0
prompt_len: equ $-prompt
newline:    db  10, 0

section .bss
input:  resb  4       ; buffer for user input
output: resb  32      ; buffer for printing numbers

section .text
global _start

_start:
    ;---------------------------
    ; Write the prompt
    ;---------------------------
    mov rax, 1          ; sys_write
    mov rdi, 1          ; stdout
    mov rsi, prompt
    mov rdx, prompt_len
    syscall

    ;---------------------------
    ; Read up to 1 digit + newline
    ;---------------------------
    mov rax, 0          ; sys_read
    mov rdi, 0          ; stdin
    mov rsi, input
    mov rdx, 2
    syscall

    ; Convert the first character of input from ASCII to number
    mov r8b, [input]
    sub r8b, '0'        ; e.g. if user typed '5', r8b = 5

    ; We'll store the count in r9
    mov r9, r8

    ; Initialize fibonacci values:
    ; F0 = 0, F1 = 1
    xor rax, rax        ; rax = current fib (F0)
    mov rbx, 1          ; rbx = next fib (F1)
    xor r10, r10        ; counter

print_fib_loop:
    cmp r10, r9
    jge done

    ; Print current Fibonacci number in rax
    push r10
    push rbx
    call print_num
    pop rbx
    pop r10

    ; Advance to next fib
    add rbx, rax
    xchg rax, rbx
    inc r10
    jmp print_fib_loop

done:
    ; Exit
    mov rax, 60         ; sys_exit
    xor rdi, rdi
    syscall

;--------------------------------------------------
; print_num - prints the unsigned integer in RAX
; followed by a newline.
;--------------------------------------------------
print_num:
    push rbx
    push rcx
    push rdx

    mov rdi, output     ; rdi points to buffer
    mov rcx, 0          ; digit count
    mov rbx, 10         ; base 10

    cmp rax, 0
    jne .convert
    ; If RAX = 0, special case
    mov byte [rdi], '0'
    mov byte [rdi+1], 10    ; newline
    mov rdx, 2
    jmp .write_it

.convert:
    .loop:
        xor rdx, rdx
        div rbx         ; divide RAX by 10
        add dl, '0'
        mov [rdi+rcx], dl
        inc rcx
        cmp rax, 0
        jne .loop

    ; rcx is number of digits, reverse them
    mov r8, 0
    dec rcx
    .reverse_loop:
        cmp r8, rcx
        jge .done_reversing
        mov dl, [rdi+r8]
        mov dh, [rdi+rcx]
        mov [rdi+r8], dh
        mov [rdi+rcx], dl
        inc r8
        dec rcx
        jmp .reverse_loop

    .done_reversing:
    ; Add newline at the end
    inc r8
    mov byte [rdi+r8], 10
    inc r8
    mov rdx, r8

.write_it:
    ; Write the string in buffer
    mov rax, 1      ; sys_write
    mov rdi, 1      ; stdout
    mov rsi, output
    syscall

    pop rdx
    pop@ rcx
    pop rbx
    ret