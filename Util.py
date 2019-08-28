import sys
import codecs
import numpy as np
import statistics
import math
import traceback
import inspect
import datetime

class pycolor:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    END = '\033[0m'
    BOLD = '\038[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE = '\033[07m'


################
# ユーティリティ #
################

# 文字列検索（主にコマンドラインから引数を受け取る用）
def option_index(l, x, default = ""):
    # 戻り値は検索文字の次の値
    # l: 検索対象のリスト
    # x: 検索文字
    # default: 検索した値がなかったときの戻り値
    # 使い方: コマンドラインに"*** -fname test"という入力をすると以下のようにして"test"という値を得られる
    # args = sys.argv
    # filename = Util.option_index(args, '-fname')
    if x in l:
        if not '-' in l[l.index(x) + 1]:
            return l[l.index(x) + 1]
        else:
            raise IndexError
    else:
        return default

# パラメーター表示（変数名に.を含むものに使うと変数名が???になる）
def chkprint(*args):  # For Debag, show value
    names = {id(v): k for k, v in inspect.currentframe().f_back.f_locals.items()}
    print(str(inspect.currentframe().f_back.f_lineno).zfill(4) + ":    " + '\n         '.join(names.get(id(arg), '???') + ' = ' + repr(arg) for arg in args))


def chklprint(*args):  # For Debag, show value length
    names = {id(v): k for k, v in inspect.currentframe().f_back.f_locals.items()}
    print(str(inspect.currentframe().f_back.f_lineno).zfill(4) + ":    len(" + '\n         len('.join(names.get(id(arg), '???') + ') = ' + str(len(arg)) for arg in args))

def chkprint2(val_name, val):
    print(str(inspect.currentframe().f_back.f_lineno).zfill(4) + ":    " + val_name + " = " + str(val))
def chklprint2(val_name, val):
    print(str(inspect.currentframe().f_back.f_lineno).zfill(4) + ":    len(" + val_name + ") = " + len(val))

# データの書き出し
def export_data(*args):
    # 第一引数: 書き出しファイルの名前（※リストで渡さない）
    # 第二引数: （※リストで渡さない）
    # 第三引数以降: 書き出したいデータ
    print(args[1], file=codecs.open(args[0], 'w', 'utf-8'))

    f = codecs.open(args[0], 'a', 'utf-8')

    for i in range(0, len(args[2])):
        for j in range(2, len(args)):
            print(args[j][i], file=f, end = "    ")
        print(file=f)

def export_ldata(*args):
    # 第一引数: 書き出しファイルの名前（※リストで渡さない）
    # 第二引数以降: 書き出したいデータ
    try:
        with open(args[0], mode = 'w') as f:
            for line in args[1:]:
                f.write('\n'.join([str(s) for s in line]) + "\n")
    except FileNotFoundError as e:
        print(">>>    " + e)
        raceback.print_exc()
        return False

#######
# 計算 #
#######

# MADFM
def madfm(x):
    try:
        tmp = [float(s) for s in x]

        med = float(statistics.median(tmp))
        med2 = []

        for i in tmp:
            med2.append(math.sqrt((i - med) * (i - med)))

        return statistics.median(med2) / 0.6744888
    except statistics.StatisticsError as e:
        return False



def datetime2mjd(t):
    datetime_mjd0 = datetime.datetime(1968,5,23,9,0,0)
    delta = t - datetime_mjd0
    return delta.total_seconds()/(24*60*60.0)

def datetime2mjs(t):
    datetime_mjd0 = datetime.datetime(1968,5,23,9,0,0)
    delta = t - datetime_mjd0
    return delta.total_seconds()

def mjd2datetime(mjd):
    deltaday = round(mjd,2) - 16140.625 # 2012/08/01 base
    year = 2012
    dmonth = int(deltaday//32)
    dday = int(deltaday//1)
    hour = int((deltaday-dday)//round(1.0/24.0,2))
    time = datetime.datetime(year, 8+dmonth, 1+dday, hour)
    return time

###########
# デバッグ #
###########
if __name__ == '__main__':
    time = datetime.datetime.now()
    print('Datetime:',time)
    print('MJD:',datetime2mjd(time))
    print('MJS:',datetime2mjs(time))