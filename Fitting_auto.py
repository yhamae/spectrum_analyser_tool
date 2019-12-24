#!/usr/bin/env python
# coding: utf-8

# In[1]:


# %matplotlib notebook
# get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import matplotlib.pyplot as plt
import os 
import math
from tqdm import tqdm
import Util as ut
import seaborn as sns
import copy
from DataLoader import GetSpectrum
import itertools
import warnings

import TrackFreq


warnings.simplefilter('ignore')

# all_source = [['IRAS15193+31', 'H2O'], ['IRAS16552-30', 'H2O'], ['IRAS18251-10', 'H2O'], ['IRAS18460-01', 'H2O'], ['IRAS18596+03', 'H2O'], ['IRAS19134+21', 'H2O'], ['IRAS19190+11', 'H2O'], ['OH16.3-3.0-3.0', 'H2O'], ['OH16.3-3.0', 'H2O'], ['W43A', 'H2O']]
all_source = [['IRAS16552-30', 'H2O'], ['IRAS18251-10', 'H2O'], ['IRAS18460-01', 'H2O'], ['IRAS18596+03', 'H2O'], ['IRAS19134+21', 'H2O'], ['IRAS19190+11', 'H2O'], ['OH16.3-3.0-3.0', 'H2O'], ['OH16.3-3.0', 'H2O'], ['W43A', 'H2O']]
# all_source = [['IRAS16552-30', 'H2O']]
all_source = [['IRAS15193+31', 'SiOv0']]


out_dir = '/Users/yhamae/OneDrive/astro/FLASHING/fitting_result/'
in_dir = '/Users/yhamae/OneDrive/astro/FLASHING/dynamic_spectrum/'




max_task_num = len(all_source)
for num, source_list in enumerate(all_source):
    print('task ' + str(num + 1) + ' / ' + str(max_task_num) + ' : ' + source_list[0] + '(' + source_list[1] + ')')
    tf = TrackFreq.TrackingFrequently()


    # In[2]:
    try:


        def fit(x_label, y_label, c_label, point, ini, title, plot_flag = True):

            tf.d = [1]
            tf.ini = np.array(ini)
            tf.maxfev = 100000
            pol1d = []

            sns.set()
            tf.a = point

            raw_x = [tf.a[i][0] for i in range(0, len(tf.a))]
            raw_y = [tf.a[i][1] for i in range(0, len(tf.a))]
            raw_c = [math.log10(math.fabs(tf.a[i][2])) for i in range(0, len(tf.a))]



            x, pol1d, labels, p1, res = tf.linear_fit()
            
                # plt.show()
        #     fig.savefig('/Users/yhamae/Desktop/' + title + '.eps')
            return x, pol1d, labels, p1, res


        # In[3]:



        tf.oname = os.path.join(in_dir + source_list[0] + '_' + source_list[1] + '.txt')

        data = GetSpectrum.load_file(tf.oname)

        def sep_data(min_val, max_val):
            lim_data = []
            for lists in data:

                if min_val < float(lists[1]) < max_val:
                    lim_data.append(lists)
            return lim_data

#         lim_data = sep_data(-400, 400)
        lim_data = data
        max_d = 20
        if source_list[0] == 'IRAS15193+31':
            lim_data = sep_data(-400, 100)
            max_d = 10
 

        def sep_date(data):
            tmp = {}
            for lists in data:
                if not float(lists[0]) in tmp.keys():
                    tmp[float(lists[0])] = [[float(lists[0]), float(lists[1]), float(lists[2])]]
                else:
                    tmp[float(lists[0])].append([float(lists[0]), float(lists[1]), float(lists[2])])
            return tmp
        data = sep_date(lim_data)

        len_data = {}
        max_comb = 1
        for key in data:
            len_data[key] = len(data[key])
            max_comb *= len(data[key])
        # print(len_data)
        r2_list = []
        b_list = []
