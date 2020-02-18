#!/bin/bash

while true; do
file=$(ls | grep -v .sh)
mv $file $file.zip
password=$(echo $file | sed -e "s/.zip//g")
unzip -P $password $file
file2=$(ls | grep .zip)
if [[ $file2 != *"flag"* ]]; then
	rm *.zip
else
	echo "[+] flag file"
	tar xf flag.zip; break
fi
done
