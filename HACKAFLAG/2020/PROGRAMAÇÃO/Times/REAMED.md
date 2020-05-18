# Times

**Categoria: Programação**

# Descrição:
> (imagem_chall.png)

# Solução
Pela descrição e pelo desenrolar do desafio, é possível entender que o servidor dará uma lista de habilidades para que se possa dividir em dois times: um time formado apenas por jogadores com habilidades iguais e outro time formado apenas por jogadores de habilidades diferente (NÃO PODE HAVER MAIS DE UM JOGADOR COM A MESMA HABILIDADE!).
Estes são exemplos das listas de jogadores:
(imagem.png)

Tendo essa informação, vamos ao script.
Irei começar pela função main(). Ela simplesmente faz a conexão com o servidor e "ajeita" os valores recebidos de tal forma que fique "limpo" para a ser usado.
```
def main():
    """
    Até a linha em que se encontra "tcp.connect()" é apenas a conexão ao servidor.
    """
    HOST = "142.93.73.149"
    PORT = 15052
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    tcp.connect(dest)

    tcp.recv(1024), tcp.recv(1024) # Recebe os dados do servidor.
    tcp.send(b"start") # Envia o start para o desafio começar.

    tcp.recv(4096) # Recebe os dados do servidor.
    data = tcp.recv(4096) # Recebe os dados do servidor e guarda numa váriavel que usaremos para obter a lista de habilidades.
    c = 1 # Contador das Etapas.
    #while b"HACKAFLAG" not in data:
    while True: # Executa o loop até o algum valor enviado como resultado ser errado ou até a flag ser encontrada.
        if b"Ops" in data: # Caso haja a palavra "Ops" é porque o resultado está errado ou demoramos muito para responder.
            break # Sai do loop e consequentemente finaliza o programa.

        print("ETAPA " + str(c) + " --------------") # Imprime em que Etapa estamos.
        while b"resposta" not in data: # Caso os valores não tenham sido recebidos completamente, esse loop entrará em execução.
            data += tcp.recv(5120) # Recebe mais dados do servidor.

        """
        Faz o decode dos dados recebidos e o reconhecimento das habilidades.
        """
        jogadores = data.decode().split("Jogadores: [")[1].split("]\n     A resposta")[0].split(", ")
        resultado = seleciona(jogadores) # Chama a função seleciona() passando a lista de habilidades como argumento.

        tcp.send(bytes(str(resultado), encoding="utf-8")) # Envia o resultado.
        data = tcp.recv(4096) # Recebe os dados do servidor.
        if c == 50: # Se estivermos na Etapa 50 (última etapa), então recebemos mais dados (a flag).
            flag = tcp.recv(4096)
            if b"HACKAFLAG" in flag: # Se houver "HACKAFLAG" dentro da váriavel flag, logo será impresso a flag e depois o programa será finalizado.
                print(flag.decode().split("flag: ")[1].split("\n")[0])
                exit()
        c += 1 # Incrementa o contador.

if __name__ == '__main__':
    main()
```

Agora indo para a função mais importante: função seleciona().
Essa função faz a escolha de quantos jogadores/habilidades podem em ambos times.
Para isso precisamos contruir um dicionário que conterá todos as habilidades e a frequência das mesmas. Da seguinte forma: dict[nome_habilidade] = frequencia.
```
def seleciona(jogadores):
    habilidades = {}
    for i in jogadores:
        if i in habilidades:
            habilidades[i] += 1
        else:
            habilidades[i] = 1
```
Logo depois, precisamos de uma lista para guardar a habilidade que aparece mais vezes. Ela também é a lista de habilidaes iguais.
Obs: índice 0 guarda o nome da habilidade e o índice 1 guarda a frequência.
```
    maior = [max(habilidades, key=habilidades.get), habilidades[max(habilidades, key=habilidades.get)]]
```
Em seguida, é preciso de um dicionário para guardar as habilidades diferentes da habilidade de maior frequência, mas que essas habilidades diferentes não sejam repetidas dentro do dicionário.
Obs: é construído um dicionário com a diferença entre um conjunto e outro, por
isso usei set(). (conjunto, de forma grosseira, é uma lista que não contém repetições).
```
    dif = set(jogadores) - set(maior)
```
Agora a parte mais lógica do programa.
A primeira verificação que deve ser feita é se o tamanho das listas são iguais, se forem então é só retornar o tamanho de qualquer uma. (O tamanho aqui pode ser entendido como a quantidade de jogadores em cada time).
```
    if len(dif) == maior[1]:
          return len(dif)
```
Caso o tamanho da lista de habilidades iguais seja maior que o tamanho da outra lista.
```
    elif len(dif) < maior[1]:
```
Sendo assim, temos que analisar outros casos:

1º - Se adicionarmos 1 ao len(dif) e subtrairmos 1 da lista de habilidades iguais, o que seria igual a tirar uma habilidade dessa lista e adiciona-lá em "dif", e esses tamanhos sejam iguais então é retornado a (len(lista) - 1) ou (len(dif) + 1).

Exemplo: ['crypto', 'for', 'web', 'web', 'web', 'web'].

