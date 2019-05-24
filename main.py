import maser_search
import get_data




mode = "cpr"
# c: ステータスコードの表示
# p: パラメーター表示
# s: 読み込んだデータの表示	
# r: 計算結果の表示



nrodata = get_data.NRODataReduction()
nrodata.channel = []
nrodata.freq = []
nrodata.T = []
nrodata.filename = "i18286_H2O_181223.txt"
nrodata.mode = mode

result01 = nrodata.get_data()

# str型をfloat型に変換
channel = [int(s) for s in nrodata.channel]
freq = [float(s) for s in nrodata.freq]
T = [float(s) for s in nrodata.T]

if 'c' in mode:
	print("------------------------------")
	print("StatusCode >    " + "get_data() = ", end = "")
	print(result01)
if 'p' in mode:
	print("------------------------------")
	print("Parameter  >    " + "Number of vcalue")
	print("Parameter  >    " + "channel: ", end = "")
	print(len(channel))
	print("Parameter  >    " + "frequency: ", end = "")
	print(len(freq))
	print("Parameter  >    " + "value: ", end = "")
	print(len(T))



maser = maser_search.SpectrumSearcher()
maser.x = freq
maser.y = T
maser.peak = []
maser.snr = 3
maser.wifth = 4
maser.mode = mode
result02 = maser.find()


if 'c' in mode:
	print("------------------------------")
	print("status code >    " + "SpectrumSearcher(): ", end = "")
	print(result01)

# print("------------------------------")
# print("DebagMode   >    " + "", end = "")
# print("Parameter   >    " + "", end = "")
# print("status code >    " + "", end = "")
# print("ResultValue >    " + "", end = "")