#         max_d = 0.5
        product = []
        bar = tqdm(total = max_comb)
        
        
        
        
        use_data = {}
        first_data = []
        tmp_max_key = 0
        tmp_max_val = 0
        for key in data.keys():
            val = [lis[1] for lis in data[key]]
            if (max(val) - min(val)) != 0:
                tmp = len(data[key]) / (max(val) - min(val))
            else:
                tmp = 0
            if tmp >= tmp_max_val:
                tmp_max_val = tmp
                tmp_max_key = key
        first_data = copy.copy(data[tmp_max_key])
        data.pop(tmp_max_key)
        

            
            
        print(first_data)
            
        for val in first_data:
            tmp_b_list = []
            tmp_r2_list = []
            
            for x in itertools.product(*data.values()):
                bar.update(1)
                # product.append(x)
                flag = True
    #             print(max_d)
                point1 = list(x)
                point1.append(val)
    #             print(point1)
                for i in range(1, len(point1)):
                    if math.fabs(point1[i][1] - point1[i - 1][1]) > max_d:
                        flag = False
                        break
                point = []
                if math.fabs(point1[1][1] - point1[0][1]) <= max_d:
                    point.append(point1[0])
    #             print(point)
                for i in range(1, len(point1) - 1):
                    if math.fabs(point1[i][1] - point1[i - 1][1]) <= max_d and math.fabs(point1[i][1] - point1[i + 1][1]) <= max_d:
                        point.append(point1[i])
    #             point = point1
    #             print(point)
                    # else:
                    #     if len(point) > 0 and math.fabs(point[-1][1] - point1[i][1]) <= 0.1:
                    #         point.append(point1[i])
    #             if flag:print(flag)
    #             if flag and len(point) >=3:
                if len(point) >=3:

    #                 print(point)
                    ini = [1,10000,10000,1]
                # x, np.poly1d(p1)(x), labels, p1
                    xres, yres, lab, result, r2 = fit('date(yy.mm.dd)\nMJD', 'LSR [km/s]', 'Flux Dencity [Jy]', point, ini, 'IRAS15193+31 sin Fitting (LSR)', False)
                #     print('IRAS15193+31 sin Fitting (LSR)')
    #                 print(result)
    #                 if r2 >= 0.6:
#                     if result[0] < 0.1 and r2>= 0.8:
                    if result[0] < 0.1:
    #                 if True: 
                        tmp_r2_list.append(r2)
                        tmp_b_list.append(result)
    #                     tqdm.write('R^2 = ' + str(r2) + ', a = ' + str(result[1]) + ', b = ' + str(result[0]))
                # print(max(r2_list))

                # result = [dict(zip(data.keys(), r)) for r in product]
                # print(result)
                # # for r in result:
                # #     print(r)
                del point, point1
            max_r2 = -1
            for a,b in zip(tmp_r2_list, tmp_b_list):
                if a >= max_r2:
                    max_r2 = a
                    max_b = b
                
            b_list.append(max_b)
            r2_list.append(max_r2)

        # In[ ]:
    except KeyboardInterrupt as e:
        # print(e)
        print('KeyboardInterrupt')
    tqdm.write(str(len(b_list)))
    def func1(X, a, b):
        tmp = []
        for val in X:
            # tmp.append(float(a) * math.sin(float(b) * float(val) + float(c)) + float(d))
            tmp.append(b * val + a)
        return np.array(tmp)
    fig = plt.figure(figsize = (16,24 ))
    ax1 = fig.add_subplot(1,1,1)
    mjd = [float(lim_data[i][0]) for i in range(0, len(lim_data))]
    lsr = [float(lim_data[i][1]) for i in range(0, len(lim_data))]
    flux = [math.log10(float(lim_data[i][2])) for i in range(0, len(lim_data))]
    x = np.linspace(min(mjd), max(mjd))
    im = ax1.scatter(mjd, lsr, c = flux, cmap = 'jet', s = 100)
    # plt.ylim(130,160)
    plt.xticks(list(plt.xticks())[0], [ut.mjd2datetime(int(s)).strftime("%y.%m.%d") + '\n' + str(s) for s in list(plt.xticks())[0]])
    ax1.set_ylabel('Flux Dencity [Jy]')
    ax1.set_xlabel('MJD')
    cbar = plt.colorbar(im)
    cbar.set_label('LSR [km/s]')
    for r2, lis in zip(r2_list, b_list):
    #     if r2 >= 0.7:
        ax1.plot(x, func1(x, lis[1], lis[0]))
    # plt.show()
    plt.savefig(out_dir + source_list[0] + '_' + source_list[1] + '.pdf')


        # In[ ]:


    import pandas as pd
    tmp = []
    for r2, lis in zip(r2_list, b_list):
        tmp.append([r2, lis[0], lis[1]])
    df = pd.DataFrame(tmp, columns=['r2', 'a', 'b'])
    df.to_csv(out_dir + source_list[0] + '_' + source_list[1] + '.csv')
    del r2_list, b_list, tmp
print("\007")