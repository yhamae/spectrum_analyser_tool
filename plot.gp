set terminal x11

filename = "i18286_H2O_181223.txt"
plot_start = 259
unset key

plot filename every ::plot_start using 1:3 with lines 
replot (424:0.03458)
replot (572:0.1937)
replot (577:0.11266)
replot (605:0.16792)
replot (620:0.17178)
replot (643:0.19093)
replot (684:0.199)
replot (697:0.44982)
replot (712:1.84134)
replot (723:1.87857)
replot (729:1.18619)
replot (739:2.27973)
replot (752:10.83474)
replot (761:9.74469)
replot (777:14.74951)
replot (800:2.15963)
replot (827:0.44077)
replot (839:0.92616)
replot (852:6.90286)
replot (962:0.97408)
replot (1039:1.73038)