import sys
import codecs
import numpy as np
import statistics
import math
import traceback
import inspect

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
    # filename = YukiUtil.option_index(args, '-fname')
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