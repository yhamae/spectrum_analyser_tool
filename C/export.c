//
//  export.c
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
#include "export.h"

long double export(char exp_filename[256], char astro[256], long double *freq_1, long double *data_1, int IF, long double start_point)
{

    FILE *fp;
    int i;
    
    fp = fopen(exp_filename,"w");   //ファイル作成
    
    for(i = 8; i <= 8178 - 7 ; i++)  //IF = 1
    {
//        if(data_1[i] <=0.005 &&data_1[i]>= -0.005)
//        {
//        fprintf(fp, "%Lf   %Lf\n",(freq_1[i]+start_point)*100
//, data_1[i]);
//        if(data_1[i] <= 1 && data_1[i] >= -1)
//        {
        fprintf(fp, "%Lf   %Lf\n",freq_1[i]*10000, data_1[i]);
//        }
    }
//    }
    fclose(fp);

    
    return 0;
}
