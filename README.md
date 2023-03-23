This package is a support library for different courses. 

1. [Plan of econometrics course](#planeco)
2. [Plan of High Performance Programming on GPU course](#planhpc)
3. [Course methods](#methods)
4. [Data information](#data)
5. [Other stuffs](#stuffs)


## Plan of econometrics course <a name="planeco"></a>

```
# 1/4 (4h): Mar-01/14:00
01 Descriptive statistics 
- Characteristics of random variables
- Standard distributions
- Cross sectional data

# 2/4 (4h): Mar-03/14:00
02 Regressions
- Fitting a model to a dataset
- Regressions techniques
- Linear regression
- Goodness of fit

# 3/4 (4h): Mar-08/14:00
03 Time-series predictions
- Time-series characteristics
- Exponential smoothing
- Trends and Seasonal components
- Holt models

# 4/4 (4h): Mar-10/14:00
04 Econometrics models
- Moving Average model
- AutoRegressive model
- ARMA model
- ARIMA model

Exercices: 
- investigating the French retraites system, predict APPLE revenues, fit the volatility smile, regress life expectency per country, Inequalities in salaries investigations, relationship between GDP and unemployement

Not presented
    Financial instruments
    Risk estimations
    Price anomalies
    Macroeconomic quantities
    Optimal portfolio construction
    Historic of financial crises
    Frequentist versus Bayesian statistics
    Systematic trading
    Yield curve
    Cryptocurrencies
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

Not presented
   11 Multiprocessing (notebook)
   12 Multithreading (notebook)
   13 Cryptocurrencies (notebook)
   14 Mandelbrot (notebook)
   Matrix multiplication
   Matrix inversion: https://fractalytics.io/moore-penrose-matrix-optimization-cuda-c
   N-body simulation: https://en.wikipedia.org/wiki/N-body_simulation
   A bit of Dash
```

## Methods <a name="methods"></a>

##### evaluation methods

You need to login to be properly evealuated:
```python:
bulkhours.init_env(login="john.d", pass_code="PASS_COURSE", env="econometrics")
bulkhours.init_env(login="john.d", pass_code="PASS_COURSE", env="hpcgpu")
```

##### Cuda methods

Cuda basic extension compiles C/C++/CUDA code and exec it
```c:
%%compile_and_exec
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


## Data information<a name="data"></a>


#### `bulkhours.get_data("supercomputers")`
The file has been downloaded from the page https://ourworldindata.org/grapher/supercomputer-power-flops

#### `bulkhours.get_data("life_expectancy_vs_gdp_2018")`
The file has been downloaded from the page https://ourworldindata.org/grapher/life-expectancy-vs-gdp-per-capita
Source: Maddison Project Database (2020); UN WPP (2022); Zijdeman et al. (2015)

#### `bulkhours.get_data("france.retraites")`
The file has been downloaded from the page https://www.insee.fr/fr/statistiques/2415121#tableau-figure1

#### `bulkhours.get_data("france.income")`
Distribution des salaires mensuels nets en équivalent temps plein (EQTP) en 2020
The file has been downloaded from the page https://www.insee.fr/fr/statistiques/6436313#tableau-figure2

#### `bulkhours.get_data("france.salaires")`
The file has been downloaded from the page https://www.insee.fr/fr/statistiques/6436313#tableau-figure2

#### `data/world_gdp_hist.csv`
"Data Source","World Development Indicators", "Last Updated Date","2022-12-22",

#### `bulkhours.get_data("co2.main")` `bulkhours.get_data("co2.mapmain")`
Data on CO2 and Greenhouse Gas Emissions by Our World in Data
- https://github.com/owid/co2-data/blob/master/owid-co2-codebook.csv
- Data source: https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv

#### `bulkhours.get_data("co2.concentrations")` or `bulkhours.get_data("co2.mapconcentrations")`
Data concentrations
- Data source: https://ourworldindata.org/atmospheric-concentrations

#### https://www.statsmodels.org/stable/index.html data
- Australian passengers: bulkhours.get_data("statsdata.air_passengers")
- bulkhours.get_data("statsdata.air")
- bulkhours.get_data("statsdata.aust")
- bulkhours.get_data("statsdata.livestock2")

#### https://www.cor-retraites.fr/
- bulkhours/data/demo-pop-pyram.xlsx
- bulkhours/data/Données septembre partie 1.xlsx
- bulkhours/data/Données_RA2022_P2.xlsx
- bulkhours/data/Données_RA2022_P4.xlsx
- bulkhours/data/Données septembre 2022 - partie 3.xlsx
- bulkhours/data/Données septembre 2022 - partie 5.xlsx
- bulkhours/data/Données complémentaires partie 2 RA 2022.xlsx

#### Other data
- bulkhours.get_data("world.macro")
- bulkhours.get_data("world.mappoverty")
- bulkhours.get_data("world.corruption")
- bulkhours.get_data("gmacro.us_gdp")
- bulkhours.get_data("gmacro.fr_gdp")
- bulkhours.get_data("wages")
- bulkhours.get_data("mincer.params") 
