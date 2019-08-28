
echo -e "\033[0;31mPeakSearcher\033[0;39m"
# Python3 PeakSearcher.py -o /Users/yhamae/OneDrive/astro/FLASHING/peak/ -s 4 -w 1 -ws 0 -a /Users/yhamae/OneDrive/astro/FLASHING/spectrum/



# echo SNR = 4
Python3 PeakSearcher.py -o /Users/yhamae/OneDrive/astro/FLASHING/peak/ -s 4 -w 1 -ws 0 -a /Users/yhamae/OneDrive/astro/FLASHING/spectrum/ -p /Users/yhamae/OneDrive/astro/FLASHING/plot/

echo -e "\033[0;31mTrackFreq\033[0;39m"
echo -e "\033[0;32mH2O\033[0;39m"
Python3 TrackFreq.py i18286 H2O /Users/yhamae/OneDrive/astro/FLASHING/peak/ /Users/yhamae/Desktop/FLASHING/i18286_H20.txt
Python3 TrackFreq.py i18251 H2O /Users/yhamae/OneDrive/astro/FLASHING/peak/ /Users/yhamae/Desktop/FLASHING/i18251_H20.txt
Python3 TrackFreq.py w43 H2O /Users/yhamae/OneDrive/astro/FLASHING/peak/ /Users/yhamae/Desktop/FLASHING/w43_H20.txt
Python3 TrackFreq.py oh16 H2O /Users/yhamae/OneDrive/astro/FLASHING/peak/ /Users/yhamae/Desktop/FLASHING/oh16_H20.txt

echo -e "\033[0;32mSiOv3\033[0;39m"
Python3 TrackFreq.py i18286 SiOv3 /Users/yhamae/OneDrive/astro/FLASHING/peak/ /Users/yhamae/Desktop/FLASHING/i18286_SiOv3.txt
Python3 TrackFreq.py i18251 SiOv3 /Users/yhamae/OneDrive/astro/FLASHING/peak/ /Users/yhamae/Desktop/FLASHING/i18251_SiOv3.txt
Python3 TrackFreq.py w43 SiOv3 /Users/yhamae/OneDrive/astro/FLASHING/peak/ /Users/yhamae/Desktop/FLASHING/w43_SiOv3.txt
Python3 TrackFreq.py oh16 SiOv3 /Users/yhamae/OneDrive/astro/FLASHING/peak/ /Users/yhamae/Desktop/FLASHING/oh16_SiOv3.txt

echo -e "\033[0;32mSiOv2\033[0;39m"
Python3 TrackFreq.py i18286 SiOv2 /Users/yhamae/OneDrive/astro/FLASHING/peak/ /Users/yhamae/Desktop/FLASHING/i18286_SiOv2.txt
Python3 TrackFreq.py i18251 SiOv2 /Users/yhamae/OneDrive/astro/FLASHING/peak/ /Users/yhamae/Desktop/FLASHING/i18251_SiOv2.txt
Python3 TrackFreq.py w43 SiOv2 /Users/yhamae/OneDrive/astro/FLASHING/peak/ /Users/yhamae/Desktop/FLASHING/w43_SiOv2.txt
Python3 TrackFreq.py oh16 SiOv2 /Users/yhamae/OneDrive/astro/FLASHING/peak/ /Users/yhamae/Desktop/FLASHING/oh16_SiOv2.txt

echo -e "\033[0;32mSiOv1\033[0;39m"
Python3 TrackFreq.py i18286 SiOv1 /Users/yhamae/OneDrive/astro/FLASHING/peak/ /Users/yhamae/Desktop/FLASHING/i18286_SiOv1.txt
Python3 TrackFreq.py i18251 SiOv1 /Users/yhamae/OneDrive/astro/FLASHING/peak/ /Users/yhamae/Desktop/FLASHING/i18251_SiOv1.txt
Python3 TrackFreq.py w43 SiOv1 /Users/yhamae/OneDrive/astro/FLASHING/peak/ /Users/yhamae/Desktop/FLASHING/w43_SiOv1.txt
Python3 TrackFreq.py oh16 SiOv1 /Users/yhamae/OneDrive/astro/FLASHING/peak/ /Users/yhamae/Desktop/FLASHING/oh16_SiOv1.txt

echo -e "\033[0;32mSiOv0\033[0;39m"
Python3 TrackFreq.py i18286 SiOv0 /Users/yhamae/OneDrive/astro/FLASHING/peak/ /Users/yhamae/Desktop/FLASHING/i18286_SiOv0.txt
Python3 TrackFreq.py i18251 SiOv0 /Users/yhamae/OneDrive/astro/FLASHING/peak/ /Users/yhamae/Desktop/FLASHING/i18251_SiOv0.txt
Python3 TrackFreq.py w43 SiOv0 /Users/yhamae/OneDrive/astro/FLASHING/peak/ /Users/yhamae/Desktop/FLASHING/w43_SiOv0.txt
Python3 TrackFreq.py oh16 SiOv0 /Users/yhamae/OneDrive/astro/FLASHING/peak/ /Users/yhamae/Desktop/FLASHING/oh16_SiOv0.txt