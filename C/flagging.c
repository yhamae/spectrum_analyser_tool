//
//  flagging.c
//  ASAS
//
//  Created by 濱江勇希 on 2017/04/30.
//  Copyright © 2017年 濱江勇希. All rights reserved.
//

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <math.h>
#include "data_processing.h"
#include "flagging.h"


#define MAXLINE 1024



long double flagging(long double *data, long double sigma, long double *data_flagging, long double *frequency, long double sfreq, long double ffreq, int N, int IF, int start, int end, int range)
{



    int k = 0;
    int j = 0;
    int p = 0;
    int a = 0;
    int b = 0;
    int i = 0;
    int r = 200;
    int d = 0;
    int e = 0;
    int f = 0;
    long double c[8192] ={0};
    long double z[1] = {0};


	/*------------------------------
	フィッティング
	------------------------------*/
    p = 4;  //字数
      j = 1;  //繰り返し
    
    for(k = 8; k <=8192 - 7 - range; k+= range)
    {
        
        sai(frequency, data, p, k, k + range, z, 2, 0);

            sai_2(frequency, data, k, k + range, 3, a, b, 0);

//        data[7] = 0;
//        for(i = k; i <= k + range; i++)
//        {
//            data[i] -= (data[k] - data[k - 1]);
//
//        }
     }
    d =k+1;
    e = k+1;
    while(isnan(data[e]) == 0)
    {
        e++;
    }
    sai(frequency, data, p, d, e, z, 2, 0);
    
    sai_2(frequency, data, d, e, 3, a, b, 0);
		/*
		MADFM()

		for(i = 8;i <= 8192 -7; i++)
		{
			
			
			
		}
		*/
    return 0;
}
