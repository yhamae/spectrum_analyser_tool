#! /usr/local/bin/Python3
import sys
import os
import traceback
import subprocess
import math

import pandas as pd
from scipy import constants
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit 
import seaborn as sns
from sklearn.metrics import r2_score
sns.set() 
# %matplotlib inline

import PeakSearcher
import Util as ut
import DataLoader
import plot


class TrackingFrequently:
    def __init__(self):
        self.source = []
        self.source_data = []
        self.directory = ""
        self.date = []
        self.array = []
        self.maxfev = 1000
        self.x = []
        self.y = []
        self.a = []
        self.b = []
        self.c = []
        self.d = [1]
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
        self.ini = [1,1,1,1]
        self.print_load_data = True
        self.uselim = False
        self.ymin = 0
        self.ymax = 0


    # def get_parameter_by_args(self):
    #     pass:

    def get_peak_data(self):
        tmp_list = os.listdir(self.directory)
        for data in tmp_list:
            if self.source_keywoed in data:
                self.flist.append(self.directory + data)
        if self.debag:
            ut.chkprint2("self.flist", self.flist)
        if self.print_load_data:
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
            tmp_channel = gp.channel

            for freq, val , channel in zip(tmp_freq, tmp_val, tmp_channel):
                self.rawdata.append([float(tmp_date), int(channel), float(freq), float(val) * 2 * constants.value('Boltzmann constant') * 1E+26 / (self.aperture_efficiency[self.reciver] * (self.r_ant / 2) * (self.r_ant / 2) * math.pi), float(val)])
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
        tmp_raw_val = []
        tmp_raw_val_log10 = []
        try:
            for i in range(0, len(self.rawdata)):
                self.time.append(float(self.rawdata[i][0]))
                self.raw_freq.append(float(self.rawdata[i][2]))
                self.raw_val.append(float(self.rawdata[i][3]))
                tmp_raw_val.append(float(self.rawdata[i][4]))
                tmp_val.append(math.log10(float(self.rawdata[i][3])))
                tmp_raw_val_log10.append(math.log10(float(self.rawdata[i][4])))
            # ut.chkprint(i)
        except IndexError as e:
            print(e)
            exit()
        except TypeError as e:
            print(e)
            exit()

        header  = "# source   = " + self.source + "\n"
        header += "# molecule = " + self.ref_freq + "\n"
        header += "# Receiver = " + self.reciver + "\n"
        header += "# Ae       = " + str(self.aperture_efficiency[self.reciver] * (self.r_ant / 2) * (self.r_ant / 2) * math.pi) + "\n"
        # header += "VakueAverage = " + str(sum(self.raw_val) / len(self.raw_val)) + "\n"
        header += "\n# MJD[day]    LSR[km/s]    FluxDensity[Jy]    AntennaTemperature[K]"

        ut.export_data(self.oname, header, self.time, self.raw_freq, self.raw_val, tmp_raw_val)


        pl = plot.MyPlot()
        pl.data = np.array(self.rawdata)
        pl.x1 = self.time
        pl.y1 = self.raw_freq
        pl.uselim = self.uselim
        if pl.uselim:
            pl.ymin = self.ymin
            pl.ymax = self.ymax
        # フラックス密度
        pl.c = tmp_val
        pl.clabel = "Flux density (Common logarithms)"
        # アンテナ温度
        # pl.c = tmp_raw_val_log10
        # pl.clabel = "Antenna temperature (Common logarithms)"
        pl.y_label = "LSR[km/s]"
        pl.title = self.source + " " + self.ref_freq
        pl.fname = os.path.splitext(self.oname)[0] + "." + self.plottype
        pl.freq_tracking_plot()



        return True


    def get_click_point(self):
        # try:
        plt.scatter(self.x, self.y, c=self.c, cmap='jet')
        plt.xticks(list(plt.xticks())[0], [ut.mjd2datetime(int(s)).strftime("%y.%m.%d") for s in list(plt.xticks())[0]])
        # x_tics = list(plt.xticks())
        # plt.xticks(list(plt.xticks())[0], [ut.mjd2datetime(int(s)).strftime("%y.%m.%d") for s in list(plt.xticks())[0]])
        plt.colorbar()

        a = plt.ginput(n=-1, mouse_add=1, mouse_pop=2, mouse_stop=3, timeout = 600)
        # n=-1でインプットが終わるまで座標を取得
        # mouse_addで座標を取得（左クリック）
        # mouse_popでUndo（右クリック）
        # mouse_stopでインプットを終了する（ミドルクリック）
        # print("click coordinate is berrow")
        # print(a)
        
        for c, d in a:
            tmp = []
            count = 0
            for tmp_x, tmp_y, tmp_c in zip(self.x, self.y, self.c):
                if math.fabs(c - tmp_x) <= self.thresholds_x and math.fabs(d - tmp_y) <= self.thresholds_y:
                    dr = (c - tmp_x) * (c - tmp_x) + (d - tmp_y) * (d - tmp_y)
                    tmp.append([tmp_x, tmp_y, tmp_c, dr])
                    count += 1
                    # break
                    
            if len(tmp) == 1:
                self.a.append(tmp[0][0:3])
                plt.scatter(tmp[0][0], tmp[0][1], c = 'Magenta', marker='x')
            elif count == 0:
                continue
            else:
                tmp_val = [tmp[i][3] for i in range(0, len(tmp))]
                j = tmp_val.index(min(tmp_val))
                self.a.append(tmp[j][0:3])
                plt.scatter(tmp[j][0], tmp[j][1], c = 'Magenta', marker='x')
            del tmp

        plt.scatter([self.a[i][0] for i in range(0, len(self.a))], [self.a[i][0] for i in range(0, len(self.a))], color = 'red', marker = '1')
        

        # plt.savefig('fig_test.png')
        plt.show()
        # print(self.a)

        return True

    def sin_fit(self):
        # TrackingFrequently.get_click_point(self)
        tmp_x = [self.a[i][0] for i in range(0, len(self.a))]
        tmp_y = [self.a[i][1] for i in range(0, len(self.a))]
        # tmp_c = [math.log10(math.fabs(self.a[i][2])) for i in range(0, len(self.a))]
        # tmp_f = []
        # plt.scatter(tmp_x, tmp_y, c = tmp_c, cmap='jet')
        # x = np.array(tmp_x)
        x = np.linspace(min(tmp_x), max(tmp_x))
        # y = np.array(tmp_y)
        # print(x)



        def func1(X, a, b, c, d):
            tmp = []
            for val in X:
                # tmp.append(float(a) * math.sin(float(b) * float(val) + float(c)) + float(d))
                tmp.append(a * math.sin(val * 2 * math.pi / b + c) + d)
            return np.array(tmp)

        popt, pcov = curve_fit(func1,np.array(tmp_x), np.array(tmp_y), p0 = self.ini, maxfev = self.maxfev)
        # popt, pcov = curve_fit(func1,np.array(tmp_x), np.array(tmp_y))


        # tmp_sin = np.sin()
        ti = '$' + 'f_{(x)} = ' + str(np.round(popt[0], decimals=2)) + "sin(\\frac{2\\pi}{" + str(np.round(popt[1], decimals=2)) + "}x + " + str(np.round(popt[2], decimals=2)) + ") + " + str(np.round(popt[3], decimals=2)) + '$'
        # print(ti)
        # plt.plot(x, func1(x, popt[0], popt[1], popt[2], popt[3]), label = ti)
        # plt.legend()
        # plt.show()

        # s1=pd.Series(tmp_y)
        # s2=pd.Series(list(func1(tmp_x, popt[0], popt[1], popt[2], popt[3])))

        # # pandasを使用してPearson's rを計算
        # res=s1.corr(s2)   # numpy.float64 に格納される
        res = r2_score(tmp_y, list(func1(tmp_x, popt[0], popt[1], popt[2], popt[3])))

        return x, func1(x, popt[0], popt[1], popt[2], popt[3]), ti, popt[0], popt[1], popt[2], popt[3], res


    def linear_fit(self):
        # TrackingFrequently.get_click_point(self)
        # print(self.a)
        # print(self.a[0])
        # print(self.a[1])
        label = []
        tmp_x = [self.a[i][0] for i in range(0, len(self.a))]
        tmp_y = [self.a[i][1] for i in range(0, len(self.a))]
        # tmp_c = [math.log10(math.fabs(self.a[i][2])) for i in range(0, len(self.a))]
        tmp_f = []
        x = np.linspace(min(tmp_x), max(tmp_x))
        y = np.array(tmp_y)
        # plt.scatter(tmp_x, tmp_y, c = tmp_c, cmap='jet')
        ylist = []
        labels = []
        
        # print("近似曲線")
        for i in self.d:
            p1 = np.polyfit(np.array(tmp_x), y, i)
            self.a_x.append(p1)
            tmp_f.append(np.poly1d(p1)(x))
            # print(np.poly1d(selfっ.a_x[i]))
            # tmp_label =str(np.poly1d(self.a_x[i]))
            
            # type(p1)
            p1 = list(p1)
            # print(p1)
            tmp_label = ''
            for j in range(0,i + 1):
                if j == i:
                    tmp_label+= str(np.round(p1[j], decimals=2))
                else:
                    if i - j != 1:
                        tmp_var = str('$x^{0}$'.format(i - j))
                    else:
                        tmp_var = str('$x$')
                    tmp_label+= str(np.round(p1[j], decimals=2)) + tmp_var
                    if p1[j + 1] >= 0:
                        tmp_label += '+'
            # print(tmp_label)
            ylist.append(np.poly1d(p1)(x))
            # plt.plot(x, , label=)
            labels.append(tmp_label)

            label.append(tmp_label)
        # plt.legend()
        # plt.xticks(list(plt.xticks())[0], [ut.mjd2datetime(int(s)).strftime("%y.%m.%d") for s in list(plt.xticks())[0]])
        # plt.colorbar()
        # plt.show()


        return x, np.poly1d(p1)(x), labels

    def slide_fit(self):
        cal = CalVariation()
        data_key = list(self.data_index.keys())
        data_key.sort()
        
        print(data_key)

        # splot = plt.figure(figsize=(20,20))

        for i in range(0, len(data_key) - 1):
            cal = CalVariation()
            max_channel = 2048
            range_pm = 15
            range_max = range_pm
            range_min = -1 * range_pm
            a = [0] * max_channel
            b = [0] * max_channel
            x = [0] * (range_max - range_min + 1)
            y = [0] * (range_max - range_min + 1)
            # ut.chkprint(len(tf.rawdata))
            for j in range(0, len(self.rawdata)):
                # index_num = 
                if int(self.rawdata[j][1]) < max_channel:
                    # if int(tf.rawdata[j][1]) <= 1122:
                    if int(self.rawdata[j][2]) >= 0:
                        tmp = int(self.rawdata[j][1])
                    else:
                        tmp = 2048 - int(self.rawdata[j][1])
                    if float(self.rawdata[j][0]) == float(data_key[i]):
                        # print("!")
                        # ut.chkprint(tf.rawdata[i][3])
                        a[tmp] += float(self.rawdata[j][3])
                        a[int(self.rawdata[j][1])] = 1
                    if float(tf.rawdata[j][0]) == float(data_key[i + 1]):
                        # ut.chkprint(tf.rawdata[i][3])
                        b[tmp] += float(self.rawdata[j][3])
                        b[int(self.rawdata[j][1])] = 1
            # ut.chkprint(a, b)
            # print("date", end = ": ")
            # print((float(data_key[i + 1]) - float(data_key[i])))
            d = cal.minimum_difference(a, b, (float(data_key[i + 1]) - float(data_key[i])), range_min, range_max)
            delta_x = float(data_key[i + 1]) - float(data_key[i])
            # plt.figure()

            # ax = splot.add_subplot(len(data_key), 1, i + 1)
            
            # ax = splot.add_subplot(2, 1, 1)


            # sns.lineplot(x = [cal.data[i][0]for i in range(0, len(cal.data))], y =  [cal.data[i][1] for i in range(0, len(cal.data))], ax = ax)




            ut.chkprint(delta_x)
            plt.plot([cal.data[i][0]for i in range(0, len(cal.data))], [cal.data[i][1] for i in range(0, len(cal.data))])
            plt.title(data_key[i] + ' --> ' + data_key[i + 1])
            plt.grid(which='major',color='black',linestyle='-')
            plt.grid(which='minor',color='black',linestyle='-')
            plt.xticks(list(plt.xticks())[0], [ut.mjd2datetime(int(s)).strftime("%y.%m.%d") for s in list(plt.xticks())[0]])
            plt.show()
            
            for k in range(0, len(cal.data)):
                y[k] += cal.data[k][1] * 365.25 / delta_x
                x[k] = cal.data[k][0]
            for k in range(0, (range_max - range_min + 1)):
                if  y[k] == 0 and x[k] == 0:
                    x.pop(k)
                    y.pop(k)


            ut.chkprint(d)


        # plt.show()
        # ax = splot.add_subplot(len(data_key), 1, len(data_key))
        # ax = splot.add_subplot(2, 1, 2)
        # sns.lineplot(x = x, y = y, ax = ax)
        
        plt.plot(x, y)
        plt.grid(which='major',color='black',linestyle='-')
        plt.grid(which='minor',color='black',linestyle='-')
        plt.title('all')
        plt.legend()
        plt.show()

