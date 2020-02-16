# SarCTF 2020 -- DeepDive (Misc) -- 701 pts

Typical matriosha challenge, using basic programming skills, you can solve this one:
```
root@kali:~/ctf/sarctf/deep_dive# file flag.txt 
flag.txt: POSIX tar archive (GNU)
root@kali:~/ctf/sarctf/deep_dive# ./solve.sh
..............
[+] POSIX tar
[+] bzip2
bzip2: Can't guess original name for flag.txt -- using flag.txt.out
[+] bzip2
bzip2: Can't guess original name for flag.txt -- using flag.txt.out
[+] Zip
Archive:  flag.txt
replace flag.txt? [y]es, [n]o, [A]ll, [N]one, [r]ename:   inflating: flag.txt                
[+] bzip2
bzip2: Can't guess original name for flag.txt -- using flag.txt.out
[+] POSIX tar
[+] ASCII
FLAG{matri0sha256}
```
