%%ipsa_nvcudac_and_exec
#include <stdlib.h>
#include <stdio.h>
#include <cuda.h>
#include <math.h>
#include <time.h>
#include <iostream>

using namespace std;


__global__ void kernel_func(int *a) {
    unsigned int thread_idx = threadIdx.x + blockDim.x * blockIdx.x;
    ...
}

int main (int argc, char *argv[]) {

  // Do sequential stuff
  malloc(...);
  ...  

  // Allocate object on the Device
  cudaMalloc(...);

  // Copy memory from Host to Device
  cudaMemcpy(..., cudaMemcpyHostToDevice);

  // Launch Kernel function
  kernel_func<<<grid_size, block_size>>>(...);

  // Copy memory from Device to Host
  cudaMemcpy(..., cudaMemcpyDeviceToHost);

  // Deallocate object on the Device
  cudaFree(...);

  // Do other sequential stuff
  ...  
  free(...);
}