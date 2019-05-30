import numpy as np
import YukiUtil
import traceback
import codecs

class GetNRO_onoff:
    def __init__(self):
        self.channel = 0
        self.freq = 0
        self.T = 0
        self.filename = ""
        self.mode = 0



    def get(self):
        try:
            with codecs.open(self.filename, 'r', 'utf-8', 'ignore') as f:
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
                        
        except FileNotFoundError as e:
            print(self.filename + ": No such file or directory")
            # print("\n\n>>> " + str(e))
            # traceback.print_exc()
            # print("\n\n")
            return e
        # except UnicodeDecodeError as e:
        #     print("\n\n>>> " + str(e))
        #     traceback.print_exc()
        #     print("\n\n")
        #     return e
        else:
            return True


