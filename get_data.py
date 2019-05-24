import numpy as np

class NRODataReduction:
	def __init__(self):
		self.channel = 0
		self.freq = 0
		self.T = 0
		self.filename = ""
		self.mode = 0



	def get_data(self):
		if 'p' in self.mode:
			print("------------------------------")
			print("Parameter   >    " + "len(self.channel) = ", end = "")
			print(len(self.channel))
			print("Parameter   >    " + "len(self.freq) = ", end = "")
			print(len(self.freq))
			print("Parameter   >    " + "len(self.T) = ", end = "")
			print(len(self.T))
			print("Parameter   >    " + "self.filename = ", end = "")
			print(self.filename)

		try:
			with open(self.filename) as f:
				line = f.readlines()

			for data in line:
				tmp = data.split()

				if 'd' in self.mode:
					print("------------------------------")
					print("DebagMode  >    data : ", end="")
					print(data, end = "")
					print("DebagMode  >    len(tmp) = ", end="")
					print(len(tmp))
					print("DebagMode  >    tmp = ", end="")
					print(tmp)


				if len(tmp) > 1 and tmp[0].isnumeric():
					if 'd' in self.mode:
						print("------------------------------")
						print("DebagMode  >    !!!found data!!!")
						print("DebagMode  >    channel = ", end="")
						print(tmp[0])
						print("DebagMode  >    freq = ", end="")
						print(tmp[1])
						print("DebagMode  >    T = ", end="")
						print(tmp[2])
					self.channel.append(tmp[0])
					self.freq.append(tmp[1])
					self.T.append(tmp[2])

						
				# del tmp
			if 's' in self.mode:
				print("------------------------------")
				for i in range(0, len(self.channel)):
					print("Data > " + self.channel[i] + "    " + self.freq[i] +  "    " + self.T[i])
				

		except AttributeError as e:
			print("##############################")
			print(e)
			print("parameter is bellow!")
			print("channel = " + self.channel)
			print("len(freq) = " + len(self.freq))
			print("len(T) = " + len(self.T))
			print("filename = " + self.filename)
			print("mode = " + self.mode)
			print("##############################")
			return -1
		except EOFError as e:
			print("##############################")
			print(e)
			print("parameter is bellow!")
			print("channel = " + self.channel)
			print("len(freq) = " + len(self.freq))
			print("len(T) = " + len(self.T))
			print("filename = " + self.filename)
			print("mode = " + self.mode)
			print("##############################")
		except KeyboardInterrupt as e:
			print("##############################")
			print(e)
			print("parameter is bellow!")
			print("channel = " + self.channel)
			print("len(freq) = " + len(self.freq))
			print("len(T) = " + len(self.T))
			print("filename = " + self.filename)
			print("mode = " + self.mode)
			print("##############################")
		else:
			return 0


