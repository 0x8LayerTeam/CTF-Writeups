

> Written by **lighthouse64**
> 
> Your friend was trying to send you the stuff that he did for your group project, but the data mysteriously got [corrupted](https://static.tjctf.org/dc3b12c1155ea3c09800ebec00f8d31498af64fe6f76e0c75a552ff2c75cc762_corrupted_project). He said his computer got infected before he was able to send it. Regardless of what happened, you need to fix it or you won't be able to complete the project.

This chall is actually pretty simple but the zip archive's messed up structure works kind of as a misdirection. The zip structure tells where the archived file starts and ends.

Here is a very nice zip file reference documentation: 
https://users.cs.jmu.edu/buchhofp/forensics/formats/pkzip.html

The bytes in the range 001A:001D store the archived filename's length and some extra fields after it:

    00000000: 2e4b 0304 1e03 8200 3f12 339f b250 ea54  .K......?.3..P.T
    00000010: 882e 7d0a 0000 f40a 0000 1100 1c00 7072  ..}...........pr
    00000020: 6f6a 6563 742d 6669 6c65 732e 7a69 7055  oject-files.zipU
    00000030: 5409 0003 f220 c35e ea24 c35e 7578 0b00  T.... .^.$.^ux..
    00000040: 0104 e803 0000 04e8 0300 0042 5a65 390c  ...........BZe9.

filename length:    0x0011 = 17 bytes  
extra field length: 0x001C = 28 bytes

So the archived file starts at 004B: 

    0000004b: 425a 6539 0c2a 12f9 7be9 4d9e 3789 0001  BZe9.*..{.M.7...

... and it's a bzip2 archive file header. We have it's beginning now let's find it's end.


A zip archive has two structures at it's end, the Central Directory Record (CDR) and the CDR End. Just before the CDR is the end of the archive's packed data. A zip file signature and it's internal headers all start with 0x504B ("PK") and has 4 bytes in total, being:

0x504B0304: local file header (one for each file in the archive)  
0x504B0102: CDR  
0x504B0506: CDR End  

As there's only one local file header things get easier. We get all the bytes from 004B (75 bytes) to the ones before 0x504B0102, which is at 0x0AC7.

    $ dd bs=1 skip=75 count=2759 if=dc3b12c1155ea3c09800ebec00f8d31498af64fe6f76e0c75a552ff2c75cc762_corrupted_project of=project-files.bz2

The bzip2 documentation is very scarce and our best shot is in the Wikipedia: 
https://en.wikipedia.org/wiki/Bzip2#File_format

This is what matters here:

    .magic:16                       = 'BZ' signature/magic number
    .version:8                      = 'h' for Bzip2 ('H'uffman coding), '0' for Bzip1 (deprecated)
    .hundred_k_blocksize:8          = '1'..'9' block-size 100 kB-900 kB (uncompressed)
    .compressed_magic:48            = 0x314159265359 (BCD (pi))
    .crc:32                         = checksum for this block

Going each header part at a time, without touching CRC complicated stuff, it goes from this:

    00000000: 425a 6539 0c2a 12f9 7be9 4d9e 3789 0001  BZe9.*..{.M.7...

to this:

    00000000: 425a 6839 3141 5926 5359 4d9e 3789 0001  BZh91AY&SYM.7...

In challenges like this it's very useful if you create a file yourself to check how a valid file is structured and it's values.


Ok, so now we can open the project-files.bz2 archive, extract the `project-files` file and extract its content too. It is 3 PNG files, one of which (project-notes-1.png) is messed up. When this file is open in a hex editor, we get a cry for help:

    $ xxd project-notes-1.png | head
    00000000: 4845 4c50 0d0a 1a0a 0000 000d 4948 4452  HELP........IHDR


... and we replace it with the correct 0x89504E47 value:

    $ xxd project-notes-1.png | head
    00000000: 8950 4e47 0d0a 1a0a 0000 000d 4948 4452  .PNG........IHDR

Here's the flag:
> tjctf{plz_dont_procrastinate}


