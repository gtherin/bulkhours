This package is a support library for different courses. 


## 1. [Data information](data/README.md)
## 2. [Plan of High Performance Programming on GPU course](bulkhours/hpc/README.md)
## 3. [Plan of High Performance Programming on GPU course](bulkhours/ecox/README.md)
## 4. [Course methods](#methods)
## 5. [Other stuffs](#stuffs)


## Methods <a name="methods"></a>

##### evaluation methods

You need to login to be properly be evaluated:
```python:
bulkhours.init_env(login="john.doe@bulkhours")
```

##### Cuda methods

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

You can load the magic methods with (in case you don't need to login):
```python:
bulkhours.load_extra_magics()
```


