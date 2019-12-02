#! /usr/local/bin/Python3
import sys
import os
import traceback
import subprocess
import statistics

import Util
import MaserSearch
import DataLoader

try:
    from tqdm import tqdm
    imp_tqdm = True
except ImportError as e:
    print(">>>    You Can't Use Progress Bar!")
    print(">>>    If you want to use progress bar, please install \"tqdm\"")
    print(">>>    Example Install Command: pip install tqdm")
    imp_tqdm = False


class PeakSearch:
    def __init__(self):
        self.args = []
        self.peak_list = []
        self.err_message  = "illegal option!"
        self.usage  = "Usage: Python PeakSearcher.py -fname FileName -o OutputfFileName [option]\n"
        self.usage += "        -s SNR\n"
        self.usage += "        -W SmoothingWidth\n"
        self.usage += "        -o OutputPeakListFileName (引数に-aがある場合は、書き出されるファイル名はここで指定した名前の後に読み込んだファイル名がくる)\n"
        self.usage += "        -ws MaserSearchWidth (>maser width)\n"
        self.usage += "        -p PlotFielName (引数に-aがある場合は、書き出されるファイル名はここで指定した名前の後に読み込んだファイル名がくる)\n"
        self.usage += "        -a InputIirectory (これを指定した場合、-fname filenameは必要ない)\n"
        self.usage += "        -h 使い方の表示\n"
        self.mode = ""
        self.filename = ""
        self.snr = 5
        self.width = 4
        self.outfile = ""
        self.iteration = 1
        self.width2 = 7
        self.plotname = ""
        self.result = []
        self.Errfilelist = []
        self.filelist = []
        self.outflist = []
        self.directory = ""
        self.debag = False

    def get_parameter_by_args(self):
        try:
            # オプションから引数を取得
            if '-h'  in self.args:    # 使い方を表示
                print(self.usage)
                exit()
            self.filename = Util.option_index(self.args, '-fname', self.filename)
            self.snr = float(Util.option_index(self.args, '-s', self.snr))
            self.width = int(Util.option_index(self.args, '-w', self.width))
            self.outfile = Util.option_index(self.args, '-o', self.outfile)
            self.iteration = int(Util.option_index(self.args, '-i', self.iteration))
            self.width2 = int(Util.option_index(self.args, '-ws', self.width2))
            self.plotname = Util.option_index(self.args, '-p')
            self.directory = Util.option_index(self.args, '-a') # 指定したディレクトリ内のすべてのファイルに対して実行
            if '-d'  in self.args: self.debag = True   # -d: デバッグモード
        except IndexError as e:    # オプションの引数が存在しない場合
            print(self.err_message)
            print(self.usage)
            return False
        except ValueError as e: # オプションの引数が間違っている場合
            print(self.err_message)
            print(self.usage)
            return False

        if not self.directory == "": # -aオプションを使った場合
            # self.outflist = []
            self.filelist = os.listdir(self.directory)
            if not self.outfile == "":
                for i in range(0, len(self.filelist)):
                    self.outflist.append(self.outfile + os.path.splitext(self.filelist[i])[0] + '.txt')

        else : # -aオプションを使う場合
            self.filelist.append(self.filename)
            if not self.outfile == "":
                self.outflist.append(self.outfile)

        return True

    def find_peak(self):
        #################
        # Main Function #
        #################
        if not self.plotname == "": # -pオプションを使う場合
            import plot
            

        if imp_tqdm: # tqdmモジュールが入っているかどうか
            bar = tqdm(range(0, len(self.filelist)))
        else:
            bar = range(0, len(self.filelist))

        for i in bar:
            if self.filelist[i][0] == ".":
                continue
            try:


                lresult = len(self.result)
                peak_channel = []
                peak_freq = []
                peak_T = []
                peak_snr = []


                # データの取得
                nrodata = DataLoader.GetSpectrum()
                nrodata.channel = []
                nrodata.freq = []
                nrodata.T = []
                nrodata.filename = self.directory + self.filelist[i]
                nrodata.mode = self.mode

                if self.debag:
                    Util.chkprint(nrodata.filename)

                self.result.append(nrodata.get_data())

                # --------------------ここから--------------------




                # str型をfloat型に変換
                channel = [int(s) for s in nrodata.channel]
                freq = [float(s) for s in nrodata.freq]
                T = [float(s) for s in nrodata.T]



                if self.debag:
                    print("------------------------------\n" + "StatusCode >     " + "data() = " + str(self.result[0]))
                    print("----- Number of value -----")
                    Util.chklprint(channel, freq, T)


                # 輝線の捜索
                maser = MaserSearch.SpectrumSearcher()
                maser.x = channel
                maser.y = T
                maser.z = T
                maser.peak = []
                maser.snr = self.snr * 1.5
                maser.width = self.width
                maser.mode = self.mode
                maser.iteration = self.iteration
                maser.width2 = self.width2
                self.result.append(maser.find())
                maser.z = []
                


                self.remove_width = 10

                if self.width2 == 0:
                    local_width = 1
                else:
                    local_width = self.width2

                maser.snr = self.snr

                for j in range(0, len(channel), self.remove_width * local_width):
                    count = 0
                    tmp = []
                    # tmp2 = []
                    for k in range(j, j + self.remove_width * local_width):
                        if k == len(channel): break
                        tmp.append(T[k])
                        # tmp2.append(freq[k])
                        
                        if k + 1 in maser.peak:
                            count += 1
                    if count == 0:
                        maser.z.extend(tmp)


                maser.peak = []
                self.result.append(maser.find())
                self.peak_list = maser.peak

                try:
                    MADFM = Util.madfm(maser.z)
                except statistics.StatisticsError as e: # Tに値が入っていない場合
                    print(e)
                    if self.debag:
                        print("\n>>> " + str(e))
                        traceback.print_exc()
                        print("\n")

                try:
                    for j in maser.peak:
                        tmp_snr = float(T[j - 1] / MADFM)
                        peak_channel.append(channel[j - 1])
                        peak_freq.append(freq[j - 1])
                        peak_T.append(T[j - 1])
                        peak_snr.append(tmp_snr)
                except IndexError as e:
                    self.result[len(self.result) - 1] = False
                    
                # 単一のファイルのみの解析の場合の標準出力
                if self.directory == "":
                    if len(maser.peak) != 0:
                        print("----- peak channels is bellow -----")
                        print(">>>   channel       Value         SNR")
                        for j in maser.peak:
                            tmp_snr = float(T[j - 1] / MADFM)
                            print('>>>     {0:>5}  {1:>10.9}   {2:>9.6}'.format(channel[j - 1], T[j - 1], tmp_snr))
                        print(">>>\n>>>    Number of peak: " + str(len(maser.peak)))
                    else:
                        print("#########################")
                        print("Can not find peak channel")
                        print("#########################")

                # 複数ファイルを解析するときの標準出力
                elif self.debag:
                    print(">>>    " + "find " + str(len(maser.peak)) + " peaks in " + self.filelist[i])

                if not self.outfile == "":
                    # 書き出し
                    try:
                        if len(peak_T) != 0:
                            tmp_ave = str(sum(peak_T) / len(peak_T))
                        tmp_med = str(statistics.median(peak_T))
                    except:
                        tmp_ave = "N/A"
                        tmp_med = "N/A"
                    exp_header  = "# Rawfile name     = " + self.filelist[i] + "\n"
                    exp_header += "# date             = " + str(nrodata.date) + "\n" 
                    exp_header += "# MJD              = " + str(nrodata.MJD) + "\n" 
                    exp_header += "# object name      = " + nrodata.object_name + "\n" 
                    exp_header += "# Number of peak   = " + str(len(maser.peak)) + "\n" 
                    exp_header += "# smoothing width  = " + str(self.width) + "\n" 
                    exp_header += "# SNR              = " + str(self.snr) + "\n" 
                    exp_header += "# Output File name = " + self.outflist[i] + "\n" 
                    exp_header += "# rms (by MADFM)   = " + str(MADFM) + "\n" 
                    exp_header += "# Peak Average     = " + tmp_ave + "\n" 
                    exp_header += "# Peak Median      = " + tmp_med + "\n"
                    exp_header += "# command          = $ Python3 " + ' '.join(self.args) + "\n" 
                    exp_header += "\n# channel    freq    val    snr"    # ヘッダー情報

                    tmp1 = self.outflist[i].split('/')
                    tmp2 = tmp1[-1].split('_')
                    if nrodata.object_name != 'N/A':
                        tmp2[0] = nrodata.object_name
                        tmp2 = '_'.join(tmp2)
                        tmp1[-1] = tmp2
                    else:
                        tmp1[-1] = 'nohead_' + tmp1[-1]
                        tmp2 = 'nohead_' + '_'.join(tmp2)
                        self.Errfilelist.append(self.filelist[i] + "  (Can not read header)")

                    out_filename = '/'.join(tmp1)

                    Util.export_data(out_filename, exp_header, peak_channel, peak_freq, peak_T, peak_snr)


                if self.debag:
                    print("------------------------------\n" + "status code >    " + "SpectrumSearcher(): " + str(self.result[1]))

                if not self.plotname == "":
                    plotpeak = plot.MyPlot()

                    if not self.directory == "":

                        plotpeak.fname = self.plotname + os.path.splitext(tmp2)[0] + '.png'
                        
                    else:
                        plotpeak.fname = self.plotname
                    # print(plotpeak.fname)
                    plotpeak.x1 = freq
                    plotpeak.y1 = T
                    plotpeak.x2 = peak_freq
                    plotpeak.y2 = peak_T
                    plotpeak.rms = MADFM
                    plotpeak.snr = self.snr
                    plotpeak.label2 = "RMS" + "(" + "σ=" + str(MADFM)[0:7] + ")"
                    plotpeak.label3 = str(self.snr) + "σ"
                    plotpeak.title = os.path.splitext(tmp2)[0]
                    self.result.append(plotpeak.ExpPlot())

                # 初期化    
                peak_channel = []
                peak_freq = []
                peak_T = []
                peak_snr = []

                # --------------------ここまで--------------------
                # 別のメソッドにする



            except ValueError as e:
                if self.debag:
                    print(">>>can not find peaks for Err\n>>> " + str(e))
                    traceback.print_exc()
                # エラーが起こったこととそのとき読み込んだファイルを記録
                if not len(self.result) == lresult + 4:
                    self.Errfilelist.append(self.filelist[i])
                    for k in range(lresult, lresult + 4):
                        self.result.append(False)


        for status in self.result:
            if not status:
                return False

        
        return True



# Main処理
if __name__ == "__main__":
    p = PeakSearch()
    p.args = sys.argv
    p.get_parameter_by_args()
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
