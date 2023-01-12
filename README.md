This package is a support library for different courses

# Table of Contents
1. [Plan of econometry course](#planeco)
2. [Plan of High Performance Programming on GPU course](#planhpc)
3. [Generic methods](#methods)
4. [Data](#data)


## Plan of econometry course <a name="planeco"></a>

```
# 1/4 (4h): Feb-09/08:30
01 Probability and statistics
- Grandeurs caracteristiques (moyenne, mediane, vol, skew, kurtosis)
- Gaussienne
- Mouvement brownien
- Lemme d'Ito

# 2/4 (4h): Feb-10/08:30
03 Time Series statistics
- Distribution des returns
- Autocorrelations
- Les queues de distribution

# 3/4 (4h): Feb-17/08:30
12 Filter time series

# 4/4 (4h): Feb-01/08:30
08 Predict time series

Might be added one day
    02 Financial products
    04 Correlations
    05 Risk estimations
    05 Price anomalies
    05 Macroeconomic quantities

    08 Optimal portfolio construction
    09 Historic of financial crises
    10 Systematic trading
    11 Yield curve
    11 Cryptocurrencies

```


## Plan of High Performance Programming on GPU course <a name="planhpc"></a>

```
# 1/5 (2h): Nov-09/13:30
01 General introduction (slides)
02 Notebooks' environment (notebook)
03 Computing Metrics (notebook)

# 2/5 (4h): Nov-10/08:30
03 Computing Metrics (notebook)
04 Hardware architecture (slides)
05 Introduction to C/C++ (notebook)

# 3/5 (4h): Nov-17/08:30
06 GPU programming (CUDA) (slides)
07 GPU programming (CUDA) (notebook)

# 4/5 (4h): Dec-01/08:30
08 Introduction to git (notebook)

# 5/5 (4h): Dec-07/13:30
09 Languages performances (notebook)
10 Parallel architecture (slides)

Ideas
   11 Multiprocessing (notebook)
   12 Multithreading (notebook)
   13 Cryptocurrencies (notebook)
   14 Mandelbrot (notebook)
   Matrix multiplication
   Convergence time
   Build a search algo
   https://fractalytics.io/moore-penrose-matrix-optimization-cuda-c
   https://github.com/ishanthilina/CUDA-Calculation-Experiements/tree/master/q1
   https://en.wikipedia.org/wiki/N-body_simulation
   Dask cuda
```

## Generic methods <a name="methods"></a>

##### Cuda executions

- Load Extension
```python:
import IPython
bulkhours.load_extra_magics(IPython)
# or 
bulkhours.init_env(login="jdoe", ip=IPython, pass_code="PASS_COURSE")
```

- Cuda basic extension: it compiles C/C++ code and exec it
```c:
%%compile_and_exec
#include <iostream>
int main() {
    for (int i = 0; i <= 10; ++i) {
        std::cout << i << std::endl;
    }
}
```

## Data <a name="data"></a>

#### `data/supercomputer-power-flops.csv`
The file has been downloaded from the page https://ourworldindata.org/grapher/supercomputer-power-flops

#### `data/supercomputer-power-flops.csv`
The file has been downloaded from the page https://ourworldindata.org/grapher/supercomputer-power-flops

