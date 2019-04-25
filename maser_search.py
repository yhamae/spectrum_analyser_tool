from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np

import matplotlib.pyplot as plt

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