import matplotlib.pyplot as plt
import math

# sin波の作成
x = [i for i in range(1, 100)]
y = [math.sin(0.1*i) for i in x]

def main():
    plt.plot(x, y)

    a = plt.ginput(n=-1, mouse_add=1, mouse_pop=3, mouse_stop=2)
    # n=-1でインプットが終わるまで座標を取得
    # mouse_addで座標を取得（左クリック）
    # mouse_popでUndo（右クリック）
    # mouse_stopでインプットを終了する（ミドルクリック）

    for c, d in a:
        print(c, d)
        plt.plot(c, d, "ro") # グラフ上に座標をマークする

    plt.savefig('fig_test.png')
    plt.show()

if __name__ == '__main__':
    main()
