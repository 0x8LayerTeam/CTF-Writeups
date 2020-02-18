# SarCTF 2020 -- Layouts (Misc) -- 866 pts

We're given a file named as "RWtm7A5f", its a zip compressed file:
```
root@kali:~/ctf/sarctf/layouts# file RWtm7A5f 
RWtm7A5f: Zip archive data, at least v2.0 to extract
```
Extracting the zip file, we get another compressed file (Matroska challenge-like), so we have built a script to deal with it:
```
root@kali:~/ctf/sarctf/layouts/solve-first-step# ls
RWtm7A5f  solve.sh
root@kali:~/ctf/sarctf/layouts/solve-first-step# ./solve.sh 
....................
Archive:  VRdCccaT.zip
  inflating: RDkJMKDa                
Archive:  RDkJMKDa.zip
  inflating: 85iVroNS                
Archive:  85iVroNS.zip
  inflating: kSPrXQjZ                
Archive:  kSPrXQjZ.zip
 extracting: flag                    
Archive:  flag.zip
  End-of-central-directory signature not found.  Either this file is not
  a zipfile, or it constitutes one disk of a multi-part archive.  In the
  latter case the central directory and zipfile comment will be found on
  the last disk(s) of this archive.
unzip:  cannot find zipfile directory in one of flag or
        flag.zip, and cannot find flag.ZIP, period.
[+] flag file
root@kali:~/ctf/sarctf/layouts/solve-first-step# ls flags/
1    105  111  118  124  130  137  143  15   156  162  169  175  181  188  194  20   206  212  219  225  231  238  244  250  27  33  4   46  52  59  65  71  78  84  90  97
10   106  112  119  125  131  138  144  150  157  163  17   176  182  189  195  200  207  213  22   226  232  239  245  251  28  34  40  47  53  6   66  72  79  85  91  98
100  107  113  12   126  132  139  145  151  158  164  170  177  183  19   196  201  208  214  220  227  233  24   246  252  29  35  41  48  54  60  67  73  8   86  92  99
101  108  114  120  127  133  14   146  152  159  165  171  178  184  190  197  202  209  215  221  228  234  240  247  253  3   36  42  49  55  61  68  74  80  87  93
102  109  115  121  128  134  140  147  153  16   166  172  179  185  191  198  203  21   216  222  229  235  241  248  254  30  37  43  5   56  62  69  75  81  88  94
103  11   116  122  129  135  141  148  154  160  167  173  18   186  192  199  204  210  217  223  23   236  242  249  255  31  38  44  50  57  63  7   76  82  89  95
104  110  117  123  13   136  142  149  155  161  168  174  180  187  193  2    205  211  218  224  230  237  243  25   26   32  39  45  51  58  64  70  77  83  9   96
```

As you could see, there are a bunch of folders in there, each folder has one empty file:
```
root@kali:~/ctf/sarctf/layouts/solve-first-step# find flags/ -type f 
flags/125/21
flags/53/17
flags/95/15
flags/83/1
flags/52/7
flags/52/14
flags/89/2
flags/101/9
flags/84/4
flags/78/3
flags/51/10
flags/102/11
flags/112/18
flags/120/13
flags/110/16
flags/103/8
flags/49/19
flags/49/20
flags/122/6
flags/123/5
flags/117/12
```

125, 53, 95, 101, 89, hm... all of those "numbers" are ASCII Readable chars, maybe those files "sequentially" created within those "random" folders should give us a guide of which characters should be read first, let's try it.

So I created a script "stego.py" which will decode those ASCII codes following the "guide" by reading the file "out-sorted.txt":
```
root@kali:~/ctf/sarctf/layouts# cat out-sorted.txt 
83,1
89,2
78,3
84,4
123,5
122,6
52,7
103,8
101,9
51,10
102,11
117,12
120,13
52,14
95,15
110,16
53,17
112,18
49,19
49,20
125,21
root@kali:~/ctf/sarctf/layouts# python stego.py 
SYNT{z4ge3fux4_n5p11}
```

It looks like it got encoded using Caesar Cipher, let's decode it using https://www.dcode.fr/caesar-cipher:

(shift) +13	(text) FLAG{m4tr3shk4_a5c11}

#### FLAG{m4tr3shk4_a5c11}
