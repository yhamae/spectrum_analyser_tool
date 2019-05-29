import maser_search
import NRODataReduction
import YukiUtil
import sys


#########
# 初期値 #
#########
err_message  = "illegal option!\n"
err_message += "usage: Python3 PeakSearcher.py -fname filename -o 結果を書き出すファイルの名前　[-m 動作モード] [-s SNR] [-w smoothing width] [-i iteration]"
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
    if '-d'  in args: mode += "d"   # -d: デバッグモード
    if '-sc' in args: mode += "c"   # -sc: ステータスコードの表示
    if '-p'  in args: mode += "p"   # -p: パラメーター表示
    if '-da' in args: mode += "s"   # -da: 読み込んだデータの表示  
    if '-r'  in args: mode += "r"   # -r: 計算結果の表示
    if '-a'  in args: mode += "a"   # -r: 計算結果の表示
except IndexError as e:    # オプションの引数が存在しない場合
    print(usage)
    exit()
except ValueError as e:
    print(usage)
    exit()


result = []
peak_channel = []
peak_freq = []
peak_T = []
peak_snr = []


nrodata = NRODataReduction.GetNRO_onoff()
nrodata.channel = []
nrodata.freq = []
nrodata.T = []
nrodata.filename = filename
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
YukiUtil.export_data(outfile, exp_header, peak_channel, peak_freq, peak_T, peak_snr)


if 'c' in mode:
    print("------------------------------\n" + "status code >    " + "SpectrumSearcher(): " + str(result[1]))

if result[0] == True and result[1] == True:
    print("\n\n------------------------------")
    print("Program has correctly finished")
    print("------------------------------")


