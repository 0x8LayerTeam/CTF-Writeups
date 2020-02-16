#!/bin/bash
while true; do
ftype=$(file flag.txt)

#bzip2
if [[ $ftype == *"bzip2"* ]]; then
	echo "[+] bzip2"
	bzip2 -d flag.txt; mv flag.txt.out flag.txt
fi

#POSIX tar
if [[ $ftype == *"POSIX tar"* ]]; then
	echo "[+] POSIX tar"
        tar xf flag.txt
fi

#gzip
if [[ $ftype == *"gzip"* ]]; then
        echo "[+] gzip"
	mv flag.txt flag.txt.gz; gzip -d -f flag.txt
fi

#XZ compressed data
if [[ $ftype == *"XZ"* ]]; then
        echo "[+] XZ"
        mv flag.txt flag.txt.xz; tar xf flag.txt.xz
fi

#Zip archive
if [[ $ftype == *"Zip"* ]]; then
        echo "[+] Zip"
        echo A | unzip flag.txt
fi

#ASCII
if [[ $ftype == *"ASCII"* ]]; then
        echo "[+] ASCII"
        cat flag.txt; break
fi

done
