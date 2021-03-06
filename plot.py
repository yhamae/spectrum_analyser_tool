#! /usr/local/bin/Python3
import traceback
import os
import statistics
import seaborn as sns
import numpy as np
import Util as ut
# import seaborn as sns
import matplotlib.pyplot as plt



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
        self.errx = []
        self.erry = []
        self.ymin = 0
        self.ymax = 0
        self.xrange = []
        self.yrange = []
        self.clabel = ""
        self.c = []
        self.uselim = False
        self.fontsize = 5
        self.ii = 0
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
        plt.figure(figsize=(int(self.f_size_x), int(self.f_size_x)), dpi=int(300))
        # sns.set()
        # sns.heatmap(self.data, annot=True)

        if self.uselim:
            plt.ylim(self.ymin,self.ymax)
        # print('aaa')
        plt.scatter(self.x1, self.y1, c=self.c, cmap='jet', s = 10)
        plt.title(os.path.splitext(self.fname)[0])
        plt.xlabel("date (yy.mm.dd)\nMJD [day]")
        plt.ylabel(self.y_label)

        # plt.set_clim(min(self.c), max(self.c))
        # plt.imshow(self.c)
        plt.title(self.title)
        # plt.legend()
        cbar = plt.colorbar()
        cbar.set_label(self.clabel)
        plt.xticks(list(plt.xticks())[0], [ut.mjd2datetime(int(s)).strftime("%y.%m.%d") + '\n' + str(s) for s in list(plt.xticks())[0]])
        # plt.show()
        plt.savefig(self.fname, bbox_inches = 'tight')
        plt.close()
        return True

    def make_fig(self):
        plt.figure(figsize=(int(self.f_size_x), int(self.f_size_x)), dpi=int(100))
        plt.xlim(self.xrange[0], self.xrange[1])
        plt.ylim(self.yrange[0], self.yrange[1])

    def line_and_errbar_plot(self):
        cmap = plt.get_cmap("tab20")
        plt.errorbar(self.x1, self.y1, yerr = self.erry, capsize=5, fmt='o',  ecolor=cmap(self.ii), color=cmap(self.ii))
        plt.plot(self.x1, self.y1, linewidth = float(self.line_width), label=self.label1, color = cmap(self.ii))

    def line_plot(self):
        plt.plot(self.x1, self.y1, linewidth = float(self.line_width), label=self.label1)

    def line_plot_ccolor(self):
        plt.plot(self.x1, self.y1, linewidth = float(self.line_width), label=self.label1, color = self.c)

    def set_label(self):
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.title(self.title)

    def save_fig(self):
        plt.legend()
        # plt.savefig(self.fname, bbox_inches = 'tight')
        plt.savefig(self.fname)
        plt.close()

    def show(self):
        plt.legend()
        plt.show()
        plt.close()



# スムージング用ヒストグラム
# fig = plt.figure(figsize=(6,8))
# ax1 = fig.add_subplot(111)
# atca_hist = ax1.hist(atb_, bins=20, histtype="step",color='black',linewidth=2,label='ATCA')
# model_hist = ax1.hist(msb_, bins=20,histtype='step',  color='blue',label='MODEL',linestyle='-.',linewidth=1.5)
# ax1.set_xlabel('Latitude (b)',fontsize=15)
# ax1.set_ylabel('Number of maser sources ',fontsize=15)
# plt.legend()
# plt.text(-2.1,35, r'${\rm R=19 kpc} $',fontsize=15,color='black')
# plt.text(-2.1,33, r'${\rm Scale \,height=200 pc} $',fontsize=15,color='black')
# plt.tick_params(labelsize=12)
# plt.savefig('../../Fig5.eps',dpi=300, transparent='true')
# plt.show()