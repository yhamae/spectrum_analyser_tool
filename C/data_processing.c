//
//  data_processing.c
//  課題1 インクの拡散(シミュレーション物理学)
//
//  Created by 濱江勇希 on 2018/04/13.
//  Copyright © 2018年 濱江勇希. All rights reserved.
//

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <malloc/malloc.h>
#include <math.h>
#include <time.h>
#include "data_processing.h"


#define MAXLINE 8192;

#define CHECK 1


/*------------------------------
 Averageを求める
------------------------------*/
long double ave(long double *data, int start, int end)
{
	int i;
	long double sum = 0;
    int N = end - start +1;

    for(i = start; i <= end; i++)
	{
		sum += data[i];
	}
    sum /= N;
	if(isnan(sum) != 0)
	{
        return 0;
	}
   
	return sum;
}


/*------------------------------
 SDを求める
 ------------------------------*/
long double sd(long double *data, int start, int end)
{
    int i, j, k, n;
    i = 0;
    j = 0;
    k = 0;
    n = end - start +1;
    long double sigma;
    long double average;
    
    average = ave(data, start, end);
    
    
    long double sum = 0;

    
    for(i = start; i <= end; i++)
    {
        sum += data[i] * data[i];
    }
    sum /= n;
    sigma = sqrt(sum - (average * average));
    
    return sigma;
}

/*------------------------------
 Medianを求める
 ------------------------------*/
long double med(long double *data, int start, int end, int IF)
{
	int i, j, n;
    long double tmp= {0};
    long double y[9000] = {0};
    long double median = 0;
//    y = (long double*)malloc(sizeof(long double ) * (end - start + 1));
	n = end - start + 1;
    
    for(i = start; i <= end + 1; i++)
    {
        y[i - start] = data[i];
    }


    for(i = start; i < end - 1; i++)
    {
    	for(j = i + 1; j < end; j++)
   		{
    		if(y[i] > y[j])
     	   	{
     	   		tmp =  y[i];
    	        y[i] = y[j];
    	        y[j] = tmp;
			}
		}
	}

	if(n % 2 == 1)  // データ数が奇数個の場合
    {
          median = y[(end - start) / 2];
    }
    else  // データ数が偶数の場合
    {
        median = (y[(n / 2) - 1] + y[start + (n / 2)]) / 2.0;
    }
//    free(y);
    return median;
	
}


/*------------------------------
 MADFMを求める
 ------------------------------*/
long double MADFM(long double *data, int start, int end, int IF)
{
	long double median_a;
    long double *median;
    median = (long double*)malloc(sizeof(long double ) * (end - start + 1));
	
	median_a = med(data, start, end, IF);

    int i;
    for(i = 0; i <=end - start; i++)
        {
            median[i] = sqrt(pow(data[i + start] - median_a, 2.0));
        }
    
    
    
//    int j;
//    long double tmp;
//
//        for(i = 1; i < 8179; i++)
//        {
//            for(j = 0; j < 8179 - i; j++)
//            {
//                if(median[j] > median[j+1])
//                {
//                    tmp =  median[j];
//                    median[j] = median[j+1];
//                    median[j+1] = tmp;
//                }
//
//            }
//        }
    median_a = med(median, 0, end - start, IF);
    free(median);
    return fabsl(median_a) ;

}

/*------------------------------
 2次近似曲線
 ------------------------------*/
long double sai_2(long double *x, long double *y, int start, int end, long double snr, long double a, long double b, int mode)
{
    
        int i = 0;
        int n = 0;
        long double madfm = 0;
        long double average = 0;
        long double sum_x = 0;
        long double sum_y = 0;
        long double sum_x2 = 0;
        long double sum_xy = 0;
    
        if(mode == 0 || mode == 1)
        {
            madfm = 0.6744888 * MADFM(y, start, end, 0);
        }
        else{
    madfm = sd(y, start, end);
        }
        average = ave(y, start, end);
    
        for (i = start; i <= end; i++)
        {
            if(y[i] <= average + (snr * madfm) || average - (snr * madfm) <= y[i])
            {
                
                sum_xy += x[i] * y[i];
                sum_x += x[i];
                sum_y += y[i];
                sum_x2 += x[i] * x[i];
                n++;
            }
        }
        
        a = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - pow(sum_x, 2));
        b = (sum_x2 * sum_y - sum_xy * sum_x) / (n * sum_x2 - pow(sum_x, 2));
    if(mode == 0)
    {
            for(i = start; i <= end; i++)
            {
                y[i] -= a * x[i] + b;
            }
    }
    
    return 0;
}


