#! /usr/local/bin/Python3
import codecs
import datetime
import sys
import traceback

import numpy as np

import Util as util



class GetSpectrum:
    def __init__(self):
        self.channel = 0
        self.freq = 0
        self.T = 0
        self.filename = ""
        self.mode = 0
        self.date = ""
        self.MJD = 0
        self.min = -50
        self.object_name = "N/A"



    def get_data(self):
        try:
            y = 0
            m = 0
            d = 0
            with codecs.open(self.filename, 'r', 'utf-8', 'ignore') as f:
                line = f.readlines()

            for data in line:
                tmp = data.split()
                if 'LAVST9( 1, 1) =integ start' in data:
                    y = int(data.split("=")[2].strip())
                if 'LAVST9( 2, 1) =integ start' in data:
                    m = int(data.split("=")[2].strip())
                if 'LAVST9( 3, 1) =integ start' in data:
                    d = int(data.split("=")[2].strip())
                if 'LAVST9( 4, 1) =integ start' in data:
                    hh = int(data.split("=")[2].strip())
                if 'LAVST9( 5, 1) =integ start' in data:
                    mm = int(data.split("=")[2].strip())
                if 'LAVST9( 6, 1) =integ start' in data:
                    ss = int(data.split("=")[2].strip())
                if 'OBJ9   = object name   =' in data:
                    self.object_name = data.split("=")[2].strip()

                if len(tmp) > 1 and tmp[0].isnumeric() and float(tmp[2]) >= self.min:
                    if 'd' in self.mode:
                        print("------------------------------")
                        print('>>>     {0:>5}  {1:>10.9}  {1:>10.9}'.format(tmp[0], tmp[1], tmp[2]))
                    self.channel.append(tmp[0])
                    self.freq.append(tmp[1])
                    self.T.append(tmp[2])

                del tmp
                

            if 's' in self.mode:
                print("------------------------------")
                for i in range(0, len(self.channel)):
                    print("Data > " + self.channel[i] + "    " + self.freq[i] +  "    " + self.T[i])
            if y != 0 and m != 0 and d != 0:
                self.date = datetime.datetime(y, m, d, hh, mm, ss)
                self.MJD = util.datetime2mjd(self.date)
            else:
                self.date = "N/A"
                self.MJD = "N/A"

                        
        except FileNotFoundError as e:
            print(self.filename + ": No such file or directory")
            # print("\n\n>>> " + str(e))
            # traceback.print_exc()
            # print("\n\n")
            return e
        # except UnicodeDecodeError as e:
        #     print("\n\n>>> " + str(e))
        #     traceback.print_exc()
        #     print("\n\n")
        #     return e
        if self.date != "N/A" and self.MJD != "N/A" and self.object_name != "N/A":
            return True
        else :return False
class GetPeak:
    def __init__(self):
        self.peak_freq = []
        self.peak_val = []
        self.fname = ""
        self.mode = ""
        self.header_num = 0
        self.date = 0

    def get_peak(self):
        try:
            with codecs.open(self.fname, 'r', 'utf-8', 'ignore') as f:
                line = f.readlines()
            for tmp in line:
                if 'MJD' in tmp:
                    self.date = tmp.split("=")[1].strip('\n')
                if tmp[0] != "#" and tmp[0] != "\n":
                    self.peak_freq.append(tmp.split()[1])
                    self.peak_val.append(tmp.split()[2])
                    
            # for i in range(0, len(line)):
            #     if line[i][0] != "#"
            #         tmp = line[i].split()
            #         self.peak_freq.append(tmp[1])
            #         self.peak_val.append(tmp[2])
                    # if 's' in self.mode:
                    #     util.chkprint(tmp[2], tmp[3])
            return True
        except FileNotFoundError as e:
            print(self.filename + ": No such file or directory")
            return False
if __name__ == "__main__":
    p = GetPeak()
    p.fname = sys.argv[1]
    p.header_num = 10
    p.get_peak()
    util.chkprint2("freq", p.peak_freq)
    util.chkprint2("val", p.peak_val)


