//
//  data_processing.h
//  課題1 インクの拡散(シミュレーション物理学)
//
//  Created by 濱江勇希 on 2018/04/13.
//  Copyright © 2018年 濱江勇希. All rights reserved.
//

#ifndef data_processing_h
#define data_processing_h

long double sd(long double *data, int start, int end);
long double ave(long double *data, int start, int end);
long double med(long double *data, int start, int end, int IF);
long double MADFM(long double *data, int start, int end, int IF);
long double sai_2(long double *x, long double *y, int start, int end, long double snr, long double a, long double b, int mode);
void sai(long double *x,long double *y, int N, int start, int end, long double *d, int mode, long double snr);
long double GetRandom(int x);


#endif /* data_processing_h */
