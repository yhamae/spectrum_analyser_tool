set terminal x11

filename = "i18286_H2O_181223.txt"
plot_start = 259
unset key

plot filename every ::plot_start using 2:3 with lines 