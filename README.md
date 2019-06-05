#spectrum_analyser_tool

##使い方
```bash
Usage: Python PeakSearcher -fname FileName -o OutputfFileName [option]
        -s SNR
        -W SmoothingWidth
        -o OutputPeakListFileName(引数に-aがある場合は、書き出されるファイル名はここで指定した名前の後に読み込んだファイル名がくる)
        -ws MaserSearchWidth(>maser width)
        -p PlotFielName(引数に-aがある場合は、書き出されるファイル名はここで指定した名前の後に読み込んだファイル名がくる)
        -a InputIirectory(これを指定した場合、-fname filenameは必要ない)
        -h 使い方の表示
```