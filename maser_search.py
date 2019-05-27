import numpy as np
import YukiUtil


class SpectrumSearcher:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.peak = 0
        self.snr  = 0
        self.width = 0
        self.mode = 0



    def find(self):
        try:
	
            
            x2 = []
            y2 = []
            tmp2 = []
            tmp3 = []

            

            # チャンネルを積分
            for j in range(0, len(self.x) - self.width - 1, self.width + 1):
                tmp = 0
                x2.append(j)
                for k in range(j, self.width + j):
                    tmp += self.y[k]
                y2.append(tmp)
            MADFM = YukiUtil.madfm(y2)
            if 'r' in self.mode:
                print("------------------------------")
                YukiUtil.chkprint(MADFM)

            # 輝線の山の部分を検索
            for j in range(1, len(y2) - 1):
                if y2[j] - y2[j - 1] > 0 and y2[j + 1] - y2[j] < 0:
                    tmp2.append(j)

            if 'r' in self.mode:
                print("------------------------------")
                YukiUtil.chklprint(tmp2)
                # print(tmp2)

            # yの値がしきい値以上のチャンネルを記録
            for channel_no in tmp2:
                if y2[channel_no] >= self.snr * MADFM :
                    tmp3.append(channel_no)
            # 輝線が見つからなかった場合通知
            if not tmp3:
                print("#########################")
                print("Can not find peak channel")
                print("#########################")


            # 輝線がある範囲の中で、最大値を記録
            for j in tmp3:
                tmp4 = []
                for k in range(j * self.width, j * self.width + self.width):
                    tmp4.append(self.y[k])

                peak_val = max(tmp4)
                l = tmp4.index(peak_val)
                self.peak.append(self.x[l + j * self.width - 1])
                del tmp4



            del x2, y2



        except OverflowError as e:
            # 計算中にオーバーフローが発生した場合
            print(e)
            return False
        except RecursionError as e:
            # 再帰処理の回数多過ぎ
            print(e)
            return False
        except ZeroDivisionError as e:
            # 0で割っている
            print(e)
            return False
        except IndexError as e:
        	print(e)
        	return False
        else:
        	return True

