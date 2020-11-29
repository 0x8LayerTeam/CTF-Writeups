import socket

def tribonacci(n):
    global cont # Contador de chamadas recursivas que estava como variável global.
    global dicionario # Dicionário que armazena todos os resultados da sequência para diversos n's.
    global dict_cont # Dicionário que armazena todos os números de recursão para diversos n's.

    if n == 1 or n == 0: # Segundo a fórmula do Tribonacci
        cont += 1
        return 0
    elif n == 2: # Segundo a fórmula do Tribonacci
        cont += 1
        return 1
    try:
        if dicionario[n]: # Verifica se o n já foi calculado antes
            cont += dict_cont[n]
            return dicionario[n]
    except:
        pass
    cont += 1
    dicionario[n] = tribonacci(n-3) + tribonacci(n-2) + tribonacci(n-1)
    return dicionario[n]

def main():
    HOST = "tribocursao-01.fireshellsecurity.team" # Conexão com o servidor.
    PORT = 20010
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    tcp.connect(dest)

    tcp.recv(1024), tcp.recv(1024) # Recebe os textos do servidor.
    tcp.send(b"start") # Envia o start para iniciar o challenge.

    tcp.recv(1024)
    data = tcp.recv(1024) # Recebe o primeiro desafio.

    global dicionario # Define o dicionário, que armazena o resultado das somas da sequência, como global para que a função Tribonacci possa acessá-lo.
    dicionario = {}

    num_desafio = 1 # Contador de número de desafios.
    while b"bhack{" not in data: # Executa o código abaixo enquanto a flag não aparecer.
        n = data.decode().split("N: ")[1].split("\n")[0] # Obtém o n.

        global cont # Define o contador de número de chamadas recursivas como global para que a função Tribonacci possa acessá-lo.

        global dict_cont # Define o dicionário, que conterá o número de chamadas recursivas, como global para que a função Tribonacci possa acessá-lo.
        dict_cont = {}

        for i in range(int(n)+1):
            cont = 0 # Toda vez que o loop for executado, esse contador será zerado.
            tribonacci(i)
            dict_cont[i] = cont

        print("[+] Desafio", num_desafio) # Imprime informações sobre o challenge.
        print("N:", n)
        print("Resposta:", cont)

        tcp.send(bytes(str(cont) + "\n", encoding="utf-8")) # Envia o número de recursões daquele n.
        tcp.recv(1024)
        data = tcp.recv(1024) # Recebe o novo desafio ou a flag (:D)

        num_desafio += 1

    FLAG = data.decode().split(": ")[1].split('\n')[0]
    print("\nFLAG:", FLAG) # Imprime a flag.

if __name__ == "__main__":
    main()
