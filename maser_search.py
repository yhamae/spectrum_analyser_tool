import numpy as np
import YukiUtil
import traceback
import statistics


class SpectrumSearcher:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.peak = 0
        self.snr  = 0
        self.width = 0
        self.mode = 0
        self.iteration = 0
        self.width2 = 0



    def find(self):
        try:
            i = 1
            while True:
                x2 = []
                y2 = []
                tmp2 = []
                tmp3 = []
                # チャンネルを積分
                if i != self.iteration or self.iteration == 1:
                    for j in range(0, len(self.x) - self.width, self.width):
                        tmp = 0
                        x2.append(self.x[j])
                        for k in range(j, self.width + j):
                            tmp += self.y[k]
                        y2.append(tmp)
                    # ↓後で消す
                    if 'b' in self.mode:
                        YukiUtil.export_data("smoothiong_data.txt", "channel    val", x2, y2)
                    # ↑後で消す
                else:
                    x2 = self.x
                    y2 = self.y

                MADFM = YukiUtil.madfm(y2)

                if 'r' in self.mode:
                    print("------------------------------")
                    YukiUtil.chkprint(MADFM)

                # 輝線の山の部分を検索
                # for j in range(1, len(y2) - 1):
                for j in range(1,len(y2) - 1):
                    # if j == 0 or j == len(self.x) - self.width: 
                    #     print(j)
                    #     continue
                    if y2[j] - y2[j - 1] > 0 and y2[j + 1] - y2[j] < 0:
                        tmp2.append(j)

                if 'r' in self.mode:
                    print("------------------------------")
                    YukiUtil.chklprint(tmp2)
                    # print(tmp2)

                count = 0
                # yの値がしきい値以上のチャンネルを記録
                for channel_no in tmp2:
                    if y2[channel_no] > self.snr * MADFM :
                        tmp3.append(channel_no)
                        count += 1

                # 輝線が見つからなかった場合通知
                # if count == 0:
                #     print("#########################")
                #     print("Can not find peak channel")
                #     print("#########################")


                # 輝線がある範囲の中で、最大値を記録
                range_list = []
                for j in tmp3:
                    tmp4 = []
                    if j * self.width + self.width2 <= len(self.y):
                        for k in range(j * self.width - self.width2, j * self.width + self.width2):
                            tmp4.append(self.y[k])
                            # range_list.append(k)

                        peak_val = max(tmp4)
                        range_list.append(peak_val)
                        l = tmp4.index(peak_val)
                        self.peak.append(self.x[l + j * self.width - self.width2 - 1])
                    del tmp4


                self.width -= 1

                del x2, y2

                if self.iteration <=1 or i == self.iteration:
                    # print(">>>    iteration: " + str(i))
                    break
                i += 1

            


        except OverflowError as e:
            print("\n>>> " + str(e))
            traceback.print_exc()
            print("\n")
            return False
        except ZeroDivisionError as e:
            print("\n>>> " + str(e))
            traceback.print_exc()
            print("\n")
            return False
        except statistics.StatisticsError as e:
            print("\n>>> " + str(e))
            traceback.print_exc()
            print("\n")
            return False
        # except NameError as e:
        #     print("\n\n>>> " + str(e))
        #     traceback.print_exc()
        #     print("\n\n")
        #     return e
        else:
            return True

        	

