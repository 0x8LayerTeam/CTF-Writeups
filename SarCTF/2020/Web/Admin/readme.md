# SarCTF2020 -- Admin (Web) -- 957 pts

Analyzing http://sherlock-message.ru/script.js, we figured out that the application can be bruteforce'd by supplying a new hash token for every login try we made
So, we created a multithreaded script to do this job for us:

![Alt text](https://github.com/0x8Layer/CTF-Writeups/blob/master/SarCTF/2020/Web/Admin/image.png?raw=true "Files")

#### FLAG{bruTe_with_hash_f0rce}