/*------------------------------
n次近似曲線
------------------------------*/
void sai(long double *x,long double *y, int N, int start, int end, long double *d, int mode, long double snr)
{
    int i = 0;
    int j = 0;
    int k = 0;
    int n = N;
    int S = end - start ;
    int l = 0;
    int pivot = 0;
    long double madfm = 0;
    long double median = 0;
    long double p = 0;
    long double q = 0;
    long double m = 0;
    
     long double dy[S+1];
     long double f[S+1];
     long double g[S+1];
     long double c[N];
     long double A[N][N+1];
     long double xx[N];
     long double b[N];
//   long double *dy;
//   long double *f;
//   long double *g;
//   long double *c;
//   long double **A;
//   long double *xx;
//   long double *b;
//
//
//   A = (long double**)malloc(sizeof(long double *) * N);
//   b = (long double*)malloc(sizeof(long double ) * N);
//   xx = (long double*)malloc(sizeof(long double) * N);
//   dy = (long double*)malloc(sizeof(long double ) * S + 1);
//   f = (long double*)malloc(sizeof(long double ) * S + 1);
//   g = (long double*)malloc(sizeof(long double ) * S + 1);
//   c = (long double*)malloc(sizeof(long double) * N);
//
//   for(i = 0; i <= N; i++)
//   {
//       A[i] = (long double*)malloc(sizeof(long double) * (N + 1));
//   }
//
    
    //
    for(i=0;i<=n;i++)
    {
        for(j=0;j<=n+1;j++)
        {
            A[i][j]=0.0;
            
        }
    }

    for(i = 0; i <= N; i++)
    {
        xx[i] = 0;
        c[i] = 0;
    }

    for(i = 0; i <= S + 1; i++)
    {
        dy[i] = 0;
        f[i] = 0;
        g[i] = 0;
    }
    for(i=0;i<N;i++)
    {
        for(j=0;j<N+1;j++)
        {
            b[j]=0.0;
            c[i] = 0.0;
            
        }
    }

    
    if(mode != 2)
    {
        
        madfm = 0.6744888 * MADFM(y, start, end, 0);
        median = ave(y, start, end);
        
        for(i = start; i <= end; i++)
        {
            if(y[i] <= median + snr * madfm && median - snr * madfm <= y[i])
            {
                f[l] = x[i];
                if(f[l] == 0)
                {
//                    printf("f = 0, %d\n", l);
                }
                if(isnan(f[l]) != 0)
                {
//                    printf("f = nan, %d\n", i);
                }
                g[l] = y[i];
                if(isnan(g[l]) != 0)
                {
//                    printf("g = nan, %d\n", i);
                }
                l++;
            }
        }
        S = l - 1;

//        for(i = start; i <= end - 1; i++)
//        {
//            dy[i - start] = (y[i + 1] - y[i]) / 2;
//
//        }
//
//        madfm = MADFM(dy, 0, end - start - 1, 0);
//        median = med(dy, 0, end - start - 1, 0);
//
//        for(i = start; i <= end - 1; i++)
//        {
//            if(dy[i - start] <= median + snr * madfm || median - snr * madfm >= dy[i - start])
//            {
//                f[l] = x[i + 1];
//                if(f[l] == 0)
//                {
//                    printf("f = 0, %d\n", l);
//                }
//                if(isnan(f[l]) != 0)
//                {
//                    printf("f = nan, %d\n", i);
//                }
//                g[l] = y[i +1];
//                if(isnan(g[l]) != 0)
//                {
//                    printf("g = nan, %d\n", i);
//                }
//                l++;
//            }
//        }
//        S = l - 1;
    }

    else
    {
        for(i = start;i <= end; i++ )
        {
            f[i - start] = x[i];
            g[i - start] = y[i];
        }
    
    }
    



  
    median = med(g, 0, end - start, 0);
    madfm = MADFM(g, 0, end - start, 0);

    /*初期化*/


/*ガウスの消去法で解く行列の作成*/
    for(i=0;i<n;i++)
    {
        for(j=0;j<n;j++)
        {
            for(k=0;k<=S;k++)
            {
                A[i][j]+=pow(f[k],i+j);
                if(A[i][j] == 0)
                {
//                    printf("1\n");
                }
                
            }
        }
        for(k=0;k<=S;k++)
        {
            A[i][n]+=pow(f[k],i)*g[k];
            if(A[i][n] == 0)
            {
//                                    printf("2\n");
            }
            
        }
    }
    
//    for( i=0 ; i < N; i++ )  /* 列 */
//    {
//        for( j=0 ; j < N + 1 ; j++ )  /* 行 */
//        {
//            printf( "%3.5Lf ", A[i][j] );
//        }
//        printf( "\n" );
//    }
        /*ガウスの消去法の実行（配列xxは解、すなわち多項式の係数を入れるためのもの）*/

    
    

    for(i=0;i<N;i++)
    {
        m=0;
        pivot=i;
        
        for(l=i;l<N;l++)
        {
            if(fabsl(A[l][i])>m)
            {   //i列の中で一番値が大きい行を選ぶ
                m=fabsl(A[l][i]);
                pivot=l;
            }
        }
        
        
        if(pivot!=i)
        {                          //pivotがiと違えば、行の入れ替え
            for(j=0;j<N+1;j++)
            {
                b[j]=A[i][j];
                A[i][j]=A[pivot][j];
                A[pivot][j]=b[j];
            }
        }
    }
    
    for(k=0;k<N;k++)
    {
        p=A[k][k];              //対角要素を保存
        A[k][k]=1;              //対角要素は１になることがわかっているから
        
        for(j=k+1;j<N+1;j++)
        {  //行列見る
            A[k][j]/=p;
            if(p == 0)
            {
               // printf("3\n");
               for(i=0;i<N;i++)
               {
                   for(j=0;j<N+1;j++)
                   {
                       printf("%5.3Lf",A[i][j]);
                   }
                   printf("\n");

               }
            }
        }
        
        for(i=k+1;i<N;i++)
        {
            q=A[i][k];
            
            for(j=k+1;j<N+1;j++)
            {
                A[i][j]-=q*A[k][j];
            }
            A[i][k]=0;              //０となることがわかっているところ
        }
    }
    
    //解の計算
    for(i=N-1;i>=0;i--)
    {
        c[i]=A[i][N];
        for(j=N-1;j>i;j--)
        {
            c[i]-=A[i][j]*c[j];
//             if(isnan(c[i]) != 0)
//             {
// //                printf("c ^ %d is nan\n",i);
//                 c[i] = 0;
//             }
        }
    }
//    FILE* fp3;
//    fp3 = fopen("test-3.txt", "a");
    


//    if(mode == 0 || mode == 2)
//    {
//        for(j=0;j<= end - start;j++)
//        {
//            fprintf(fp3, "%Lf   %Lf, %Lf, %Lf, %Lf, %Lf\n",x[j+start], y[j+start], c[0], c[1], c[2], c[3]);
//            for(i=0;i<N;i++) {
//                y[start + j]-=c[i]*pow(x[j + start],i);
////                printf("c^%d=%Lf ",i,c[i]);
////                if(isnan(y[start + j]) != 0)
////                {
////                    printf("%d ch is nan\n",start + j);
////                }
//            }
////            printf("\n");
//        }
//    }
//    fprintf(fp3, "------------------------\n");
//    fclose(fp3);
//    FILE *fp2;
//    long double XXX = 0;
//    fp2=fopen("test-2.txt", "a");
//    for(j = 0; j <= end - start; j++)
//    {
//        for(i=0;i<N;i++) {
//            XXX+=c[i]*pow(x[j + start],i);
//        }
//        fprintf(fp2, "%Lf   %Lf\n",x[j+start], XXX);
//        XXX = 0;
//    }
//    fclose(fp2);
    if(mode == 1)
    {
        for(j=0;j<= end - start;j++)
        {
            for(i=0;i<N;i++)
            {
                d[i] =c[i];
            }
        }
    }

//再初期化
 for(i=0;i<=n;i++)
    {
        for(j=0;j<=n+1;j++)
        {
            A[i][j]=0.0;
            
        }
    }

    for(i = 0; i <= N; i++)
    {
        xx[i] = 0;
        c[i] = 0;
    }

    for(i = 0; i <= S + 1; i++)
    {
        dy[i] = 0;
        f[i] = 0;
        g[i] = 0;
    }
    for(i=0;i<N;i++)
    {
        for(j=0;j<N+1;j++)
        {
            b[j]=0.0;
            c[i] = 0.0;
            
        }
    }

//   for(i = 0; i <n; i++)
//   {
//       free(A[i]);
//   }

//
//   free(A);
//   free(b);
//   free(xx);
//   free(dy);
//   free(f);
//   free(c);
//   free(g);
}


