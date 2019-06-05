# spectrum_analyser_tool

## プログラムの構成  
このプログラムはメインとなる`PeakSearcher.py`の他に以下の4つのモジュールによって構成されている。  
- `maser_search.py`  
- `NRODataReduction.py`  
- `plot.py`  
- `YukiUtil.py`  
使用する際は、これらの5つのファイルを同じディレクトリに置いておく必要がある。  

## 使い方  
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

## 使用例  
    ###使用例1  
    ```
    Python3 PeakSearcher.py -o dir1 -s 4 -w 4 -ws 7 -a dir2 -p dir3/plot
    ```  
    この場合は、dir2の中にあるファイルを処理する。処理する際のSNRは4、スムージングの幅は4、ピークを検索する幅は7となっている。処理されたデータはテキスト形式のデータはdir1に書き出され、グラフはdir3に`plot****`という名前で書き出される。  
    ###使用例2  
    ```
    Python3 PeakSearcher.py -o test_data/out.txt -s 20 -w 4 -ws 7 -fname test_data/i18286_H2O_181223.txt -p test.png
    ```  
    この場合は、test_data/i18286_H2O_181223.txtというファイルを処理する。処理する際のSNRは20、スムージングの幅は4、ピークを検索する幅は7となっている。処理されたデータはテキスト形式のデータはtest_data/out.txtといった名前で書き出され、グラフはtest.pngという名前で書き出される。　　

## エラーについて  
プログラムが正常に処理を終え、終了した場合は、以下のメッセージが表示される。  
```
--------------------------------
Program has correctly finished
--------------------------------
```  
しかし、すべてのファイルに対して正常な処理を行えなかったり、ファイルの読み込みに失敗した場合は以下のメッセージが表示される。  
```
--------------------------------
Program has incorrectly finished
** Error found
--------------------------------
```  
1. 読み込めなかったファイルについて  
    読み込めなかったファイルは最後に`<<< Err files is bellow >>>`というメッセージの下に表示される。  
2. Progress Bar  
    このプログラムではプログレスバーを表示できるが、`tqdm`というモジュールを使う。もし、このモジュールがインストールされていない場合、"You Can't Use Progress Bar!"というメッセージが出るので、もし使いたかったらインストールしてください。