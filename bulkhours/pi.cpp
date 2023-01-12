// source: http://cacs.usc.edu/education/cs596/src/cuda/pi.cu

// Using CUDA device to calculate pi

////How to run?
//===========
//
//Single precision :
//
//nvcc -O3 pi-mystery.cu ; ./a.out
//
//Double precision
//
//nvcc -O3 -D DP pi-mystery.cu ; ./a.out

#include <stdio.h>
#include <cuda.h>


#define TRIALS_PER_THREAD 4096
#define NUM_BLOCK  256  // Number of thread blocks
#define NUM_THREAD  256  // Number of threads per block
// #define NBIN TRIALS_PER_THREAD*NUM_THREAD*NUM_BLOCK  // Number of bins 4096*256*256
// 
// // 2^28
#define NBIN 268435456  // Number of bins 4096*256*256

// // 2^26
// #define NBIN 67108864  // Number of bins 1024*256*256

// 2^24
// #define NBIN 16777216  // Number of bins 256*256*256

//Help code for switching between Single Precision and Double Precision
#ifdef DP
typedef double Real;
#define PI  3.14159265358979323846  // known value of pi
#else
typedef float Real;
#define PI 3.1415926535  // known value of pi
#endif

int tid;
Real pi = 0;

// Kernel that executes on the CUDA device
__global__ void cal_pi(Real *sum, int nbin, Real step, int nthreads, int nblocks) {
	int i;
	Real x;
	int idx = blockIdx.x*blockDim.x+threadIdx.x;  // Sequential thread index across the blocks
	for (i=idx; i< nbin; i+=nthreads*nblocks) {
		x = (i+0.5)*step;
		sum[idx] += 4.0/(1.0+x*x);
	}
}

// Main routine that executes on the host
int main(void) {

	clock_t start,end;

	dim3 dimGrid(NUM_BLOCK,1,1);  // Grid dimensions
	dim3 dimBlock(NUM_THREAD,1,1);  // Block dimensions
	Real *sumHost, *sumDev;  // Pointer to host & device arrays

	printf("# of trials per thread = %d, # of blocks = %d, # of threads/block = %d\n",TRIALS_PER_THREAD,NUM_BLOCK,NUM_THREAD);

	Real step = 1.0/NBIN;  // Step size
	size_t size = NUM_BLOCK*NUM_THREAD*sizeof(Real);  //Array memory size
	sumHost = (Real *)malloc(size);  //  Allocate array on host

	start=clock();

	cudaMalloc((void **) &sumDev, size);  // Allocate array on device
	// Initialize array in device to 0
	cudaMemset(sumDev, 0, size);
	// Do calculation on device
	cal_pi <<<dimGrid, dimBlock>>> (sumDev, NBIN, step, NUM_THREAD, NUM_BLOCK); // call CUDA kernel
	// Retrieve result from device and store it in host array
	cudaMemcpy(sumHost, sumDev, size, cudaMemcpyDeviceToHost);
	for(tid=0; tid<NUM_THREAD*NUM_BLOCK; tid++)
		pi += sumHost[tid];
	pi *= step;

	end=clock();
	// Print results

	printf("GPU PI calculated in : %f s.\n",(end-start)/(float)CLOCKS_PER_SEC);

	#ifdef DP
	printf("GPU estimated PI = %20.18f [error of %20.18f]\n",pi,pi-PI);
	#else
	printf("GPU estimated PI = %f [error of %f]\n",pi,pi-PI);
	#endif

	// Cleanup
	free(sumHost); 
	cudaFree(sumDev);

	return 0;
}
