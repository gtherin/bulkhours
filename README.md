This package is a support library for different courses. 


1. [Data information page](data/README.md)
2. [Plan of High Performance Programming on GPU course](bulkhours/hpc/README.md)
3. [Plan of the econometrics course](bulkhours/ecox/README.md)
4. [Magic methods](#methods)


## Methods <a name="methods"></a>

##### evaluation methods

You need to login to be properly be evaluated:
```python:
bulkhours.init_env(login="john.doe@bulkhours")
```

##### Cuda/C++ methods

Cuda basic extension compiles C/C++/CUDA code and exec it
```c:
%%evaluation_cell_id -i demo_cuda
%%compile_and_exec -c nvcc
#include <iostream>
int main() {
    for (int i = 0; i <= 10; ++i) {
        std::cout << i << std::endl;
    }
}
```


