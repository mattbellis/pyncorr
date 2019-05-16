#include<stdio.h>
#include<stdlib.h>

#define imax 256

int main(int argc, char *argv[]) {

    unsigned long nvals = atoll(argv[1]);

    printf("nvals: %lu\n",nvals);

    //long long *hist = long long *(malloc(r * c * sizeof(int));

    int i, j, k = 0; 
    
    // Issues sometimes with large arrays because of the stack?
    // https://stackoverflow.com/questions/7902228/segmentation-fault-large-arrays
    static unsigned long hist[imax][imax][imax];



    //int imax = 128;
    int jmax = imax;
    int kmax = imax;

    /*
    unsigned long ***hist = (unsigned long***)malloc(imax * sizeof(unsigned long**));
    for (i = 0; i <  imax; i++)  {
        hist[i] = (unsigned long**)malloc(jmax * sizeof(unsigned long*));
        for (j = 0; j < jmax; j++) {
            hist[i][j] = (unsigned long*)malloc(kmax * sizeof(unsigned long)); 
        }
    }
    */

    printf("Allocated the memory.\n");

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
    printf("Filling the memory with %lu entries .\n",nvals);

    printf("RAND_MAX: %d\n",RAND_MAX);
    int slice = (int)(RAND_MAX/imax);

    for(unsigned long count=0;count<nvals;count++)
    {
        if (count%1000000==0){
            printf("count: %d\n",count);
        }
        /*
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
        }
        */

        i = (int)rand()/slice;
        j = (int)rand()/slice;
        k = (int)rand()/slice;
        //printf("%d %d %d\n",i,j,j);
        if(i<imax && j<imax && k<imax)
            hist[i][j][k]++;
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
