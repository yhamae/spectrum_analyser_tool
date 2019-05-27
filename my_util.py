import sys
from inspect import currentframe

def my_index(l, x, default = ""):
    # l: 検索対象のリスト
    # x: 検索文字
    # default: 検索した値がなかったときの戻り値
    if x in l:
        return l[l.index(x) + 1]
    else:
        return default

def chkprint(*args):
    names = {id(v):k for k,v in currentframe().f_back.f_locals.items()}
    print(">>>    "+'\n>>>    '.join(names.get(id(arg),'???')+' = '+repr(arg) for arg in args))

def chklprint(*args):
    names = {id(v):k for k,v in currentframe().f_back.f_locals.items()}
    print(">>>    len("+'\n>>>    len('.join(names.get(id(arg),'???')+') = '+str(len(arg)) for arg in args))