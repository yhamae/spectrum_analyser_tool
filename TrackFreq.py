#! /usr/local/bin/Python3
import sys
import os
import traceback
import subprocess
import PeakSearcher
import math
from scipy import constants
from tqdm import tqdm
import Util as ut
import PeakSearcher
import numpy as np
import DataLoader
import matplotlib.pyplot as plt
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
        self.a = []
        self.b = []
        self.c = []
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
        self.thresholds_x = 5
        self.thresholds_y = 2
        self.a_x = []
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
        



        start_index = 0

        if "H2O" in self.ref_freq:
            self.reciver = "H22"
        if "SiO" in self.ref_freq:
            self.reciver = "H40"
        # ut.chkprint(self.flist)


        for file in self.flist:
            gp = DataLoader.GetPeak()
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


    def get_click_point(self):
        # try:
        plt.scatter(self.x, self.y, c=self.c, cmap='jet')
        plt.colorbar()

        a = plt.ginput(n=-1, mouse_add=1, mouse_pop=2, mouse_stop=3, timeout = 600)
        # n=-1でインプットが終わるまで座標を取得
        # mouse_addで座標を取得（左クリック）
        # mouse_popでUndo（右クリック）
        # mouse_stopでインプットを終了する（ミドルクリック）
        # print("click coordinate is berrow")
        for c, d in a:
            tmp = []
            count = 0
            for tmp_x, tmp_y, tmp_c in zip(self.time, self.raw_freq, self.raw_val):
                if math.fabs(c - tmp_x) <= self.thresholds_x and math.fabs(d - tmp_y) <= self.thresholds_y:
                    dr = (c - tmp_x) * (c - tmp_x) + (d - tmp_y) * (d - tmp_y)
                    tmp.append([tmp_x, tmp_y, tmp_c, dr])
                    count += 1
                    # break
                    
            if len(tmp) == 1:
                self.a.append(tmp[0][0:3])
                plt.scatter(tmp[0][0], tmp[0][1], c = 'black')
            elif count == 0:
                continue
            else:
                tmp_val = [tmp[i][3] for i in range(0, len(tmp))]
                j = tmp_val.index(min(tmp_val))
                self.a.append(tmp[j][0:3])
                plt.scatter(tmp[j][0], tmp[j][1], c = 'black')
            del tmp

        # plt.savefig('fig_test.png')
        plt.show()
        print(self.a)

        return True


    def analysis_peak(self):
        self.x = self.time
        self.y = self.raw_freq
        self.c = [math.log10(s) for s in self.raw_val]
        TrackingFrequently.get_click_point(self)
        # print(self.a)
        # print(self.a[0])
        # print(self.a[1])
        tmp_x = [self.a[i][0] for i in range(0, len(self.a))]
        tmp_y = [self.a[i][1] for i in range(0, len(self.a))]
        tmp_c = [math.log10(self.a[i][2]) for i in range(0, len(self.a))]
        tmp_f = []
        plt.scatter(tmp_x, tmp_y, c = tmp_c, cmap='jet')
        print("近似曲線")
        for i in range(0, 3):
            self.a_x.append(np.polyfit(tmp_x, tmp_y, i + 1))
            tmp_f.append(np.poly1d(self.a_x[i])(tmp_x))
            print(np.poly1d(self.a_x[i]))
            tmp_label =str(np.poly1d(self.a_x[i]))
            plt.plot(tmp_x, tmp_f[i], label=tmp_label)
        plt.legend()
        plt.colorbar()
        plt.show()


        return True
    
        


if __name__ == "__main__":
    # Usage: Python3 TrackFreq.py 天体名 分子名(H2O, SiOなど) テキストファイルを検索するディレクトリ 書き出すテキストファイルの名前 モード選択("-a"をつけると周波数方向の変化が図れる。付かないと計算しない)
    args = sys.argv
    tf = TrackingFrequently()
    tf.source_keywoed = args[1] + "_" + args[2] + "_"
    tf.source = args[1]  # 天体名
    tf.ref_freq = args[2]  # 分子名（H2O,SiOなど）
    tf.directory = args[3]  # ファイルを検索するディレクトリ
    tf.oname = args[4]  # 書き出すテキストファイルの名前
    result1 = tf.get_peak_data()
    if "-a" in args:  # 最後に-aをつけると計算モード
        result2 = tf.analysis_peak()
    else:
        result2 = True
    if result1 and result2:
        print(ut.pycolor.GREEN + "------------------------------")
        print("Program has correctly finished")
        print("------------------------------" + ut.pycolor.END)
    else:
        print(ut.pycolor.RED + "--------------------------------")
        print("Program has incorrectly finished")
        print("--------------------------------" + ut.pycolor.END)