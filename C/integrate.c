//
//  integrate.c
//  ASAS
//
//  Created by 濱江勇希 on 2017/04/30.
//  Copyright © 2017年 濱江勇希. All rights reserved.
//

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "data_processing.h"
#include "integrate.h"


long double integrate(char *inf, char *object, long double *data, long double *freq, int ifreq, int maxcha, int ave_range, char *on, char *off, long double start_point)
{

	/*------------------------------
	Define variable
	------------------------------*/
	FILE *fp;
	fp = fopen(inf, "r");
    
    int i = 0;
    int IF = 0;
    int channel = 0;
    int j = 0;
    int a = 0;
    int k = 0;
    long double frequency = 0.0;
   	long double velocity;
   	long double real;
   	long double imag;
   	long double onpoint[8193];
   	long double offpoint[8193];
    char polar;
    char buf[256];
		
    
	/*------------------------------
	Read and Integrate
	------------------------------*/
    rewind(fp);
 	while(fscanf(fp, "%s", buf) != EOF)
 	{
 		if(strcmp(buf, object) == 0)
 		{
//            printf("%s\n", buf);
 			//on point
 			for(int e = 0; e <= 840; e += 70)  //Header information
            {
                fgets(on,256,fp);
//                printf("%s", on);
            }

			while(fscanf(fp,"%d %d %s %Lf %Lf %Lf %Lf",&channel, &IF, &polar, &frequency, &velocity, &real, &imag) != EOF)  //Data
            {
 				if(IF == ifreq)
                {
                    onpoint[channel] += real;
                    freq[channel] = frequency/10000;
//                    if(k == 0)
//                    {
//                        start_point = frequency;
//                        k++;
//                    }
                    
            //                    printf("  %4d %d %f %f\n",channel, IF, frequency, real );
							i++;
                    
            
                }

                if(channel == maxcha && IF == atoi("4"))
                {
	                break;
                }
			}

			//off point
			for(int e = 0; e <= 910; e += 70)  //Header information
            {
                fgets(&on[e],256,fp);
//                printf("%c", on[e]);
            }

			while(fscanf(fp,"%d %d %s %Lf %Lf %Lf %Lf",&channel, &IF, &polar, &frequency, &velocity, &real, &imag) != EOF)  //Data
            {
                if(IF == ifreq)
                {
                    offpoint[channel] += real;
                   
//                    printf("  %4d %d %f %f\n",channel, IF, frequency, real );
                }
 				

 				if(channel == maxcha && IF == atoi("4"))
                {
	                break;
                }
			}

			a++;
 		}
 	}

 	fclose(fp);
    k = 0;
	//積分が失敗したとき
	if(a ==0)
	{
		printf("Faild\n");
		return 1;
	}


	/*------------------------------
	off point をならす
	------------------------------*/
	long double off_ave[8193];
	
    for(int j = 8; j < 8192 - 7; j++)
    {
        off_ave[j] = ave(offpoint, j - 7, j + 7);
//        printf("%f\n", off_ave[j]);
    }
	


	/*------------------------------
	on point - off point
	------------------------------*/
	
    for(j = 8; j <= maxcha-7; j++)
    {
        data[j] = 1000* (onpoint[j] - off_ave[j])  / i;
//        freq[j] = (freq[j] - start_point)/10;
//        printf("%f\n",data[j]);
    }
//    for(j = 8; j <= maxcha-7; j++)
//    {
//        modfl( onpoint[j] - off_ave[j], &data[j]);
//        //        printf("%f\n",data[j]);
//    }
	


//    printf("Finish calculation\n");


	return start_point;
}
