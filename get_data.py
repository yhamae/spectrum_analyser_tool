import numpy as np

class data:
	def get_data(channel, freq, T, filename, mode):

		# mode = "d"
		try:
			with open(filename) as f:
				line = f.readlines()

			for data in line:
				tmp = data.split()

				if mode == "d":
					print("Debag_mode >    data : ", end="")
					print(data, end = "")
					print("Debag_mode >    len(tmp) = ", end="")
					print(len(tmp))
					print("Debag_mode >    tmp = ", end="")
					print(tmp)


				if len(tmp) > 1 and tmp[0].isnumeric():
					if mode == "d":
						print("Debag_mode >    !!!found data!!!")
						print("Debag_mode >    channel = ", end="")
						print(tmp[0])
						print("Debag_mode >    freq = ", end="")
						print(tmp[1])
						print("Debag_mode >    T = ", end="")
						print(tmp[2])
					channel.append(tmp[0])
					freq.append(tmp[1])
					T.append(tmp[2])

						
				# del tmp
			if mode == "d":
				for i in range(0, len(channel)):
					print(channel[i] + "    " + freq[i] +  "    " + T[i])
				

		except AttributeError as e:
			print(e)
			print("index err")
			return -1
		except EOFError as e:
			print(e)
			print("Filename: " + filename)
		except KeyboardInterrupt as e:
			print(e)
			print("fource quit!")
		else:
			return 0


