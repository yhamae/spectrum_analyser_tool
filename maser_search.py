import numpy as np




class data:
	def read_file(channel, freq, T, filename, mode):

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


	def find(x, y, peak, snr, width):
	    

		try:

		    MADFM = madfm(y)
		    x1 = []
		    y2 = []
		    tmp2 = []
		    tmp3 = []

		    # チャンネルを積分
		    for j in range(0, len(x) - width - 1, width + 1):
		        tmp = 0
		        x2.append(j)
		        for k in range(j, width + j):
		            tmp += y[k]
		        y2.append(tmp)

		    # 輝線の山の部分を検索
		    for j in range(1, len(y2) - 1):
		    	if y2[j] - y2[j - 1] > 0 and y[j + 1] - y[j] < 0:
		    		tmp2.append(j)

		    # yの値がしきい値以上のチャンネルを記録
		    for channel_no in tmp2:
		        if y[channel_no] >= snr * MADFM:
		            tmp3.append(channel_no)
		    # 輝線が見つからなかった場合通知
		    if tmp3 == NULL:
		    	print("##### Can not find peak channel!#####")

		    # 輝線がある範囲の中で、最大値を記録
		    for j in tmp3:
		    	tmp4 = []
		    	for k in range(j * width, j * width + width):
		    		tmp3.append(y[k])
		    	max(tmp4)
		    	del tmp4



		    del x2, y2

		except OverflowError as e:
			# 計算中にオーバーフローが発生した場合
			print(e)
		except RecursionError as e:
			# 再帰処理の回数多過ぎ
			print(e)
		except ZeroDivisionError as e:
			# 0で割っている
			print(e)

class cal:
	def MADFM(x):
		med = statistics.median(x)

		for i in len(x):
			med2[i] = math.sqrt((x[i] - med) * (x[i] - med))

		return statistics.median(med2) / 0.6744888