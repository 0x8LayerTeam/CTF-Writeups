#!/usr/bin/python
#-*- coding: utf-8 -*-

import hashlib

def main():
	HASH = "267530778aa6585019c98985eeda255f"
	colors = ["red", "blue", "yellow", "purple", "green", "black", "white", "gray", "pink", "violet", "brow", "orange", "grey", "dark", "magenta", "lime", "blank"]
	members = ["zestyfe", "durkinza", "purvesta", "s7a73farm"]

	for color in colors:
	    for year in range(1900, 2021):
	        for member in members:
	            hashencode = color + "-" + str(year) + "-" + member
	            result = hashlib.md5(hashencode)
	            hash_crack = result.hexdigest()

	            if hash_crack == HASH:
	                print(HASH + " is: " + hashencode)
	                exit()

if __name__ == "__main__":
	main()
