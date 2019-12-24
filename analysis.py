# Python version 3 (and 2)
# Contents: vexファイルをndevice(pointing含む)に変換するスクリプト
# 
# Since(ver 1.0) : Nov, 2019
#                  Yuki Hamae

import sys
import os
import traceback
import subprocess
import statistics

import Util
import MaserSearch
import DataLoader
import PeakSearcher
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import os 
import math
from tqdm import tqdm
import Util as ut
import seaborn as sns
from DataLoader import GetSpectrum
import itertools

import TrackFreq

p = PeakSearcher.PeakSearch()
# p.args = ''

p.outfile = '../peak/'
p.snr = 4
p.width = 1
p.width2 = 0
p.directory = '../spectrum/'
p.plotname = '../plot/'
out_dynamic_dir = "../dynamic_spectrum/"
lower_v = [-400,-300]
upper_v = [300,400]
ref_freq_list = ['H2O', 'H2OR', 'H2OB', 'SiOv3', 'SiOv2', 'SiOv1', 'SiOv0']


# p.get_parameter_by_args()
p.set_prm()
if p.find_peak():
    print("------------------------------")
    print("Program has correctly finished")
    print("------------------------------")
else:
    print("--------------------------------")
    print("Program has incorrectly finished")
    print(str(len(p.Errfilelist)) + " Error found")
    print("--------------------------------")
    print("<<< Err files is bellow >>>")
    print("- ", end = "")
    print('\n- '.join(p.Errfilelist))
print('\n\n')


file_list = os.listdir(p.outfile)
source_list = []
for fname in file_list:
    if not fname.split('_')[0] in [source_list[i][0] for i in range(0, len(source_list))]:
        for val in ref_freq_list:
            source_list.append([fname.split('_')[0], val])

err_file = []

# os.chdir(p.outfile)
print('Detected High velocity Maser Component(' + str(lower_v[0]) + '~' + str(lower_v[1]) + ' or ' + str(upper_v[0]) + '~' + str(upper_v[1]) + ')')
for i in tqdm(range(0, len(source_list))):
    try:
        tf = TrackFreq.TrackingFrequently()
        tf.print_load_data = False
        tf.source = source_list[i][0]  # 天体名
        tf.ref_freq = source_list[i][1]  # 分子名（H2O,SiOなど）
        tf.directory = os.path.join(p.outfile)  # ファイルを検索するディレクトリ
        tf.oname = os.path.join(out_dynamic_dir + source_list[i][0] + '_' + source_list[i][1] + '.txt')  # 書き出すテキストファイルの名前
        tf.source_keywoed = source_list[i][0] + "_" + source_list[i][1] + "_"
        tf.get_peak_data()
        for val, time in zip(tf.raw_freq, tf.time):

            if lower_v[0] <= val <= lower_v[1] or upper_v[0] <= val <= upper_v[0]:
                tqdm.write(tf.source + ' ' + tf.ref_freq + ' : ' + str(val) + 'km/s observed in ' + str(ut.mjd2datetime(time).strftime("%y.%m.%d")))

    except:
        err_file.append(tf.oname)

print('Error File')
print('\n'.join(err_file))
