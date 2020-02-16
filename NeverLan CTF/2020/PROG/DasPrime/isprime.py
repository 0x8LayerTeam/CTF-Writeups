import math

def main():
	primes = []
	count = 2

	while True:
		divisores = 0
		for x in range(2, int(math.sqrt(count) + 1)):
			if count % x == 0:
				divisores += 1

		if divisores == 0:
			primes.append(count)
			if len(primes) == 10497:
				print(str(primes[10496]) + "\n")
				exit()
		count += 1

if __name__ == "__main__":
    main()
