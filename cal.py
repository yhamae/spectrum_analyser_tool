import numpy as np
import statistics
import math

def MADFM(x)
	med = statistics.median(x)

	for i in len(x)
		med2[i] = math.sqrt((x[i] - med) * (x[i] - med))

	return statistics.median(med2) / 0.6744888