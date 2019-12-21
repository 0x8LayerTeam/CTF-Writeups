# Santa's letter

**Category: Forensics**

# Description:
> It seems that Santa may have used some Invisible Ink to write this letter... he is surely playing Hide&Seek.
> 
> Files: challenge.png

# Solve

Once you download the filer linked in the above description, you find an image called *challenge.png*, as shown ahead:

<img src="image1.png">

So, since there was a *Hide&Seek* hint on the description, we used DIIT (Digital Invisible Ink Toolkit) 1.5 (see more about it [here](http://diit.sourceforge.net/)) to try and decode it through *HideSeek* algorithm, as shown in the following image:

<img src="image2.png">

After that, we simply checke the *flag_chall.out* file content, as follows:

```bash
cat /root/flag_chall.out
```

The execution of such command printed the following *flag*: ```X-MAS{NOBODY:_SANTA:Hyvää joulua!}```.

# Flag: 
```X-MAS{NOBODY:_SANTA:Hyvää joulua!}```
