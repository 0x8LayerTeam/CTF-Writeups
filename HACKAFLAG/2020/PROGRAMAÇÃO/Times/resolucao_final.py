#!/usr/bin/python3
#-*- coding: utf-8 -*-
import socket

def seleciona(jogadores):
    """
    Definimos um dicionário que conterá como chave as habilidades e como item
    quantas vezes a mesma habilidade aparece.
    """
    habilidades = {}
    for i in jogadores:
        if i in habilidades:
            habilidades[i] += 1
        else:
            habilidades[i] = 1

    """
    Definimos uma lista chamada "maior" que contém a key do dicionário com maior
    item, respectivemente: índice 0 e índice 1, ou seja, a que aparece mais.
    Em outras palavras, é o time formado só por habilidades iguais e
    consequentemente a frequência da habilidade é o total de pessoas do time.
    """
    maior = [max(habilidades, key=habilidades.get), habilidades[max(habilidades, key=habilidades.get)]]

    """
    "dif" recebe um dicionário, que contém a diferença do conjunto de "jogadores"
    (todas habilidades) com o conjunto "maior", ou seja, "dif" irá receber só
    habilidades diferentes da habilidade que mais aparece, e ainda por cima não
    terá repetição de quaisquer outras habiliades, ou seja, só uma "cópia" de cada.
    Obs: conjuntos não aceitam repetidos.
    """
    dif = set(jogadores) - set(maior)

    # Para o if abaixo:
    # Se o tamanho de "dif" for igual ao time de habilidades iguais, então é retornado o tamanho de qualquer um deles.
    # Exemplo: ['crypto', 'for', 'rev', 'web', 'web', 'web']
    #            Temos que se separarmos em dois times:
    #                habilidade iguais = ['web', 'web', 'web']
    #                habilidades diferentes = ['crypto', 'for', 'rev']
    #            Existe a mesma quantidade de players no mesmo time.
    if len(dif) == maior[1]:
        return len(dif)

    # Para o elif abaixo:
    # Se o len(dif) for menor que a lista de habilidades iguais, então temos que avaliar as seguintes possibilidades.
    elif len(dif) < maior[1]:
        # Para o if abaixo, temos:
        # Se adicionarmos 1 ao len(dif) e subtrairmos 1 da lista de habilidades
        # iguais, o que seria igual a tirar uma habilidade dessa lista e
        # adiciona-lá em "dif", e esses forem iguais então é retornado a
        # (lista - 1) ou (len(dif) + 1).
        # Exemplo: ['crypto', 'for', 'web', 'web', 'web', 'web']
        #             Se separarmos os times:
        #                 habilidades iguais = ['web', 'web', 'web']
        #                 habilidades diferentes = ['crypto', 'for', 'web']
        if (len(dif)+1) == (maior[1]-1):
            return (maior[1]-1)

        # Para o elif abaixo:
        # Se adicionarmos 1 ao len(dif) e subtrairmos 1 da lista habilidades
        # iguais, o que seria igual a tirar uma habilidade dessa lista e
        # adiciona-lá em "dif", e o primeiro for maior que o segundo, então temos
        # que o tamanho possível para os times é o próprio tamanho de "dif".
        # Exemplo: ['crypto', 'misc', 'misc', 'web', 'web', 'web']
        #           Se separarmos em times:
        #               habilidades iguais = ['web', 'web']
        #               habilidades diferentes = ['crypto', 'misc']
        #                Pois se definirmos a lista de habilidades iguais como
        #                ['web', 'web', 'web'] e ao passar um valor desses para a
        #                lista de habilidades diferentes, essa última ficará com
        #                tamanho maior, então o correto é manter o tamanho dessa
        #                última e diminuir uma habilidade da lista de habilidades
        #                iguais.
        elif (len(dif)+1) > (maior[1]-1):
            return len(dif)

        # Para o else abaixo:
        # Se mesmo depois das operações acima o len(dif) for menor
        # que a lista de habilidades iguais, então o que resta é transferir uma
        # habilidade a "dif" e retornar o novo tamanho de "dif".
        # Exemplo: ['crypto', 'misc', 'web', 'web', 'web', 'web', 'web', 'web', 'web', 'web']
        #            Se separarmos em times:
        #                habilidades iguais = ['web', 'web', 'web']
        #                habilidades diferetens = ['crypto', 'misc', 'web']
        #                 Pois se definirmos a lista de habilidades iguais como
        #                 ['web', 'web', 'web', 'web', 'web', 'web', 'web', 'web'],
        #                 temos que mesmo se transferirmos uma habilidade para a
        #                 outra lista, a  primeira continuará sendo maior
        #                 (lembre-se que não se pode transferir mais que uma
        #                 habilidade pois a outra lista não pode ter nenhuma
        #                 valor repetido), então apenas transferimos uma
        #                 habilidade e retornamos o novo tamanho da lista de
        #                 habilidades diferentes.
        else:
            return (len(dif)+1)

    # Para o else abaixo:
    # Caso o len(dif) seja maior que a lista de habilidades iguais,
    # então é retornado o tamanha desta lista. O que seria a mesma coisa que
    # apenas retirar uma habilidade de "dif".
    # Exemplo: ['for', 'misc', 'misc', 'misc', 'recon', 'rev', 'rev', 'rev', 'web', 'web']
    #            Se separarmos em times:
    #                habilidades iguais = ['misc', 'misc', 'misc']
    #                habilidaes diferentes = ['for', 'recon', 'rev', 'web']
    #                 Pois como a lista de habilidades diferentes é maior que a
    #                 outra lista e não podemos fazer o que vinhamos fazendo
    #                 acima (transferir uma habilidade), então o que nos resta é
    #                 retornar o tamanho da outra lista, sendo a mesma coisa que
    #                 remover uma habilidade da lista de habilidade diferentes.
    else:
        return maior[1]

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
        resultado = seleciona(jogadores) # Chama a função seleciona() passando a lista de jogadores como argumento.

        tcp.send(bytes(str(resultado[0]), encoding="utf-8")) # Envia o resultado.
        data = tcp.recv(4096) # Recebe os dados do servidor.
        if c == 50: # Se estivermos na Etapa 50 (última etapa), então recebemos mais dados (a flag).
            flag = tcp.recv(4096)
            if b"HACKAFLAG" in flag: # Se houver "HACKAFLAG" dentro da váriavel flag, logo será impresso a flag e depois o programa será finalizado.
                print(flag.decode().split("flag: ")[1].split("\n")[0])
                exit()
        c += 1 # Incrementa o contador.

if __name__ == '__main__':
    main()
