# Roboworld

**Categoria:** Web

## Descrição:
A friend of mine told me about this website where I can find secret cool stuff. He even managed to leak a part of the source code for me, but when I try to login it always fails :(

Can you figure out what's wrong and access the secret files?

Remote server: http://challs.xmas.htsp.ro:11000
Files: leak.py
Author: Reda


## Solução
Como premissa de uma flag web, primeiro vamos acessar nosso alvo via browser para vermos o que será retornado.

![Login](print1_login.png)

Então temos aqui uma tela de login onde podemos tentar alguns tipos de injections, mas antes vamos dar uma olhada no arquivo `leak.py` que foi disponibilizado.

![Leak](print2-leak.py.png)

Fazendo um code review, podemos pegar o usuário/senha (linha 21) e a chave privada (linha 36) que está sendo substituída por uns `XXXXXXXXXXXXXX`, deixando assim a chave sempre inválida. Testando essa combinação de usuário e senha na página web, não obtive um bom retorno, então analisei o código novamente e descobri uma falha na linha 19, que é possível inserir um `{}` e alterar a atribuição do valor... É nesse ponto que iremos atacar para explorar essa falha.

![Login Failed](print3-login-burp.png)

> Payload: 
user=backd00r&pass=catsrcool&captcha_verification_value=GlHgspeIs2%26privateKey=8EE86735658A9CE426EAF4E26BB0450E%26test={}&remote_addr=127.0.0.1&captchaUserValue=GlHgspeIs2&privateKey=8EE86735658A9CE426EAF4E26BB0450E&privKey=8EE86735658A9CE426EAF4E26BB0450E

![paylaod](print4-burp-payload.png)

Bingo, conseguimos passar dessa parte, porém estamos recebendo uma mensagem de `access denied`, o que não é muito bom. 

![Access Denied](print5-burp-access-denied.png)

Reparando melhor na tela antes do redirecionamento, podemos ver que foi criada uma sessão que se perde depois de nos redirecionar. Vamos então colocar esse cookie manualmente para corrigir esse problema.

![cookie](print6-burp-cookie.png)
![files](print7-burp-secret.png)

Bom, agora temos 3 arquivos interessantes que devemos analisar.  Nas duas imagens, não encontrei nada de interessante, mas no vídeo encontrei a solução do meu problema, a valiosa flag.

![img1](2.jpg)
![img2](098c533dc5420628a9f51c1911198c4c.jpg)
![video](print7-wtf.mp4.png)

Obviamente ela não está no formato correto pois está invertida, mas para corrigir vamos executar o comando `echo '}o.0_?tob0R_3hT_1_mA{SAM-X' | rev`

![Flag](print8-flag.png)

Mission Complete!! Mais uma flag conquistada, é hora de comemorar.

Espero que esse writeup tenha sido útil.

Abs...


## Flag: 
```X-MAS{Am_1_Th3_R0bot?_0.o}```