class CalVariation:
    def __init__(self):
        self.data = []


    def minimum_difference(self, a, b, delta_x, range_min, range_max):
        n = len(a)
        if len(a) != len(b):
            print('ERR')
        def f_1(x):
            count = 0
            for i in range(0, n):
                if a[i] != 0: count += 1
                if b[i] != 0: count += 1
            d = 0
            # print(n)
            # print(x)
            if x >= 0:
                for i in range(0, int(n) - int(x)):
                    d += math.fabs(float(a[i + int(x)]) - float(b[i]))
                return d / (int(n) - int(x))
            if x < 0:
                for i in range(0, int(n) + int(x)):
                    d += math.fabs(float(b[i - int(x)]) - float(a[i]))
                return d / (int(n) + int(x))



        # x = np.arange(-1 * int(n) + 1, int(n), 1)
        x = np.arange(range_min, range_max, 1)
        # print(x)

        y = [f_1(i) for i in x]
        


        f_min = min(y)
        x_min = x[y.index(f_min)]
        x = [365.25 * i / delta_x for i in x]
        for tmp_x, tmp_y in zip(x, y):
            self.data.append([tmp_x, tmp_y])
        


        # plt.plot(x, y, label='f(x)')
        # plt.xlim(-50, 50)
        # plt.ylim(0.3, 0.5)
        plt.grid(which='major',color='black',linestyle='-')
        plt.grid(which='minor',color='black',linestyle='-')

        # plt.legend()
        # plt.show()
        return x_min * 365.25 / delta_x
    def show(self):
        plt.legend()
        plt.show()


        
        


