#! /usr/local/bin/Python3
import sys
import os
import traceback
import subprocess
import PeakSearcher

from tqdm import tqdm
import YukiUtil as ut
import PeakSearcher
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
        
        self.rawdata = []
        self.raw_freq = []
        self.raw_val = []


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
            self.date = gp.date
            self.raw_freq = gp.peak_freq
            self.raw_val = gp.peak_val

            for freq, val in zip(self.raw_freq, self.raw_val):
                self.rawdata.append([self.date, freq, val])

            self.data_index[self.date] = [start_index, len(self.rawdata) - 1]

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
                tmp_date.append(self.rawdata[i][0])
                tmp_freq.append(self.rawdata[i][1])
                tmp_val.append(self.rawdata[i][2])
        except IndexError as e:
            print(e)
            exit()
        except TypeError as e:
            print(e)
            exit()

        header = "source = " + self.source + "\n"
        header += "\nMJD    Freq    Val"

        ut.export_data("out.txt", header, tmp_date, tmp_freq, tmp_val)
        # ut.export_data("out.txt", self.data[0], self.data[1], self.data[2])
        pl = plot.MyPlot()
        pl.x1 = tmp_date
        pl.y1 = tmp_freq
        pl.freq_tracking_plot()

    # def spectrum_cal(self):
    #     max_val = 




    def analysis_peak(self):
        sort()
        


if __name__ == "__main__":
    args = sys.argv
    tf = TrackingFrequently()
    tf.source = args[1]
    tf.directory = args[2]
    print(tf.get_peak_data())
