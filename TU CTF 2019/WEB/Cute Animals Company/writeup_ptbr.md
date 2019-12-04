# Cute Animals Company

**Categoria: Web**

# Descrição:
>Look at this cute website! Why don't you find some cute animals that are hidden from view?

>chal.tuctf.com:30000
![CuteAnimalCompany - Chall](cute0.png)

# Solução:
Acessando o link temos:
![CuteAnimalCompany - Página Web](cute1.png)
Porém não obtivemos muitos resultados, então rodei o dirb em cima do site:
![CuteAnimalCompany - dirb](cute2.png)
Ao acessar "/admin.php", somos redirecionados para "/loginform.html", então tentei um sql injection no formulário:
![CuteAnimalCompany - SQL Injection](cute3.png)
Na próxima página, é possível ver um login "bro/ultimate699":
![CuteAnimalCompany - Credenciais](cute4.png)
Logando com essas credenciais:
![CuteAnimalCompany - Logando](cute5.png)
Redirecionados para "/portal.php":
![CuteAnimalCompany - Portal](cute6.png)
No código fonte de "/portal.php" é possível ver um formulário com um parâmetro "file" que seria enviado via GET:
![CuteAnimalCompany - Código fonte "/portal.php"](cute7.png)
Então, passando "file" como parâmetro e testando alguns payloads, me deparei com um LFI e explorei esse LFI com file:///etc/passwd e assim obtendo a flag:
![CuteAnimalCompany - LFI file:///etc/passwd](cute8.png)

# Flag:
```TUCTF{m0r3_cut3_4n1m415_c4n_b3_f0und_4t_https://bit.ly/1HU2m5Q}```