if __name__ == "__main__":
    # Usage: Python3 TrackFreq.py 天体名 分子名(H2O, SiOなど) テキストファイルを検索するディレクトリ 書き出すテキストファイルの名前 モード選択("-a"をつけると周波数方向の変化が図れる。付かないと計算しない)
    
    # Python3 GitHub/spectrum_analyser_tool/TrackFreq.py IRAS15193+31 H2O /Users/yhamae/OneDrive/astro/FLASHING/peak/ /Users/yhamae/OneDrive/astro/FLASHING/dynamic_spectrum/IRAS15193+31_H20.txt

    args = sys.argv
    tf = TrackingFrequently()
    # tf.source_keywoed = args[1] + "_" + args[2] + "_"
    tf.source = 'IRAS15193+31'  # 天体名
    tf.ref_freq = 'H2O'  # 分子名（H2O,SiOなど）
    tf.directory = '/Users/yhamae/OneDrive/astro/FLASHING/peak/'  # ファイルを検索するディレクトリ
    tf.oname = '/Users/yhamae/OneDrive/astro/FLASHING/dynamic_spectrum/IRAS15193+31_H20.txt'  # 書き出すテキストファイルの名前
    tf.source_keywoed = tf.source + "_" + tf.ref_freq + "_"
    tf.print_load_data = False
    tf.get_peak_data()
    tf.x = tf.time
    tf.y = tf.raw_freq
    tf.c = [math.log10(s) for s in tf.raw_val]
    tf.get_click_point()
    print(tf.a)

    # tf.x = tf.time
    # tf.y = t
    # f.raw_freq
    # tf.c = [math.log10(s) for s in tf.raw_val]

    # tf.thresholds_x = 10
    # tf.thresholds_y = 10
    # tf.x = tf.time
    # tf.y = tf.raw_val
    # tf.c = [math.log10(s) for s in tf.raw_freq]

    # result2 = tf.get_click_point()
    # print("get_peak_data() -->" + str(result1))
    # print("get_click_point() -->" + str(result2))
    # print("--------------------")
    # print(tf.a)


    # if "-a" in args:  # 最後に-aをつけると計算モード
    #     result2 = tf.analysis_peak()
    # if "-sin" in args:
    #     result2 = tf.sin_fitting()
    # if "-c" in args:  # 
    #     cal = CalVariation()
    #     data_key = list(tf.data_index.keys())
    #     data_key.sort()
        
    #     print(data_key)

    #     # splot = plt.figure(figsize=(20,20))

    #     for i in range(0, len(data_key) - 1):
    #         cal = CalVariation()
    #         max_channel = 2048
    #         range_pm = 15
    #         range_max = range_pm
    #         range_min = -1 * range_pm
    #         a = [0] * max_channel
    #         b = [0] * max_channel
    #         x = [0] * (range_max - range_min + 1)
    #         y = [0] * (range_max - range_min + 1)
    #         # ut.chkprint(len(tf.rawdata))
    #         for j in range(0, len(tf.rawdata)):
    #             # index_num = 
    #             if int(tf.rawdata[j][1]) < max_channel:
    #                 # if int(tf.rawdata[j][1]) <= 1122:
    #                 if int(tf.rawdata[j][2]) >= 0:
    #                     tmp = int(tf.rawdata[j][1])
    #                 else:
    #                     tmp = 2048 - int(tf.rawdata[j][1])
    #                 if float(tf.rawdata[j][0]) == float(data_key[i]):
    #                     # print("!")
    #                     # ut.chkprint(tf.rawdata[i][3])
    #                     a[tmp] += float(tf.rawdata[j][3])
    #                     a[int(tf.rawdata[j][1])] = 1
    #                 if float(tf.rawdata[j][0]) == float(data_key[i + 1]):
    #                     # ut.chkprint(tf.rawdata[i][3])
    #                     b[tmp] += float(tf.rawdata[j][3])
    #                     b[int(tf.rawdata[j][1])] = 1
    #         # ut.chkprint(a, b)
    #         # print("date", end = ": ")
    #         # print((float(data_key[i + 1]) - float(data_key[i])))
    #         d = cal.minimum_difference(a, b, (float(data_key[i + 1]) - float(data_key[i])), range_min, range_max)
    #         delta_x = float(data_key[i + 1]) - float(data_key[i])
    #         # plt.figure()

    #         # ax = splot.add_subplot(len(data_key), 1, i + 1)
            
    #         # ax = splot.add_subplot(2, 1, 1)


    #         # sns.lineplot(x = [cal.data[i][0]for i in range(0, len(cal.data))], y =  [cal.data[i][1] for i in range(0, len(cal.data))], ax = ax)




    #         ut.chkprint(delta_x)
    #         plt.plot([cal.data[i][0]for i in range(0, len(cal.data))], [cal.data[i][1] for i in range(0, len(cal.data))])
    #         plt.title(data_key[i] + ' --> ' + data_key[i + 1])
    #         plt.grid(which='major',color='black',linestyle='-')
    #         plt.grid(which='minor',color='black',linestyle='-')
    #         plt.show()
            
    #         for k in range(0, len(cal.data)):
    #             y[k] += cal.data[k][1] * 365.25 / delta_x
    #             x[k] = cal.data[k][0]
    #         for k in range(0, (range_max - range_min + 1)):
    #             if  y[k] == 0 and x[k] == 0:
    #                 x.pop(k)
    #                 y.pop(k)


    #         ut.chkprint(d)


    #     # plt.show()
    #     # ax = splot.add_subplot(len(data_key), 1, len(data_key))
    #     # ax = splot.add_subplot(2, 1, 2)
    #     # sns.lineplot(x = x, y = y, ax = ax)
        
    #     plt.plot(x, y)
    #     plt.grid(which='major',color='black',linestyle='-')
    #     plt.grid(which='minor',color='black',linestyle='-')
    #     plt.title('all')
    #     plt.legend()
    #     plt.show()
        



    #     result2 = True
    # else:
    #     result2 = True
    # if result1 and result2:
    #     print(ut.pycolor.GREEN + "------------------------------")
    #     print("Program has correctly finished")
    #     print("------------------------------" + ut.pycolor.END)
    # else:
    #     print(ut.pycolor.RED + "--------------------------------")
    #     print("Program has incorrectly finished")
    #     print("--------------------------------" + ut.pycolor.END)