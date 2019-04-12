//
//  find.c
//  ASAS
//
//  Created by 濱江勇希 on 2017/10/20.
//  Copyright © 2017年 濱江勇希. All rights reserved.
//

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <math.h>
#include "data_processing.h"
#include "find.h"


long double find(long double *data, long double *freq, char find_filename[256], long double snr, long double max, int range)
{
    int i, j, k, l, m;
    long double a = 0;
    long double b = 0;
    long double sigma, average;
    long double SN;
    long double *f;
    long double fr;
    int g[8192] = {0};
    f = (long double*)malloc(sizeof(long double ) * range + 1);
  
    
    i =0;
    j = 0;
    k = 0;
    l = 0;
    m = 0;
    FILE *fp;
    
    fp = fopen(find_filename, "w");
    
        fprintf(fp, "Freqency,Real,signal-noise ratio\n");
    for(i = 8; i <= 8192 - 7 - range; i ++)
    {
        
        sai_2(freq, data, i, i + range, 3, a, b, 1);

        for(j = i; j <= i + range; j++)
        {
            
            f[j - i] = data[j] - (a * freq[j]) ;
            if(isnan(f[j - i] !=0))
            {
                printf("null\n");
            }
//            printf("%f\n",f[i]);
        }
        
        sigma = 0.6744888 * MADFM(f, 0, range, 0);
        average = ave(f, 0, range);

        
        for(j = i; j <= i + range; j++)
        {
            if(f[j - i] <= (max * sigma) + average)
            {

            if(f[j - i] >= (snr * sigma) + average)
            {
                modfl(freq[j], &fr);
                if(g[j] == 0)
                {
                SN = (f[j - i] - average) / sigma;
                fprintf(fp, "%5Lf,%Lf, %Lf\n", fr, SN, (max * sigma) + average);
//                printf("%5Lf,%Lf\n", fr, SN);
                }
                g[j] = 1;
            }
            
        }
        }
        
       
    }
    
    
    

//
//    for(i = max; i >= min; i--)
//    {
//        for(j = 0; j <= 8192; j++)
//        {
//            if(d[j][i] != 0)
//            {
//                fprintf(fp, "%f %f %d\n", freq[d[j][i]], data[d[j][i]], i);
//            }
//        }
//    }
    
    
    free(f);
    fclose(fp);
    return 0;
}
