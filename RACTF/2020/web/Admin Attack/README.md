# Admin Attack

![Banner Chall](images/banner-chall.png)

Essa é uma chall bem simples que pode ser explorada com SQL Injection.  
Assim que abrimos a URL, podemos ver uma página WEB de autenticação esperando por um usuário e senha.  


![Login](images/login.png)

Começando pelo básico do básico, vamos verificar se o código apresenta falhas ao tratar aspas simples.

![Injection Quote](images/injection-quote.png)

Check!! Vemos então a falha da aplicação ao tentar realizar a query e também já sabemos que o alvo utiliza SQLite.

![Flaw SQL Injection](images/flaw-sqli.png)

Agora que já sabemos seu ponto fraco, é hora de explorar.    
Iremos injetar o seguinte código no campo `username` e no campo `password`.  
  
**PAYLOAD:** `' or 1=1 -- `

![First Injection](images/first-injection.png)

E então vamos ter o seguinte resultado.


![Welcome xxslayer420](images/welcome-xxslayer420.png)

Bom, pegamos um usuário que, aparentemente não é um usuário que está nos entregando a Flag. Por padrão, quando utilizamos esse injection, o SQLite irá nos retornar o primeiro resultado válido. Pensando assim, vamos tentar ignorar esse usuário e pegar o segundo resultado válido.    
Nosso payload agora irá ficar uma leve alteração, ficando assim:  
  
**PAYLOAD:** `' or username != 'xxslayer420' -- `

![Final Exploit Login](images/final-exploit-login.png)

E como resultado iremos ter...

![Flag](images/flag.png)

Trabalho feito, já podemos ver a flag que o usuário `JimmyTehAdmin` nos deu. 
   
**FLAG:** `ractf{!!!4dm1n4buse!!!}`