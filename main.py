import maser_search
import NRODataReduction
import my_util
import sys
import cal



# mode 詳細
# d: デバッグモード
# c: ステータスコードの表示
# p: パラメーター表示
# s: 読み込んだデータの表示    
# r: 計算結果の表示


# filename = "i18286_H2O_181223.txt"

try:
    # オプションから引数を取得
    args = sys.argv
    mode = my_util.my_index(args, '-m', "")
    filename = my_util.my_index(args, '-fname')
    snr = my_util.my_index(args, '-s', 3)
    width = my_util.my_index(args, '-w', 4)

except IndexError as e:    # オプションの引数が存在しない場合
    print("illegal option")
    print("usage: Python main.py -fname filename [-m 動作モード] [-s SNR] [-w smoothing width]")
    exit()




nrodata = NRODataReduction.GetNRO_onoff()
nrodata.channel = []
nrodata.freq = []
nrodata.T = []
nrodata.filename = filename
nrodata.mode = mode

result01 = nrodata.get()

# str型をfloat型に変換
channel = [int(s) for s in nrodata.channel]
freq = [float(s) for s in nrodata.freq]
T = [float(s) for s in nrodata.T]

if 'c' in mode:
    print("\n------------------------------\n" + "StatusCode >     " + "data() = " + str(result01))
if 'p' in mode:
    print("\n" + "----- Number of value -----")
    my_util.chklprint(channel, freq, T)



maser = maser_search.SpectrumSearcher()
maser.x = channel
maser.y = T
maser.peak = []
maser.snr = float(snr)
maser.width = int(width)
maser.mode = mode
result02 = maser.find()

MADFM = cal.madfm(T)

print("\n----- peak channels is bellow -----")
print(">>>   channel       Value         SNR")
for i in maser.peak:
    # print(">>>    ", end ="")
    # print(channel[i], end =", ")
    # print(T[i], end = ",  ")
    # print(T[i] / MADFM)
    tmp_snr = float(T[i] / MADFM)
    # print(tmp_snr)
    print('>>>     {0:>5}  {1:>10.9}   {2:>9.6}'.format(channel[i], T[i], tmp_snr))


if 'c' in mode:
    print("\n------------------------------\n" + "status code >    " + "SpectrumSearcher(): " + str(result01))
    

# print("------------------------------")
# print("DebagMode   >    " + "", end = "")
# print("Parameter   >    " + "", end = "")
# print("status code >    " + "", end = "")
# print("ResultValue >    " + "", end = "")