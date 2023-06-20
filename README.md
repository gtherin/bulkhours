This package is a support library for different courses. 

1. [Plan of econometrics course](#planeco)
2. [Plan of High Performance Programming on GPU course](#planhpc)
3. [Course methods](#methods)
4. [Data information](#data)
5. [Other stuffs](#stuffs)


## Plan of econometrics course <a name="planeco"></a>
[Plan of High Performance Programming on GPU course](bulkhours/ecox/README.md)

## Plan of High Performance Programming on GPU course <a name="planhpc"></a>

[Plan of High Performance Programming on GPU course](bulkhours/hpc/README.md)


## Data information<a name="data"></a>
[Data information](data/README.md)

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


