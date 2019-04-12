//
//  gnuplot.c
//  ASAS
//
//  Created by 濱江勇希 on 2017/11/07.
//  Copyright © 2017年 濱江勇希. All rights reserved.
//

#include "gnuplot.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <math.h>
#include "data_processing.h"
long double plot(long double *x, long double *y, char *infilename, char * object, char *file, char *write)
{
    int freq[8192] = {0};
    long double snr = 0;
    long double f = 0;
    int i = 0;
    int j = 0;
    char outfilename[512];
    char buf[512];
    long double range = 0;
    long double max = 0;
    long double  mfreq[8192] = {0};

    FILE *fp1;
    FILE *fp2;


    strcpy(outfilename, "result.gp");

    fp1 = fopen(infilename, "r");
    
    fgets(buf, 512, fp1);
    
    while(fscanf(fp1, "%Lf, %Lf, %Lf", &f, &snr, &max) != EOF)
    {
        freq[i] = f;
        mfreq[i] = max;
        i++;
    }
   
    fclose(fp1);

    sprintf(buf, "%s-source.txt", file);

    fp2 = fopen(outfilename, "a");
    range = freq[0];
    fprintf(fp2, "set terminal postscript eps enhanced color\n");

    
    for(j = 0; j <= i; j++)
    {
        
        if(freq[j] - 5 >= range)
        {
            fprintf(fp2, "set autoscale y\n");
            fprintf(fp2, "set autoscale yfixmax\n");
            fprintf(fp2, "set autoscale yfixmin\n");
            fprintf(fp2, "set xrange[%d:%d]\n", freq[j] - 3, freq[j] + 3);
            fprintf(fp2, "set xlabel 'frequency[MHz]'\n");
            fprintf(fp2, "lp title '%s %.0d-%.0d'\n", object, freq[j] - 3, freq[j] + 3);
            fprintf(fp2, "plot '%s' with lines\n", buf);
            fprintf(fp2, "set output 'result/%d-%d_%s.eps'\n", freq[j] - 3, freq[j] + 3, object);
            fprintf(fp2, "replot\n");
            range = freq[j];
        }
        
        
    }
    fclose(fp2);
    
    return 0;
}
