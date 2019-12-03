# runme

**Categoria: Pwn**

# Descrição:
>Everyone starts somewhere.

# Solução:
Apenas executar o binário e digitar "flag":
```
root@kali:~/pwn/runme# ./runme 
Enter 'flag'
> flag
TUCTF{7h4nk5_f0r_c0mp371n6._H4v3_fun,_4nd_600d_luck}
```
Ou usar strings no binário:
```
root@kali:~/pwn/runme# strings runme 
[...]
u+UH
[]A\A]A^A_
Enter 'flag'
flag
TUCTF{7h4nk5_f0r_c0mp371n6._H4v3_fun,_4nd_600d_luck}
How did you fail that?
:*3$"
[...]
```

# Flag:
```TUCTF{7h4nk5_f0r_c0mp371n6._H4v3_fun,_4nd_600d_luck}```
