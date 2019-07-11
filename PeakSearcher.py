#! /usr/local/bin/Python3
import sys
import os
import traceback
import subprocess

import YukiUtil
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

    def get_parameter_by_args(self):
        try:
            # オプションから引数を取得
            if '-h'  in self.args:    # 使い方を表示
                print(self.usage)
                exit()
            self.filename = YukiUtil.option_index(self.args, '-fname', self.filename)
            self.snr = float(YukiUtil.option_index(self.args, '-s', self.snr))
            self.width = int(YukiUtil.option_index(self.args, '-w', self.width))
            self.outfile = YukiUtil.option_index(self.args, '-o', self.outfile)
            self.iteration = int(YukiUtil.option_index(self.args, '-i', self.iteration))
            self.width2 = int(YukiUtil.option_index(self.args, '-ws', self.width2))
            self.plotname = YukiUtil.option_index(self.args, '-p')
            self.directory = YukiUtil.option_index(self.args, '-a') # 指定したディレクトリ内のすべてのファイルに対して実行
            if '-d'  in self.args: self.mode += "d"   # -d: デバッグモード
            if '-sc' in self.args: self.mode += "c"   # -sc: ステータスコードの表示
            if '-prm'  in self.args: self.mode += "p"   # -p: パラメーター表示
            if '-da' in self.args: self.mode += "s"   # -da: 読み込んだデータの表示  
            if '-r'  in self.args: self.mode += "r"   # -r: 計算結果の表示
            if '-b'  in self.args: self.mode += "b"   # -b: smoothing dataの書きだし
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
            # self.filelist = []
            # self.outflist = []
            self.filelist.append(self.filename)
            if not self.outfile == "":
                self.outflist.append(self.outfile)

    def find_peak(self):
        #################
        # Main Function #
        #################
        if not self.plotname == "": # -pオプションを使う場合
            try:
                import plot
            except ImportError as e:
                print("\"plot.py\" is not found")
                DLFile("https://raw.githubusercontent.com/yhamae/spectrum_analyser_tool/master/plot.py")
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

                if 'p' in self.mode:
                    YukiUtil.chkprint(nrodata.filename)

                self.result.append(nrodata.get_data())

                # str型をfloat型に変換
                channel = [int(s) for s in nrodata.channel]
                freq = [float(s) for s in nrodata.freq]
                T = [float(s) for s in nrodata.T]



                if 'c' in self.mode:
                    print("------------------------------\n" + "StatusCode >     " + "data() = " + str(self.result[0]))
                if 'p' in self.mode:
                    print("----- Number of value -----")
                    YukiUtil.chklprint(channel, freq, T)


                # 輝線の捜索
                maser = MaserSearch.SpectrumSearcher()
                maser.x = channel
                maser.y = T
                maser.z = T
                maser.peak = []
                maser.snr = self.snr
                maser.width = self.width
                maser.mode = self.mode
                maser.iteration = self.iteration
                maser.width2 = self.width2
                self.result.append(maser.find())
                maser.z = []
                


                self.remove_width = 10

                for j in range(0, len(channel), self.remove_width * self.width2):
                    count = 0
                    tmp = []
                    # tmp2 = []
                    for k in range(j, j + self.remove_width * self.width2):
                        if k == len(channel): break
                        tmp.append(T[k])
                        # tmp2.append(freq[k])
                        
                        if k + 1 in maser.peak:
                            # print(k)
                            count += 1
                    if count == 0:
                        maser.z.extend(tmp)
                        # xval.extend(tmp2)
                # print(maser.z)
                # YukiUtil.chklprint(maser.z)

                maser.peak = []
                self.result.append(maser.find())
                self.peak_list = maser.peak

                try:
                    MADFM = YukiUtil.madfm(maser.z)
                except statistics.StatisticsError as e: # Tに値が入っていない場合
                    if 'c' in self.mode:
                        print("\n>>> " + str(e))
                        traceback.print_exc()
                        print("\n")


                for j in maser.peak:
                    tmp_snr = float(T[j - 1] / MADFM)
                    peak_channel.append(channel[j - 1])
                    peak_freq.append(freq[j - 1])
                    peak_T.append(T[j - 1])
                    peak_snr.append(tmp_snr)
                    
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
                elif 'c' in self.mode:
                    print(">>>    " + "find " + str(len(maser.peak)) + " peaks in " + self.filelist[i])

                if not self.outfile == "":
                    # 書き出し
                    exp_header  = "Rawfile name     = " + self.filelist[i] + "\n"
                    exp_header += "date             = " + nrodata.date + "\n" 
                    exp_header += "Number of peak   = " + str(len(maser.peak)) + "\n" 
                    exp_header += "smoothing width  = " + str(self.width) + "\n" 
                    exp_header += "SNR              = " + str(self.snr) + "\n" 
                    exp_header += "Output File name = " + self.outfile + "\n" 
                    exp_header += "rms (by MADFM)   = " + str(MADFM) + "\n" 
                    exp_header += "self.filelist[i]ut command    = $ Python3 " + ' '.join(self.args) + "\n" 
                    exp_header += "\nchannel    freq    val    snr"    # ヘッダー情報
                    YukiUtil.export_data(self.outflist[i], exp_header, peak_channel, peak_freq, peak_T, peak_snr)


                if 'c' in self.mode:
                    print("------------------------------\n" + "status code >    " + "SpectrumSearcher(): " + str(self.result[1]))

                if not self.plotname == "":
                    plotpeak = plot.MyPlot()

                    if not self.directory == "":

                        plotpeak.fname = self.plotname + os.path.splitext(self.filelist[i])[0] + '.png'
                        
                    else:
                        plotpeak.fname = self.plotname
                    # print(plotpeak.fname)
                    plotpeak.x1 = freq
                    plotpeak.y1 = T
                    plotpeak.x2 = peak_freq
                    plotpeak.y2 = peak_T
                    plotpeak.rms = MADFM
                    plotpeak.snr = self.snr
                    self.result.append(plotpeak.ExpPlot())



            except ValueError as e:
                if 'c' in self.mode:
                    print(">>>can not find peaks for Err\n>>> " + str(e))
                    traceback.print_exc()
                # エラーが起こったこととそのとき読み込んだファイルを記録
                if not len(self.result) == lresult + 4:
                    self.Errfilelist.append(self.filelist[i])
                    for k in range(lresult, lresult + 4):
                        self.result.append(False)


        for status in self.result:
            if not status:
                print("--------------------------------")
                print("Program has incorrectly finished")
                print(str(len(self.Errfilelist)) + " Error found")
                print("--------------------------------")
                print("<<< Err files is bellow >>>")
                print("- ", end = "")
                print('\n- '.join(self.Errfilelist))
                exit()

        print("------------------------------")
        print("Program has correctly finished")
        print("------------------------------")



# Main処理
if __name__ == "__main__":
    p = PeakSearch()
    p.args = sys.argv
    p.get_parameter_by_args()
    p.find_peak()

    # peak_list = []
    # main(sys.argv, peak_list)



    