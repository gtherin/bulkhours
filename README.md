This package is a support library for different courses. 


1. [Data information page](data/README.md)
2. [Plan of High Performance Programming on GPU course](bulkhours/hpc/README.md)
3. [Plan of the econometrics course](bulkhours/ecox/README.md)
4. [Methods](#methods)


## Methods <a name="methods"></a>

[evaluation_cell_id](#evaluation_cell_id)
[student_evaluation_function](#student_evaluation_function)
[student_explanation_function](#student_explanation_function)
[compile_and_exec](#compile_and_exec)


##### `evaluation_cell_id` <a name="evaluation_cell_id"></a>

To evaluate a notebook, you need to tag a cell using `evaluation_cell_id` magic method (lmine or cell). 
By doing this, your cell will link several users cells (example: between one teacher with his students).

```python
%%evaluation_cell_id -h 

usage: %%evaluation_cell_id -i CELL_ID 
            [-t {base,checkboxes,bkcode,code_project,codetext,floatslider,formula,intslider,markdown,radios,bkscript,table,textarea}]
            [-w WIDGETS] [-l LABEL] [-o OPTIONS] [-d DEFAULT]
            [-u USER] [-a ANSWER] [-h] [-p PUPPET]
```

You have several types of cell available, 

##### `student_evaluation_function` <a name="student_evaluation_function"></a>


- data_test should be a numpy compatible object

```python
def student_evaluation_function(max_score=10, debug=False, run=False, run=False):
    score = 1
    score += bulkhours.is_equal(data_test=student.m_train, teacher.m_train, max_score=1)
    score += bulkhours.is_equal(m_test, max_score=1)
    score += bulkhours.is_equal(student.num_px, max_score=1)
    score += bulkhours.premium.is_equal(data_test, data_ref=0.9525741268, max_score=1)
    score += bulkhours.premium.is_equal(data_test, data_ref=0.9525741268, max_score=1)
    score += bulkhours.premium.is_equal(data_test, data_ref=3, policy="gaussian", error=1e-8, max_score=1)
    score += bulkhours.is_equal(student.stdout, teacher.stdout, policy="gaussian", error=0.2, max_score=1)

    return score
```

```python:
def student_evaluation_function(max_score=10):
    data_ref = np.array([[0.67826139, 0.29380381, 0.90714982]])
    if np.max(np.abs(image2vector(image)-data_ref)) < 0.001:
        return max_score
    return 0
```

```c
%%evaluation_cell_id -i cpp -w scoa -l Construire une suite géométrique de raison 2 en C++, de 2 a 1024
%%compile_and_exec -c g++
#include <iostream>

int main() {
    int pow2 = 1;
    for (int i = 1; i < 10; ++i)
    {
      pow2 *= 2;
      std::cout << pow2 << " ";
    }
}

float student_evaluation_function(bool debug=false, bool run=false, bool show_code=false) {
    return bulkhours.is_equal(student.stdout, teacher.stdout, policy="gaussian", error=0.1);
}
```

##### `student_explanation_function` <a name="student_explanation_function"></a>

```python
def student_explanation_function():
    ax = plt.hist(np.round((np.random.normal(loc=teacher.answer, scale=20, size=1000))), bins=20, label="Sondage")
    plt.vlines(teacher.answer, 0, 35, color="red", label=f"Valeur actuelle: %sm" % teacher.answer)
    plt.vlines(student.answer, 0, 35, color="orange", label="Votre estimation: %sm" % student.answer)
    plt.legend()
```

##### `compile_and_exec` <a name="compile_and_exec"></a>

Working with Cuda/C++ methods


```python
usage: ipykernel_launcher.py [-h] [-t] [-c {nvcc,g++,gcc}]

compile_and_exec params

options:
  -h, --help            show this help message and exit
  -t, --timeit          flag to return timeit result instead of stdout
  -c {nvcc,g++,gcc}, --compiler {nvcc,g++,gcc}
usage: ipykernel_launcher.py [-h] [-t] [-c {nvcc,g++,gcc}]

compile_and_exec params

options:
  -h, --help            show this help message and exit
  -t, --timeit          flag to return timeit result instead of stdout
  -c {nvcc,g++,gcc}, --compiler {nvcc,g++,gcc}
```

Cuda basic extension compiles C/C++/CUDA code and exec it
```c
%%evaluation_cell_id -i demo_cuda
%%compile_and_exec -c nvcc
#include <iostream>
int main() {
    for (int i = 0; i <= 10; ++i) {
        std::cout << i << std::endl;
    }
}
```


