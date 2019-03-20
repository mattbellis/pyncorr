#include<stdio.h>
#include<stdlib.h>

#define imax 256

int main(int argc, char *argv[]) {

    int nvals = atoi(argv[1]);

    printf("nvals: %d\n",nvals);

    int i, j, k = 0; 
    
    static unsigned long hist[imax][imax][imax];

    //int imax = 128;
    int jmax = imax;
    int kmax = imax;

    printf("Allocated the memory.\n");

    // Zero out the entries
    for (i = 0; i <  imax; i++)  {
        //printf("%d\n",i);
        for (j = 0; j < jmax; j++) {
            //printf("\t%d ",j);
              for (k = 0; k < kmax; k++) {
                  hist[i][j][k] = 0;
              }
        }
    }

    printf("Zeroed the memory.\n");
    printf("Filling the memory with %d entries .\n",nvals);

    printf("RAND_MAX: %d\n",RAND_MAX);
    int slice = (int)(RAND_MAX/imax);

    for(int count=0;count<nvals;count++)
    {
        if (count%100000==0){
            printf("count: %d\n",count);
        }

        i = (int)rand()/slice;
        j = (int)rand()/slice;
        k = (int)rand()/slice;
        //printf("%d %d %d\n",i,j,j);
        
        if(i<imax && j<imax && k<imax)
            hist[i][j][k]++;
    }
                      
    return 0;
}
