import traceback
import numpy as np
import os
import statistics
import seaborn as sns
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
        self.snr = 0
        self.fname = "out.eps"
        self.f_size_x = 16
        self.f_size_y = 9
        self.dpi = 300
        self.line_width = 0.5
        self.x_label = "LSR[km/s]"
        self.y_label = "T[K]"
        self.title = ""
        self.label1 = "Spectrum"
        self.label2 = "RMS"
        self.label3 = ""
        self.data = []
        self.c = []
    def ExpPlot(self):
        
        
        plt.figure(figsize=(int(self.f_size_x), int(self.f_size_y)), dpi=int(self.dpi))
        plt.hlines(y=self.rms * self.snr, xmin=min(self.x1), xmax=max(self.x1), linewidth = float(self.line_width), label=self.label3, edgecolors='g')
        plt.hlines(y=self.rms, xmin=min(self.x1), xmax=max(self.x1), linewidth = float(self.line_width), linestyle='dashed', label=self.label2, edgecolors='g')
        plt.plot(self.x1, self.y1, linewidth = float(self.line_width), label=self.label1)
        plt.scatter(self.x2, self.y2, facecolors='none', edgecolors='r', linewidth = 0.5, s=100.0)
        plt.scatter(self.x2, self.y2, facecolors='none', edgecolors='r', linewidth = 1, s=1, marker = '.')
        # plt.rcParams['font.family'] ='Helvetica-Light'
        plt.title(self.title)
        # plt.subplots_adjust(1,1)
        plt.legend()
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)



        plt.savefig(self.fname, bbox_inches = 'tight')

        plt.close()

        return True


    def freq_tracking_plot(self):
        plt.figure(figsize=(int(self.f_size_x), int(self.f_size_x)), dpi=int(500))
        # sns.set()
        # sns.heatmap(self.data, annot=True)


        plt.scatter(self.x1, self.y1, c=self.c, cmap='jet', s = 10)
        plt.title(os.path.splitext(self.fname)[0])
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        # plt.set_clim(min(self.c), max(self.c))
        # plt.imshow(self.c)
        plt.title(self.title)
        plt.legend()
        plt.colorbar()
        # plt.show()
        plt.savefig(self.fname, bbox_inches = 'tight')
        plt.close()
        return True