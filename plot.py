import traceback
import numpy as np
import os
try:
    import matplotlib.pyplot as plt
except ImportError as e:
    print(">>>    Not Found \"matplotlib\" in your computer")
    print(">>>    Please Enter Command: pip install matplotlib")
    exit()


class MyPlot:
    def __init__(self):
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0
        self.rms = 0
        self.fname = ""
        self.f_size_x = 16
        self.f_size_y = 9
        self.dpi = 120
        self.line_width = 0.5
        self.x_label = "LSR[km/s]"
        self.y_label = "T[K]"
    def ExpPlot(self):
        
        plt.figure(figsize=(int(self.f_size_x), int(self.f_size_y)), dpi=int(self.dpi))
        plt.plot(self.x1, self.y1, linewidth = float(self.line_width))
        plt.scatter(self.x2, self.y2, facecolors='none', edgecolors='r', linewidth = 0.5, s=100.0)
        # plt.rcParams['font.family'] ='Helvetica-Light'
        plt.title(os.path.splitext(self.fname)[0])
        # plt.subplots_adjust(1,1)
        # plt.legend()
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)



        plt.savefig(self.fname, bbox_inches = 'tight')

        plt.close()

        return True


    def freq_tracking_plot(self):
        plt.figure(figsize=(int(self.f_size_x), int(self.f_size_y)), dpi=int(self.dpi))
        plt.plot(self.x1, self.y1, linewidth = float(self.line_width))
        plt.title(os.path.splitext(self.fname)[0])
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.savefig(self.fname, bbox_inches = 'tight')
        plt.close()
        return True