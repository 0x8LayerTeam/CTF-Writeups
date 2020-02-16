#!/usr/bin/python
#-*- coding: utf-8 -*-

import socket, string, codecs

def main():
	HOST = '212.47.229.1'
	PORT = 33002

	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	dest = (HOST, PORT)
	tcp.connect(dest)

	data = tcp.recv(2048)
	while b"Answer" in data:
		if b"FLAG" in data:
			print(data)
			exit()

		print(data)
		palavra = data.split(b":")[1].split(b"\n")[0]
		result = codecs.encode(palavra[2::], "rot_13")
		print(result)

		if "FLAG" in result:
			print(result)
			exit()

		tcp.send(result + b"\n")
		data = tcp.recv(2048)

	print(data)


if __name__ == "__main__":
	main()
