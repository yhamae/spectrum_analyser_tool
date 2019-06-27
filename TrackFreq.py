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

    def get_peak_data(self):
        tmp2 = []
        tmp3 = []
        try:
            for file in self.source_data:
                with codecs.open(file, 'r', 'utf-8', 'ignore') as f:
                    tmp = data.split()
                    if len(tmp) == 8:
                        continue
                    for i in range(9, len(tmp))
                        tmp2.append(tmp[1])
                        tmp3.append(tmp[2])
                    self.peak_freq.append(tmp2)
                    self.peak_val.append(tmp3)
                    

            if self.debag:
                chkprint2("self.peak_freq", self.peak_freq)
                chkprint2("self.peak_val", self.peak_val)
            return True
        except FileNotFoundError as e:
            print(e)
            traceback.print_exc()
            return False
        except IndexError as e:
            print(e)
            traceback.print_exc()
            return False











if __name__ == "__main__":
    tf = TrackingFrequently()
