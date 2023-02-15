import pandas as pd


perfs = {
    "energy": {
        "C": 1,
        "Rust": 1.03,
        "C++": 1.34,
        "Ada": 1.70,
        "Java": 1.98,
        "Pascal": 2.14,
        "Chapel": 2.18,
        "Lisp": 2.27,
        "Ocaml": 2.40,
        "Fortran": 2.52,
        "Swift": 2.79,
        "Haskell": 3.10,
        "C#": 3.14,
        "Go": 3.23,
        "Dart": 3.83,
        "F#": 4.13,
        "JavaScript": 4.45,
        "Racket": 7.91,
        "TypeScript": 21.50,
        "Hack": 24.02,
        "PHP": 29.3,
        "Erlang": 42.23,
        "Lua": 45.98,
        "Jruby": 46.54,
        "Ruby": 69.91,
        "Python": 75.88,
        "Perl": 79.58,
    },
    "time": {
        "C": 1.00,
        "Rust": 1.04,
        "C++": 1.56,
        "Ada": 1.85,
        "Java": 1.89,
        "Chapel": 2.14,
        "Go": 2.83,
        "Pascal": 3.02,
        "Ocaml": 3.09,
        "C#": 3.14,
        "Lisp": 3.40,
        "Haskell": 3.55,
        "Swift": 4.20,
        "Fortran": 4.20,
        "F#": 6.30,
        "JavaScript": 6.52,
        "Dart": 6.67,
        "Racket": 11.27,
        "Hack": 26.99,
        "PHP": 27.64,
        "Erlang": 36.71,
        "Jruby": 43.44,
        "TypeScript": 46.20,
        "Ruby": 59.34,
        "Perl": 65.79,
        "Python": 71.90,
        "Lua": 82.91,
    },
    "memory": {
        "Pascal": 1.00,
        "Go": 1.05,
        "C": 1.17,
        "Fortran": 1.24,
        "C++": 1.34,
        "Ada": 1.47,
        "Rust": 1.54,
        "Lisp": 1.92,
        "Haskell": 2.45,
        "PHP": 2.57,
        "Swift": 2.71,
        "Python": 2.80,
        "Ocaml": 2.82,
        "C#": 2.85,
        "Hack": 3.34,
        "Racket": 3.52,
        "Ruby": 3.97,
        "Chapel": 4.00,
        "F#": 4.25,
        "JavaScript": 4.59,
        "TypeScript": 4.69,
        "Java": 6.01,
        "Perl": 6.62,
        "Lua": 6.72,
        "Erlang": 7.20,
        "Dart": 8.64,
        "Jruby": 19.84,
    },
}


def get_languages_perf():
    """References:
    - https://dl.acm.org/doi/10.1145/3136014.3136031
    - https://en.wikipedia.org/wiki/The_Computer_Language_Benchmarks_Game

    They used 10 problems from the Computer Language Benchmarks Game,
    a free software project for comparing performance which includes a standard set of simple
    algorithmic problems, as well as a framework for running tests.
    (It was formerly known as “The Great Computer Language Shootout.”)
    “This allowed us to obtain a comparable, representative, and extensive set of programs… along with the compilation/execution options,
    and compiler versions.”"""

    print("A bit more about the data: https://en.wikipedia.org/wiki/The_Computer_Language_Benchmarks_Game")
    return pd.DataFrame(perfs)
