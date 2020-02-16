#!/usr/bin/python
#-*- coding: utf-8 -*-

import socket

def main():
	HOST = '212.47.229.1'
	PORT = 33001

	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	dest = (HOST, PORT)
	tcp.connect(dest)

	valores_p = []
	valores_c = []
	c = 0
	while True:
		if c > 5000:
			break

		data = tcp.recv(1024)
		valores_p.append(data)
		c += 1

	for p in valores_p:
		if b"pip" in p:
			valores_c.append(".")
		elif b"piiiip" in p:
			valores_c.append("-")
		else:
			valores_c.append(" ")

	f = open("morse1.txt", "w")
	for c in valores_c:
		f.write(c)
	f.close()

if __name__ == "__main__":
	main()
