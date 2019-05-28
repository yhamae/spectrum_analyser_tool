filename = "i18286_H2O_181223.txt"
peak_filename = "out.txt"
plot_start = 259
PeakFileHeader = 10

set terminal x11
set autoscale ymin
set autoscale ymax
set autoscale xmin
set autoscale xmax
set key
plot filename every ::plot_start using 1:3 with lines title "spectrum"
replot peak_filename every ::PeakFileHeader using 1:3 title "peak" pt 6 ps 3
replot 'smootiong_data.txt' every ::2 with lines title "smootiong"