/*------------------------------
//Runge Kutta Quadratic
------------------------------*/
long double runge_kutta_quadratic(long double C1, long double C0, long double *x, long double *f, long double initial_value_1, long double initial_value_2, long double dx, int start, int end)
{
    //Define variable
    int i = 0;
    long double g[3] = {0};
    long double k[5] = {0};
    long double h[5] = {0};
    
    //Initialization
    f[0] = initial_value_1;
    g[1] = initial_value_2;
    
    for (i = 0; i <= end - start; i ++)
    {
        x[i] = start + i * dx;
        
        k[1] = dx * g[1];
        h[1] = -dx * (C1 * g[1] + C0 * f[i]);
        
        k[2] = dx * (g[1] + h[1] / 2);
        h[2] = -dx * (C1 * (g[1] + h[1] / 2) + C0 * (f[i] + k[1] / 2) );
        
        k[3] = dx * (g[1] + h[2] / 2);
        h[3] = -dx * (C1 * (g[1] + h[2] / 2) + C0 * (f[i] + k[2] / 2) );
        
        k[4] = dx * (g[1] + h[3]);
        h[4] = -dx * (C1 * (g[1] + h[3]) + C0 * (f[i] + k[3]) );
        
        k[0] = (k[1] + 2 * k[2] + 2 * k[3] + k[4]) / 6;
        f[i + 1] = f[i] + k[0];
        
        h[0] = (h[1] + 2*h[2] + 2*h[3] + h[4]) / 6;
        g[2] = g[1] + h[0];
        
        g[1] = g[2];
    }

    return 0;
}


/*------------------------------
乱数生成
------------------------------*/
long double GetRandom(int x)
{
    int a = 0;
    long double r = 0;

    a = pow(10, x) + 1;
    srand((unsigned int) time(NULL)); //現在時刻を元に種を生成
    r = rand() % a;
    
    return r / a;
}
