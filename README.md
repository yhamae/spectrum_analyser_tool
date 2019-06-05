#spectrum_analyser_tool

##使い方  
基本的にはLinuxコマンドと同じように`-`を使ってパラメーターを変更できる。  
コマンドライン上で`Python PeakSearcher.py -fname FileName -o OutputfFileName [option]`と実行する。`-fname`、`o`は必ず指定する。（ただし、-aを使ってあるディレクトリ内を一括で処理する場合は`-fname`は指定する必用はない）  
`[option]`は以下の通りになっている。  
-s SNR  
-W SmoothingWidth  
-o OutputPeakListFileName(引数に-aがある場合は、書き出されるファイル名はここで指定した名前の後に読み込んだファイル名がくる)  
-ws MaserSearchWidth(>maser width)  
-p PlotFielName(引数に-aがある場合は、書き出されるファイル名はここで指定した名前の後に読み込んだファイル名がくる)  
-a InputIirectory(これを指定した場合、-fname filenameは必要ない)  
-h 使い方の表示  
