text = open("out-sorted.txt").read().strip("\n")

a = []; b = []
for i in text.split("\n"):
	a.append(i.split(",")[0])
for i in text.split("\n"):
	b.append(i.split(",")[1])

text = ""
for i in range(0, len(b)):
	text += chr(int(a[i]))

print text