#!/usr/bin/python
#-*- coding: utf-8 -*-

import socket, base64

def main():
	HOST = 'challenges.neverlanctf.com'
	PORT = 1120

	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	dest = (HOST, PORT)
	tcp.connect(dest)

	data = tcp.recv(2048)
	while b"decrypt" in data:
		print(data)
		bas64 = data.split(b"decrypt:")[1]
		valor = base64.b64decode(bas64)
		tcp.send(valor)
		data = tcp.recv(2048)

	print(data)

if __name__ == "__main__":
	main()
