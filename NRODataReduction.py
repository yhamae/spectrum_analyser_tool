import numpy as np
import YukiUtil

class GetNRO_onoff:
    def __init__(self):
        self.channel = 0
        self.freq = 0
        self.T = 0
        self.filename = ""
        self.mode = 0



    def get(self):
        try:
            with open(self.filename) as f:
                line = f.readlines()

            for data in line:
                tmp = data.split()

                if len(tmp) > 1 and tmp[0].isnumeric():
                    if 'd' in self.mode:
                        print("------------------------------")
                        print('>>>     {0:>5}  {1:>10.9}  {1:>10.9}'.format(tmp[0], tmp[1], tmp[2]))
                    self.channel.append(tmp[0])
                    self.freq.append(tmp[1])
                    self.T.append(tmp[2])

                del tmp

            if 's' in self.mode:
                print("------------------------------")
                for i in range(0, len(self.channel)):
                    print("Data > " + self.channel[i] + "    " + self.freq[i] +  "    " + self.T[i])
                        

        except AttributeError as e:
            print(e)
            print("filename = " + self.filename)
            return False

        except EOFError as e:
            print(e)
            print("parameter is bellow!")
            print(">>>    channel = " + self.channel)
            print(">>>    len(freq) = " + len(self.freq))
            print(">>>    len(T) = " + len(self.T))
            print(">>>    filename = " + self.filename)
            return False
        else:
            return True


