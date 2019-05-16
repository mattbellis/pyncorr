#include<stdio.h>
#include<stdlib.h>

#define imax 256
#define imax2 imax*imax
#define imax3 imax*imax*imax

int main(int argc, char *argv[]) {

    unsigned long nvals = atoll(argv[1]);

    printf("nvals: %lu\n",nvals);

    int i, j, k = 0; 
    
    static unsigned long hist[imax][imax][imax];
    //static unsigned long hist[imax3];

    //int imax = 128;
    int jmax = imax;
    int kmax = imax;

    int idx = 0;

    printf("Allocated the memory.\n");

    // Zero out the entries
    for (i = 0; i <  imax; i++)  {
        for (j = 0; j < jmax; j++) {
              for (k = 0; k < kmax; k++) {
                  hist[i][j][k] = 0;
              }
        }
    }

    printf("Zeroed the memory.\n");
    printf("Filling the memory with %lu entries .\n",nvals);

    printf("RAND_MAX: %d\n",RAND_MAX);
    int slice = (int)(RAND_MAX/imax);

    for(unsigned long count=0;count<nvals;count++)
    {
        if (count%1000000==0){
            printf("count: %d\n",count);
        }

        i = (int)rand()/slice;
        j = (int)rand()/slice;
        k = (int)rand()/slice;
        //printf("%d %d %d\n",i,j,j);
        
        if(i<imax && j<imax && k<imax)
            hist[i][j][k]++;

        /*
        idx = i*imax2 + j*imax + k;
        if (idx<imax3)
            hist[idx]++;
        */
    }
                      
        for (i = 0; i <  imax; i++)  {
          printf("%d\n",i);
            for (j = 0; j < jmax; j++) {
                  for (k = 0; k < kmax; k++) {
                      printf("%d ",hist[i][j][k]);
                  }
                  printf("\n");
            }
          printf("\n");
        }
    

    /*
    for (i = 0; i <  imax; i++) 
          for (j = 0; j < jmax; j++) 
              for (k = 0; k < kmax; k++) 
                   *(arr + i*c + j) = ++count; 
 
   for (i = 0; i <  r; i++) 
         for (j = 0; j < c; j++) 
                  printf("%d ", *(arr + i*c + j)); 
      */
                                                                

    return 0;
}
