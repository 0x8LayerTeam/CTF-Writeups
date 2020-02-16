# SarCTF 2020 -- Confidential (Forensics) -- Writeup
We're given a pcap capture file, "capture.pcap". First of all, we enumerated the pcap file using wireshark, as shown below:

Taking a look in those packets, we could understand what was primordialy happening there: a FTP File Transmission. Using Wireshark, we saved those files by getting their tcp-data stream and saving them into our storage.
![Alt text](https://github.com/0x8Layer/CTF-Writeups/blob/master/SarCTF/2020/Forensics/image.png?raw=true "Files")

database.kdbx is a Keepass Password Database, we can break his password using:
```
$ keepass2john database.kdbx > database.hash
$ john database.hash --wordlist=/usr/share/wordlists/rockyou.txt
database:blowme!
1 password hash cracked, 0 left
```

Now we just have to access the database using the cracked password:
```
$ keepass2 database.kdbx
```

![Alt text](https://github.com/0x8Layer/CTF-Writeups/blob/master/SarCTF/2020/Forensics/image2.png?raw=true "Flag")
