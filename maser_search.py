from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np

import matplotlib.pyplot as plt

def find(x, y, peak, snr, width)
	MADFM = madfm(y)

	y2 = []



	for channel in len(x)
		if y[channel] >= snr * MADFM
			peak.append(x[channel])
