import maser_search




mode = "d"

channel = []
freq = []
T = []

result01 = get_data.data(channel, freq, T, "i18286_H2O_181223.txt", mode)
print(result01)