Se separarmos os times: habilidades iguais = ['web', 'web', 'web'], habilidades diferentes = ['crypto', 'for', 'web']

Inicialmente a lista de habilidades iguais seria ['web', 'web', 'web', 'web'], mas como essa era maior que a outra lista, então uma habilidade dessa lista foi transferida a outra. Em código:
```
        if (len(dif)+1) == (maior[1]-1):
                return (maior[1]-1)
```

2º - Se adicionarmos 1 ao len(dif) e subtrairmos 1 da lista habilidades iguais, o que seria igual a tirar uma habilidade dessa lista e adiciona-lá em "dif", e o primeiro for maior que o segundo, então temos que o tamanho possível para os times é o próprio len(dif).

Exemplo: ['crypto', 'misc', 'misc', 'web', 'web', 'web']

Se separarmos em times: habilidades iguais = ['web', 'web'], habilidades diferentes = ['crypto', 'misc']

Pois se definirmos a lista de habilidades iguais como ['web', 'web', 'web'] e ao passar um valor desses para a lista de habilidades diferentes, essa última ficará com tamanho maior, então o correto é manter o tamanho original dessa última e diminuir uma habilidade da lista de habilidades iguais. Em código:
```
        elif (len(dif)+1) > (maior[1]-1):
                return len(dif)
```

3º - Se mesmo depois das operações acima o len(dif) for menor que a lista de habilidades iguais, então o que resta é transferir uma habilidade a "dif" e retornar o novo tamanho de "dif".

Exemplo: ['crypto', 'misc', 'web', 'web', 'web', 'web', 'web', 'web', 'web', 'web']

Se separarmos em times: habilidades iguais = ['web', 'web', 'web'], habilidades diferetens = ['crypto', 'misc', 'web']

Pois se definirmos a lista de habilidades iguais como ['web', 'web', 'web', 'web', 'web', 'web', 'web', 'web'], temos que se transferirmos uma habilidade para a outra lista, a  primeira continuará sendo maior (lembre-se que não se pode transferir mais que uma habilidade pois a outra lista não pode ter nenhum valor repetido), então apenas transferimos uma habilidade e retornamos o novo tamanho dessa outra lista ("dif"). Em código:
```
        else:
            return (len(dif)+1)
```
E, por último, caso o len(dif) seja maior que a lista de habilidaes iguais, então é retornado o tamanha desta lista. O que seria a mesma coisa que apenas retirar uma habilidade de "dif".

Exemplo: ['for', 'misc', 'misc', 'misc', 'recon', 'rev', 'rev', 'rev', 'web', 'web']

Se separarmos em times: habilidades iguais = ['misc', 'misc', 'misc'], habilidaes diferentes = ['for', 'recon', 'rev', 'web']

Pois como a lista de habilidades diferentes é maior que a outra lista e não podemos fazer o que vinhamos fazendo acima (transferir uma habilidade), pois nessa outra lista só pode habilidades iguais, então o que nos resta é retornar o tamanho da outra lista, sendo a mesma coisa que remover uma habilidade da lista de habilidade diferentes. Em código:
```
    else:
          return maior[1]
```

O código final é (também pode ser encontrado aqui nesse github):
```
#!/usr/bin/python3
#-*- coding: utf-8 -*-
import socket

def seleciona(jogadores):
    habilidades = {}
    for i in jogadores:
        if i in habilidades:
            habilidades[i] += 1
        else:
            habilidades[i] = 1

    maior = [max(habilidades, key=habilidades.get), habilidades[max(habilidades, key=habilidades.get)]]

    dif = set(jogadores) - set(maior)

    if len(dif) == maior[1]:
        return len(dif)

    elif len(dif) < maior[1]:
        if (len(dif)+1) == (maior[1]-1):
            return (maior[1]-1)
        elif (len(dif)+1) > (maior[1]-1):
            return len(dif)
        else:
            return (len(dif)+1)
    else:
        return maior[1]

def main():
    HOST = "142.93.73.149"
    PORT = 15052
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    tcp.connect(dest)

    tcp.recv(1024), tcp.recv(1024)
    tcp.send(b"start")

    tcp.recv(4096)
    data = tcp.recv(4096)
    c = 1
    #while b"HACKAFLAG" not in data:
    while True:
        if b"Ops" in data:
            break

        print("ETAPA " + str(c) + " --------------")
            data += tcp.recv(5120)

        jogadores = data.decode().split("Jogadores: [")[1].split("]\n     A resposta")[0].split(", ")
        resultado = seleciona(jogadores)

        tcp.send(bytes(str(resultado[0]), encoding="utf-8"))
        if c == 50:
            flag = tcp.recv(4096)
            if b"HACKAFLAG" in flag:
                print(flag.decode().split("flag: ")[1].split("\n")[0])
                exit()
        c += 1

if __name__ == '__main__':
    main()
```
A partir dessas explanações é só juntar tudo e pronto! :)
(imagem_flag.png)


# Flag:
```HACKAFLAG{IIYECICKGBDUCRBQKIQSCIBSGM3TIOJTHA3TEOIK}```
