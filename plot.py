import traceback
import numpy as np
import os
try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError as e:
    print("Not Found \"matplotlib\" in your computer")
    print("Please Enter Command: pip install matplotlib")
    import matplotlib.pyplot as plt


class MyPlot:
    def __init__(self):
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0
        self.rms = 0
        self.fname = ""
    def ExpPlot(self):
        
        plt.figure(figsize=(16, 9), dpi=120)
        plt.plot(self.x1, self.y1, linewidth = 0.5)
        plt.scatter(self.x2, self.y2, facecolors='none', edgecolors='r', linewidth = 0.5, s=100.0)
        # plt.rcParams['font.family'] ='Helvetica-Light'
        plt.title(os.path.splitext(self.fname)[0])
        # plt.subplots_adjust(1,1)
        # plt.legend()
        plt.xlabel('LSR[km/s]')
        plt.ylabel('T[K]')



        plt.savefig(self.fname, bbox_inches = 'tight')

        plt.close()

        return True