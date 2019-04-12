//
//  main.c
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
#include <time.h>
#include "find.h"
#include "data_processing.h"
#include "export.h"
#include "flagging.h"
#include "integrate.h"
#include "gnuplot.h"

#define MAX_LINE 512


int main()
{

    
    
    /*------------------------------
	Define variable
	------------------------------*/

    int i = 0;
    int j = 0;
    int k = 0;
    int range = 0;
    int repeat = 0;
    int spectpoint = 0;
    int IF = 0;
    int fla = 0;
    int hed;
    int mood_a;
    int mood_b;
    int d = 0;
    long time = 0;
    long double sigma_a = 0.0;
    long double sigma_b;
    long double data[8193];
    long double data_fla[8193];
    long double freq[8193];
    char astro[256];
    char write[64];
    char buf[MAX_LINE];
    char task[MAX_LINE];
    char parameter[MAX_LINE];
    char inf[MAX_LINE];
    char exf[MAX_LINE];
    char ifreq[MAX_LINE];
    char fname[MAX_LINE];
    
    FILE *command = NULL;
    FILE *gnu;

    gnu = fopen("result.gp", "w");
    fclose(gnu);
    
    
	/*------------------------------
	Parameter setting
	------------------------------*/
    strcpy(buf, "default");

	while(strcmp(buf, "exit") != 0)
	{
    	while(strcmp(buf, "go") != 0 || strcmp(buf, "exit") == 0)
    	{
            i = 0;
            if(strcmp(buf, "default\n") == 0)
            {
                /*------------------------------
                 Initialization for parameter
                 ------------------------------*/
                i = 0;
                j = 0;
                k = 0;
                spectpoint = 8192;  //分光点の数
                IF = 1;             //IF(Intermediate_Frequency)の数
                hed = 13;           //Header informationの行数
                fla = 0;            //フラギングをする(0) or しない(1)
                mood_a = 0;         //off pointをならすときMedianフィルタ(1) or 移動平均(0)
                mood_b = 1;         //輝線判定をする(0) or しない(1)
                sigma_a = 1;        //flagging時のσ
                sigma_b = 2;        //輝線判定時のσ
                d = 10;
                range = 1000;
                i++;
            }
            //コマンドラインから取得
            printf("ASAS>");
            fgets(buf, 1024, stdin);
            sscanf(buf, "%s %s\n", task, parameter);
            
            if(strcmp(task, "inp") == 0)
            {
                repeat = 1;
                
                i++;
                
                if((command = fopen(parameter, "r")) != NULL)
                {
                break;
                }
                else
                {
                    printf("%s: No such file or directory\n", parameter);
                }
                
                repeat = -1;
            }

    		if(strcmp(buf, "parameter\n") == 0)
    		{
				printf("Input filename		%s\n", inf);
				printf("Export filename		%s\n", exf);
				printf("Spectrum point		%d\n", spectpoint);
				printf("IF					%d\n", IF);
				printf("Flagging's sigma	%Lf\n", sigma_a);
                i++;
    		}

            if(strcmp(task, "infile") == 0)
            {
                strcpy(inf, parameter);
                i++;
            }

            if(strcmp(task, "exfile") == 0)
            {
                strcpy(exf, parameter);
                i++;
            }

            if(strcmp(task, "object") == 0)
            {
                strcpy(astro, parameter);
                i++;
            }
            
            if(strcmp(task, "IF") == 0)
            {
                strcpy(ifreq, parameter);
                IF = atoi(ifreq);
                i++;
            }
        
            if(i == 0)
            {
                printf("%s: command not found\n", buf);
            }
            
            i = 0;
            
        }
        
        
        if(strcmp(buf, "exit") == 0)
        {
            break;
        }
 

        while(repeat != 0)
        {
            
            if(repeat >= 1)
            {
                if(fscanf(command,"%s %s %s %d %s", inf, exf, astro, &IF, fname) == EOF)
                {
                    break;
                }
                printf("Read: %s %s %s %d %s\n", inf, exf, astro, IF, fname);
            }
            
        time = clock();

        printf("Input filename        %s\n", inf);
        printf("IF                    %d\n", IF);
        printf("Object                %s\n", astro);

        /*------------------------------
        Reading and Integrate
        ------------------------------*/
        char on[512], off[512];
            long double stpoint = 0.0, point =0;;
        point = integrate(inf, astro, data, freq, IF, 8192, 7, on, off, stpoint);
        sprintf(buf, "%s-source.txt", exf);
            
        export(buf, astro, freq, data, IF, stpoint);

        /*------------------------------
        Flagging
        ------------------------------*/
        

        flagging(data, sigma_a, data_fla, freq, 1, 8192,d/*コブの範囲*/, IF, 8, 8192 - 7, 1000);


        /*------------------------------
        Export
        ------------------------------*/
        export(exf, astro, freq, data, IF, point);

//        find(data, freq, fname, 4  , 8, 20);
            strcpy(write, "a");
//            plot(freq, data, fname, astro, exf, write);
            printf("Time = %lu\n", clock() - time);
            printf("--------------------------------------------\n");

            repeat ++;
        }
        if(strcmp(buf, "exit") == 0)
        {
            break;
        }
//        strcpy(buf, NULL);
        
    }
    return 0;
}
