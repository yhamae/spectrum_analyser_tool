import numpy as np
import statistics
import math

def madfm(x):
    tmp = [float(s) for s in x]

    med = float(statistics.median(tmp))
    med2 = []

    for i in tmp:
        med2.append(math.sqrt((i - med) * (i - med)))

    return statistics.median(med2) / 0.6744888