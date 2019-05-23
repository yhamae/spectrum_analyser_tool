import numpy as np

class NRODataReduction:
	def __init__(self):
		self.channel = 0
		self.freq = 0
		self.T = 0
		self.filename = ""
		self.mode = 0



	def get_data(self):

		# mode = "d"
		try:
			with open(self.filename) as f:
				line = f.readlines()

			for data in line:
				tmp = data.split()

				if self.mode == "d":
					print("Debag_mode >    data : ", end="")
					print(data, end = "")
					print("Debag_mode >    len(tmp) = ", end="")
					print(len(tmp))
					print("Debag_mode >    tmp = ", end="")
					print(tmp)


				if len(tmp) > 1 and tmp[0].isnumeric():
					if self.mode == "d":
						print("Debag_mode >    !!!found data!!!")
						print("Debag_mode >    channel = ", end="")
						print(tmp[0])
						print("Debag_mode >    freq = ", end="")
						print(tmp[1])
						print("Debag_mode >    T = ", end="")
						print(tmp[2])
					self.channel.append(tmp[0])
					self.freq.append(tmp[1])
					self.T.append(tmp[2])

						
				# del tmp
			if self.mode == "d":
				for i in range(0, len(self.channel)):
					print(self.channel[i] + "    " + self.freq[i] +  "    " + self.T[i])
				

		except AttributeError as e:
			print(e)
			print("index err")
			return -1
		except EOFError as e:
			print(e)
			print("Filename: " + self.filename)
		except KeyboardInterrupt as e:
			print(e)
			print("fource quit!")
		else:
			return 0


