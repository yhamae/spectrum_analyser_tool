import maser_search
import NRODataReduction
import YukiUtil
import sys
import os
import traceback
import plot
try:
    from tqdm import tqdm
    imp_tqdm = True
except ImportError as e:
    print()
    imp_tqdm = False

#########
# 初期値 #
#########
err_message  = "illegal option!"
usage  = "Usage: Python PeakSearcher -fname FileName -o OutputfFileName [option]\n"
usage += "        -s SNR\n"
usage += "        -W SmoothingWidth\n"
usage += "        -o OutputPeakListFileName(引数に-aがある場合は、書き出されるファイル名はここで指定した名前の後に読み込んだファイル名がくる)\n"
usage += "        -ws MaserSearchWidth(>maser width)\n"
usage += "        -p PlotFielName(引数に-aがある場合は、書き出されるファイル名はここで指定した名前の後に読み込んだファイル名がくる)\n"
usage += "        -a InputIirectory(これを指定した場合、-fname filenameは必要ない)\n"
usage += "        -h 使い方の表示\n"
default_mode = ""
default_filename = ""
default_snr = 3
default_width = 4
default_outfile = "out.txt"
default_iteration = 1
default_width2 = 8


#################
# Main Function #
#################
try:
    # オプションから引数を取得
    args = sys.argv
    mode = default_mode
    filename = YukiUtil.option_index(args, '-fname', default_filename)
    snr = float(YukiUtil.option_index(args, '-s', default_snr))
    width = int(YukiUtil.option_index(args, '-w', default_width))
    outfile = YukiUtil.option_index(args, '-o', default_outfile)
    iteration = int(YukiUtil.option_index(args, '-i', default_iteration))
    width2 = int(YukiUtil.option_index(args, '-ws', default_width2))
    plotname = YukiUtil.option_index(args, '-p')
    directory = YukiUtil.option_index(args, '-a') # 指定したディレクトリ内のすべてのファイルに対して実行
    if '-d'  in args: mode += "d"   # -d: デバッグモード
    if '-sc' in args: mode += "c"   # -sc: ステータスコードの表示
    if '-prm'  in args: mode += "p"   # -p: パラメーター表示
    if '-da' in args: mode += "s"   # -da: 読み込んだデータの表示  
    if '-r'  in args: mode += "r"   # -r: 計算結果の表示
    if '-b'  in args: mode += "b"   # -b: smoothing dataの書きだし
    if '-h'  in args:    # 使い方を表示
        print(usage)
        exit()
except IndexError as e:    # オプションの引数が存在しない場合
    print(err_message)
    print(usage)
    exit()
except ValueError as e:
    print(err_message)
    print(usage)
    exit()

if not directory == "":
    outflist = []
    filelist = os.listdir(directory)
    for i in range(0, len(filelist)):
        outflist.append(outfile + os.path.splitext(filelist[i])[0] + '.txt')

else :
    filelist = []
    outflist = []
    filelist.append(filename)
    outflist.append(outfile)

result = []
ErrFilelist = []

# for imp, out in tqdm(zip(filelist, outflist)):
if imp_tqdm:
    bar = tqdm(range(0, len(filelist)))
else:
    bar = range(0, len(filelist))

for i in bar:
    try:

        lresult = len(result)

        peak_channel = []
        peak_freq = []
        peak_T = []
        peak_snr = []

        # データの取得
        nrodata = NRODataReduction.GetNRO_onoff()
        nrodata.channel = []
        nrodata.freq = []
        nrodata.T = []
        nrodata.filename = directory + filelist[i]
        nrodata.mode = mode

        result.append(nrodata.get())

        # str型をfloat型に変換
        channel = [int(s) for s in nrodata.channel]
        freq = [float(s) for s in nrodata.freq]
        T = [float(s) for s in nrodata.T]



        if 'c' in mode:
            print("------------------------------\n" + "StatusCode >     " + "data() = " + str(result[0]))
        if 'p' in mode:
            print("----- Number of value -----")
            YukiUtil.chklprint(channel, freq, T)


        # 輝線の捜索
        maser = maser_search.SpectrumSearcher()
        maser.x = channel
        maser.y = T
        maser.peak = []
        maser.snr = snr
        maser.width = width
        maser.mode = mode
        maser.iteration = iteration
        maser.width2 = width2
        result.append(maser.find())

        try:
            MADFM = YukiUtil.madfm(T)
        except statistics.StatisticsError as e:
            if 'c' in mode:
                print("\n>>> " + str(e))
                traceback.print_exc()
                print("\n")


        for j in maser.peak:
            tmp_snr = float(T[j] / MADFM)
            peak_channel.append(channel[j])
            peak_freq.append(freq[j])
            peak_T.append(T[j])
            peak_snr.append(tmp_snr)
        # 単一のファイルのみの解析の場合の標準出力
        if directory == "":
            if len(maser.peak) != 0:
                print("----- peak channels is bellow -----")
                print(">>>   channel       Value         SNR")
                for i in maser.peak:
                    tmp_snr = float(T[i] / MADFM)
                    print('>>>     {0:>5}  {1:>10.9}   {2:>9.6}'.format(channel[i], T[i], tmp_snr))
                print(">>>\n>>>    Number of peak: " + str(len(maser.peak)))
            else:
                print("#########################")
                print("Can not find peak channel")
                print("#########################")

        # 複数ファイルを解析するときの標準出力
        elif 'c' in mode:
            print(">>>    " + "find " + str(len(maser.peak)) + " peaks in " + filelist[i])

        # 書き出し
        exp_header  = "Rawfile name     = " + filelist[i] + "\n"
        exp_header += "Number of peak   = " + str(len(maser.peak)) + "\n" 
        exp_header += "smoothing width  = " + str(width) + "\n" 
        exp_header += "SNR              = " + str(snr) + "\n" 
        exp_header += "Output File name = " + outfile + "\n" 
        exp_header += "rms (by MADFM)   = " + str(MADFM) + "\n" 
        exp_header += "filelist[i]ut command    = $ Python3 " + ' '.join(args) + "\n" 
        exp_header += "\nchannel    freq    val    snr"    # ヘッダー情報
        YukiUtil.export_data(outflist[i], exp_header, peak_channel, peak_freq, peak_T, peak_snr)


        if 'c' in mode:
            print("------------------------------\n" + "status code >    " + "SpectrumSearcher(): " + str(result[1]))

        if not plotname == "":
            plotpeak = plot.MyPlot()

            if not directory == "":

                plotpeak.fname = plotname + os.path.splitext(filelist[i])[0] + '.png'
                
            else:
                plotpeak.fname = plotname
            # print(plotpeak.fname)
            plotpeak.x1 = freq
            plotpeak.y1 = T
            plotpeak.x2 = peak_freq
            plotpeak.y2 = peak_T
            plotpeakrms = MADFM
            result.append(plotpeak.ExpPlot())



    except ValueError as e:
        if 'c' in mode:
            print(">>>can not find peaks for Err\n>>> " + str(e))
            traceback.print_exc()
        # エラーが起こったこととそのとき読み込んだファイルを記録
        if not len(result) == lresult + 3:
            for k in range(lresult, lresult + 3):
                result.append(False)
                ErrFilelist.append(filelist[i])


for status in result:
    if not status:
        print("--------------------------------")
        print("Program has incorrectly finished")
        print(str(len(ErrFilelist)) + " Error found")
        print("--------------------------------")
        print("<<< Err files is bellow >>>")
        print("- ", end = "")
        print('\n- '.join(ErrFilelist))
        exit()

print("------------------------------")
print("Program has correctly finished")
print("------------------------------")




