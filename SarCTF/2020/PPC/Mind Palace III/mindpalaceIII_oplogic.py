#!/usr/bin/python
#-*- coding: utf-8 -*-

import socket

def main():
        HOST = '212.47.229.1'
        PORT = 33003

        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dest = (HOST, PORT)
        tcp.connect(dest)

        data = tcp.recv(2048)
	while "FLAG" not in data:
		result = 0
		print(data)
		valores = data.split(b"[>]")[1].split(b"\n")[0].split(b" ")
		op = valores[2]

		if op == b"XOR":
			result = int(valores[1]) ^ int(valores[3])
		elif op == b"OR":
			result = int(valores[1]) | int(valores[3])
		elif op == b"AND":
			result = int(valores[1]) & int(valores[3])
		else:
			print(op)

		print(result)
		tcp.send(str(result) + b"\n")
		data = tcp.recv(2048)
	print(data)

if __name__ == "__main__":
	main()
