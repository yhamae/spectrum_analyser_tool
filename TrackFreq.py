#! /usr/local/bin/Python3
import sys
import os
import traceback
import subprocess
import PeakSearcher
import math
from scipy import constants
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
        self.debag = False
        self.flist = []
        self.peak_date = []
        self.data = []
        self.data_index = {}
        self.header_line = 10
        self.oname = ""
        self.source_keywoed = ""
        self.reciver = "H22"
        self.rawdata = []
        self.raw_freq = []
        self.raw_val = []
        self.time = []
        self.r_ant = 45
        self.plottype = "eps"
        self.ref_freq = "H2O"
        self.aperture_efficiency = {"H22":0.61, "H40":0.55}


    # def get_parameter_by_args(self):
    #     pass:

    def get_peak_data(self):
        tmp_list = os.listdir(self.directory)
        for data in tmp_list:
            if self.source_keywoed in data:
                self.flist.append(self.directory + data)
        if self.debag:
            ut.chkprint2("self.flist", self.flist)
        print(">>> Load Data")
        print('- ' + '\n- '.join(self.flist))
        gp = DataLoader.GetPeak()
        gp.header_num = self.header_line


        start_index = 0

        if "H2O" in self.ref_freq:
            self.reciver = "H22"
        if "SiO" in self.ref_freq:
            self.reciver = "H40"


        for file in self.flist:
            gp.fname = file

            if self.debag:
                ut.chkprint(file)


            gp.get_peak()
            tmp_date = gp.date
            tmp_freq = gp.peak_freq
            tmp_val = gp.peak_val

            for freq, val in zip(tmp_freq, tmp_val):
                self.rawdata.append([float(tmp_date), float(freq), float(val) * 2 * constants.value('Boltzmann constant') * 1E+26 / (self.aperture_efficiency[self.reciver] * (self.r_ant / 2) * (self.r_ant / 2) * math.pi)])
                # 2k_b/A_e

            self.data_index[tmp_date] = [start_index, len(self.rawdata) - 1]

            # spectrum_cal()

            start_index = len(self.rawdata)

            del tmp_date, tmp_freq, tmp_val

        # print(self.data[1709][1])
        if self.debag:
            ut.chkprint2("self.data_index", self.data_index)
            # ut.chkprint2("self.data", self.data)


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

        header = "# source = " + self.source + "\n"
        header += "# molecule = " + self.ref_freq + "\n"
        header += "# Receiver = " + self.reciver + "\n"
        # header += "VakueAverage = " + str(sum(self.raw_val) / len(self.raw_val)) + "\n"
        header += "\n# MJD    Freq    Val"

        ut.export_data(self.oname, header, self.time, self.raw_freq, self.raw_val)


        pl = plot.MyPlot()
        pl.data = np.array(self.rawdata)
        pl.x1 = self.time
        pl.y1 = self.raw_freq
        pl.c = tmp_val
        pl.y_label = "LSR[km/s]"
        pl.x_label = "MJD[day]"
        pl.title = self.source + " " + self.ref_freq
        pl.fname = os.path.splitext(self.oname)[0] + "." + self.plottype
        pl.freq_tracking_plot()



        return True
    # def spectrum_cal(self):
    #     max_val = 


    def analysis_peak(self):
        sort()
        


if __name__ == "__main__":
    args = sys.argv
    tf = TrackingFrequently()
    tf.source_keywoed = args[1] + "_" + args[2] + "_"
    tf.source = args[1]  # 天体名
    tf.ref_freq = args[2]  # 分子名（H2O,SiOなど）
    tf.directory = args[3]  # ファイルを検索するディレクトリ
    tf.oname = args[4]
    if tf.get_peak_data():
        print(ut.pycolor.GREEN + "------------------------------")
        print("Program has correctly finished")
        print("------------------------------" + ut.pycolor.END)
    else:
        print(ut.pycolor.RED + "--------------------------------")
        print("Program has incorrectly finished")
        print("--------------------------------" + ut.pycolor.END)