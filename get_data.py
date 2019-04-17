
def get_data(channel, freq, T, filename, mode):

	# mode = "d"
	try:
		with open(filename) as f:
			line = f.readlines()

		for data in line:
			if mode == "d":
				print(data)
			tmp = data.split()
			if mode == "d":
				print(len(tmp))
			if len(tmp) >= 2:
				# continue/
				channel.apend(1)
				freq.append(tmp1[1])
				T.apend(tmp1[2])

				# if tmp1[0].isalpha():
				# 	continue
	# except AttributeError as e:
	# 	print(e)
	# 	print("index err")
	# 	return -1

	# else:
	# 	return 0

channel = []
freq = []
T = []

tmp = get_data(channel, freq, T, "i18286_H2O_181223.txt", "d")
for i in range(0, len(channel)):
	print(channel[i], end="")
	print(freq[i], end="")
	print(T)

print(tmp)