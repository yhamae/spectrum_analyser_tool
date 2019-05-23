import maser_search
import get_data




mode = "d"

channel = []
freq = []
T = []

nrodata = get_data.NRODataReduction()
nrodata.channel = []
nrodata.freq = []
nrodata.T = []
nrodata.filename = "i18286_H2O_181223.txt"
nrodata.mode = mode

result01 = nrodata.get_data()

print("status code = " + result01)



maser = maser_search.SpectrumSearcher()

