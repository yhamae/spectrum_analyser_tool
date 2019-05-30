import maser_search
import NRODataReduction
import YukiUtil
import sys
import os
import traceback

#########
# 初期値 #
#########
err_message  = "illegal option!"
usage = "usage: Python3 PeakSearcher.py -fname filename -o 結果を書き出すファイルの名前　[-m 動作モード] [-s SNR] [-w smoothing width] [-i iteration]"
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
    directory = YukiUtil.option_index(args, '-a') # 指定したディレクトリ内のすべてのファイルに対して実行
    if '-d'  in args: mode += "d"   # -d: デバッグモード
    if '-sc' in args: mode += "c"   # -sc: ステータスコードの表示
    if '-p'  in args: mode += "p"   # -p: パラメーター表示
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
        filelist[i] = directory + filelist[i]

else :
    filelist = []
    outflist = []
    filelist.append(filename)
    outflist.append(outfile)

result = []
ErrFilelist = []

for imp, out in zip(filelist, outflist):
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
        nrodata.filename = imp
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

        MADFM = YukiUtil.madfm(T)

        # 単一のファイルのみの解析の場合の標準出力
        if directory == "":
            if len(maser.peak) != 0:
                print("----- peak channels is bellow -----")
                print(">>>   channel       Value         SNR")
                for i in maser.peak:
                    tmp_snr = float(T[i] / MADFM)
                    print('>>>     {0:>5}  {1:>10.9}   {2:>9.6}'.format(channel[i], T[i], tmp_snr))
                    peak_channel.append(channel[i])
                    peak_freq.append(freq[i])
                    peak_T.append(T[i])
                    peak_snr.append(tmp_snr)
                print(">>>\n>>>    Number of peak: " + str(len(maser.peak)))
            else:
                print("#########################")
                print("Can not find peak channel")
                print("#########################")

        # 複数ファイルを解析するときの標準出力
        else:
            print(">>>    " + "find " + str(len(maser.peak)) + " peaks in " + imp)

        # 書き出し
        exp_header  = "Rawfile name     = " + filename + "\n"
        exp_header += "Number of peak   = " + str(len(maser.peak)) + "\n" 
        exp_header += "smoothing width  = " + str(width) + "\n" 
        exp_header += "SNR              = " + str(snr) + "\n" 
        exp_header += "Output File name = " + outfile + "\n" 
        exp_header += "rms (by MADFM)   = " + str(MADFM) + "\n" 
        exp_header += "imput command    = $ Python3 " + ' '.join(args) + "\n" 
        exp_header += "\n" 
        exp_header += "channel    freq    val    snr"    # ヘッダー情報
        YukiUtil.export_data(out, exp_header, peak_channel, peak_freq, peak_T, peak_snr)


        if 'c' in mode:
            print("------------------------------\n" + "status code >    " + "SpectrumSearcher(): " + str(result[1]))

    except ValueError as e:
        print(">>>can not find peaks for Err\n>>> " + str(e))
        traceback.print_exc()
        # エラーが起こったこととそのとき読み込んだファイルを記録
        if not len(result) == lresult + 2:
            for k in range(lresult, lresult + 2):
                result.append(False)
                ErrFilelist.append(imp)


for status in result:
    if not status:
        print("\n\n--------------------------------")
        print("Program has incorrectly finished")
        print(str(int(result.count(False) / 2)) + " Error found")
        print("--------------------------------\n")
        print("Err files")
        print('\n'.join(ErrFilelist))
        exit()

print("\n\n------------------------------")
print("Program has correctly finished")
print("------------------------------")




