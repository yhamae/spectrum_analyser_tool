#! /usr/local/bin/Python3
import sys
import os
import traceback
import subprocess
import PeakSearcher

def DLFile(url):
    print(">>>    Start download from " + url)
    inp = []
    inp.append("curl")
    inp.append("-O")
    inp.append(url)
    subprocess.call(inp)
    del inp

try:
    from tqdm import tqdm
    imp_tqdm = True
except ImportError as e:
    print(">>>    You Can't Use Progress Bar!")
    print(">>>    If you want to use progress bar, please install \"tqdm\"")
    print(">>>    Example Install Command: pip install tqdm")
    imp_tqdm = False

try:
    import YukiUtil
except ImportError as e:
    print("\"YukiUtil.py\" is not found")
    DLFile("https://raw.githubusercontent.com/yhamae/spectrum_analyser_tool/master/YukiUtil.py")
    import YukiUtil
try:

try:
    import PeakSearcher
except ImportError as e:
    print("\"PeakSearcher.py\" is not found")
    DLFile("https://raw.githubusercontent.com/yhamae/spectrum_analyser_tool/master/PeakSearcher.py")
    import PeakSearcher
try:

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
        self.flist - []
        self.peak_date = []
        self.data = []
        self.data_index = {}

    def get_parameter_by_args(self):
        pass:

    def get_peak_data(self):
        tmp_list = os.listdir(self.directory)
        for data in tmp_list
            if self.source in data:
                self.fist.append(self.directory + data)
        gp = DataLoader.GetPeak()
        gp.header_num = 7

        for file in self.flist:
            tmp = len(self.data)
            gp.filename = file
            gp.get_peak()
            self.peak_freq.append(gp.peak_freq)
            self.peak_val.append(gp.peak_val)
            self.data = 

            self.data_index[gp.date] = [tmp, len(self.data)]

            # for freq, val in zip(gp.peak_freq, gp.peak_val)
            #     self.data.append(freq, val)
        ftp = plot.MyPlot()

    def analysis_peak(self):
        sort()
        











if __name__ == "__main__":
    tf = TrackingFrequently()
