
# In few lines

BulkHours was started as a standalone project:
- To build a real interactivity between students and a teacher (through Jupyter notebooks).
- To serve as as data provider, to support courses.

After a successful use of the package in several courses, I have decided to share it with you.
The industrialization of the package is still on-going and the aim reamains the same as before:
- Tools to easily share information between several notebooks,
- Facilitate the students follow-up by a teacher [evaluation_cell_id](#evaluation_cell_id),
- Tools to automaticaly evaluate exercices,
- Integration of a variety of useful data to feed courses,
- Tools to develop in C/C++/CUDA within a jupyter notebook environement

![](data/BulkHours.png)


# Access someone else cell content

A typical case is a student and a teacher who wants to share cell information:

![](data/Evaluation.gif)


### `evaluation_cell_id` <a name="evaluation_cell_id"></a>

To evaluate a notebook, you need to tag a cell using `evaluation_cell_id` magic method (lmine or cell). 
By doing this, your cell will link several users cells (example: between one teacher with his students).


```console
%%evaluation_cell_id -h 

usage: %%evaluation_cell_id -i CELL_ID 
            [-t {base,checkboxes,bkcode,code_project,codetext,floatslider,formula,intslider,markdown,radios,bkscript,table,textarea}]
            [-w WIDGETS] [-l LABEL] [-o OPTIONS] [-d DEFAULT]
            [-u USER] [-a ANSWER] [-h] [-p PUPPET]
```

You have several types of cell available, 



- [Data information page](data/README.md)
- Method [student_evaluation_function](#student_evaluation_function)
- Method [is_equal](#is_equal)
- Method [student_explanation_function](#student_explanation_function)
- Method [compile_and_exec](#compile_and_exec)
- [Plan of High Performance Programming on GPU course](bulkhours/hpc/README.md)
- [Plan of the econometrics course](bulkhours/ecox/README.md)



### `compile_and_exec` <a name="compile_and_exec"></a>

Working with Cuda/C++ methods



```console
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


### `student_evaluation_function` <a name="student_evaluation_function"></a>


In a cell with the magic method `evaluation_cell_id` activated, 
the codes of the student and the codes of the teacher are both run (using the current notebook previous variables).
So variables of the cells are available in 2 different contexts: ``teacher` `student`.
Example:

```python
data_test = image2vector(image)

def student_evaluation_function():
    data_ref = np.array([[0.67826139, 0.29380381, 0.90714982]])
    score = 0
    if np.max(np.abs(student.data_test-data_ref)) < 0.001:
        score += 2
    # Should be the same test than the previous one, assuming, teacher.my_tested_data = data_ref
    if np.max(np.abs(student.my_tested_data-teacher.my_tested_data)) < 0.001:
        score += 2
    return score
```

This code is also run to estimate students notes


### `is_equal` <a name="is_equal"></a>


norm = Linf-norm, L2-norm, L1-norm, 
distance = norm(|data_test - data_ref|)

# policy strict
score = max_score if |distance < error| else min_score

# policy gaussian
score = exp(-((distance / error) ** 2) / 2) * (max_score - min_score) + min_score

```python
def is_equal(data_test, data_ref, norm="Linf-norm", error=1e-8, policy="strict", min_score=0, max_score=10,
):
```

- `data_test` should be:
- a numpy compatible object (pandas.DataFrame, float, int, ...)
- a list, should be converted in a numpy.array
- a string (distance is estimated using a Ratcliff-Obershelp algorithm)

```python

m_test = np.array([[0., 3, 4], [1, 6, 4]])
num_px = [1, 3]
m_train = np.array([[0., 3, 5], [1, 6, 4]])
iterations = 1990
print("This is my standard output")

def student_evaluation_function(max_score=10, debug=False, run=False, run=False):
    score = 1
    cost = 0.9525741268
    score += bulkhours.is_equal(student.m_test, max_score=1)
    score += bulkhours.is_equal(data_test=student.num_px, max_score=1)
    score += bulkhours.is_equal(data_test=student.m_train, teacher.m_train, max_score=1)
    score += bulkhours.is_equal(cost, data_ref=0.9525741268, max_score=1)
    score += bulkhours.is_equal(student.iterations, data_ref=2000, policy="gaussian", error=1e-8, max_score=1)

    # Compare standard outputs of student and teacher executions. Strings distances are estimated using a Ratcliff-Obershelp algorithm
    score += bulkhours.is_equal(student.stdout, teacher.stdout, policy="gaussian", error=0.2, max_score=1)

    return score
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

### `student_explanation_function` <a name="student_explanation_function"></a>

```python
def student_explanation_function():
    ax = plt.hist(np.round((np.random.normal(loc=teacher.answer, scale=20, size=1000))), bins=20, label="Sondage")
    plt.vlines(teacher.answer, 0, 35, color="red", label=f"Valeur actuelle: %sm" % teacher.answer)
    plt.vlines(student.answer, 0, 35, color="orange", label="Votre estimation: %sm" % student.answer)
    plt.legend()
```

