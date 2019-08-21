#! /usr/local/bin/Python3
import sys
import os
import traceback
import subprocess
import PeakSearcher
import math
from scipy import constants
# import scipy

from tqdm import tqdm
import YukiUtil as ut
import PeakSearcher
import numpy as np
import DataLoader
import plot


class TrackingFrequently:
    def __init__(self):
        self.source = []
        self.source_data = []
        self.directory = ""
        self.date = []
        self.array = []
        self.x = []
        self.y = []
        self.peak_freq = []
        self.peak_val = []
        self.args = []
        self.debag = True
        self.flist = []
        self.peak_date = []
        self.data = []
        self.data_index = {}
        self.header_line = 10
        self.oname = ""
        
        self.rawdata = []
        self.raw_freq = []
        self.raw_val = []
        self.time = []
        self.flux = 1.7353787 / 0.61
        print(constants.value('Boltzmann constant') * 1E+26)


    # def get_parameter_by_args(self):
    #     pass:

    def get_peak_data(self):
        tmp_list = os.listdir(self.directory)
        for data in tmp_list:
            if self.source in data:
                self.flist.append(self.directory + data)
        if self.debag:
            ut.chkprint2("self.flist", self.flist)
        gp = DataLoader.GetPeak()
        gp.header_num = self.header_line


        start_index = 0

        for file in self.flist:
            gp.fname = file

            if self.debag:
                ut.chkprint(file)


            gp.get_peak()
            tmp_date = gp.date
            tmp_freq = gp.peak_freq
            tmp_val = gp.peak_val

            for freq, val in zip(tmp_freq, tmp_val):
                self.rawdata.append([float(tmp_date), float(freq), float(val) * self.flux])

            self.data_index[tmp_date] = [start_index, len(self.rawdata) - 1]

            # spectrum_cal()

            start_index = len(self.rawdata)

        # print(self.data[1709][1])
        if self.debag:
            ut.chkprint2("self.data_index", self.data_index)
            # ut.chkprint2("self.data", self.data)

        tmp_date = []
        tmp_freq = []
        tmp_val = []
        try:
            for i in range(0, len(self.rawdata)):
                self.time.append(float(self.rawdata[i][0]))
                self.raw_freq.append(float(self.rawdata[i][1]))
                self.raw_val.append(float(self.rawdata[i][2]))
                tmp_val.append(math.log10(float(self.rawdata[i][2])))
            # ut.chkprint(i)
        except IndexError as e:
            print(e)
            exit()
        except TypeError as e:
            print(e)
            exit()

        header = "source = " + self.source + "\n"
        header += "\nMJD    Freq    Val"

        ut.export_data(self.oname, header, self.time, self.raw_freq, self.raw_val)


        pl = plot.MyPlot()
        pl.data = np.array(self.rawdata)
        pl.x1 = self.time
        pl.y1 = self.raw_freq
        pl.c = tmp_val
        pl.y_label = "LSR[km/s]"
        pl.x_label = "MJD[day]"
        pl.title = os.path.splitext(self.oname)[0].split('/')[-1]
        pl.fname = os.path.splitext(self.oname)[0] + ".eps"
        pl.freq_tracking_plot()



        return True
    # def spectrum_cal(self):
    #     max_val = 


    def analysis_peak(self):
        sort()
        


if __name__ == "__main__":
    args = sys.argv
    tf = TrackingFrequently()
    tf.source = args[1]
    tf.directory = args[2]
    tf.oname = args[3]
    print(tf.get_peak_data())
