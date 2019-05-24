import sys

def my_index(l, x, default = ""):
    # l: 検索対象のリスト
    # x: 検索文字
    # default: 検索した値がなかったときの戻り値
    if x in l:
        return args[l.index(x) + 1]
    else:
        return default