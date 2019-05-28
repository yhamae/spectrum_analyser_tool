import maser_search
import NRODataReduction
import YukiUtil
import sys



# mode 詳細
# d: デバッグモード
# c: ステータスコードの表示
# p: パラメーター表示
# s: 読み込んだデータの表示    
# r: 計算結果の表示

try:
    # オプションから引数を取得
    args = sys.argv
    mode = YukiUtil.option_index(args, '-m', "")
    filename = YukiUtil.option_index(args, '-fname')
    snr = YukiUtil.option_index(args, '-s', 3)
    width = YukiUtil.option_index(args, '-w', 4)
    outfile = YukiUtil.option_index(args, '-o', "out.txt")

except IndexError as e:    # オプションの引数が存在しない場合
    print("illegal option")
    print("usage: Python3 PeakSearcher.py -fname filename -o 結果を書き出すファイルの名前　[-m 動作モード] [-s SNR] [-w smoothing width]")
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
maser.snr = float(snr)
maser.width = int(width)
maser.mode = mode
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
exp_header \
= "Rawfile name     = " + filename + "\n" \
+ "Number of peak   = " + str(len(maser.peak)) + "\n" \
+ "smoothing width  = " + str(width) + "\n" \
+ "SNR              = " + str(snr) + "\n" \
+ "Output File name = " + outfile + "\n" \
+ "rms (by MADFM)   = " + str(MADFM) + "\n" \
+ "imput command    = $ Python3 " + ' '.join(args) + "\n" \
+ "\n" \
+ "channel    freq    val    snr"    # ヘッダー情報
YukiUtil.export_data(outfile, exp_header, peak_channel, peak_freq, peak_T, peak_snr)


if 'c' in mode:
    print("------------------------------\n" + "status code >    " + "SpectrumSearcher(): " + str(result[1]))

if result[0] == True and result[1] == True:
    print("\n\n------------------------------")
    print("Program has correctly finished")
    print("------------------------------")


