"""course-manager on a small example course: the format, and that no answer
reaches a student. Standard library only:
    python3 -m unittest discover -s tests"""
import json
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from course_manager import spec                      # noqa: E402
from course_manager.render import do_render          # noqa: E402
from course_manager.spec import CourseError          # noqa: E402

ANSWER = "activity = trades.resample('5min').size()"


def notebook(cells):
    return json.dumps({"cells": cells, "metadata": {}, "nbformat": 4, "nbformat_minor": 5})


def code(src, outputs=None):
    return {"cell_type": "code", "id": "x", "metadata": {}, "source": src,
            "outputs": outputs or [], "execution_count": 3 if outputs else None}


class Course:
    """A course in a temporary folder."""
    def __init__(self, toml, files):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "course.toml").write_text(textwrap.dedent(toml), encoding="utf-8")
        for rel, text in files.items():
            p = self.root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")

    def build(self, lab):
        course, labs = spec.load(self.root)
        do_render(self.root, course, lab, labs[lab], notebooks=True)
        return self.root / "build"


TOML = '''
[course]
name = "toy"
audience = ["@m0.students", "@m1.students"]
teacher = ["teacher/", "*.teacher.*"]

[wave.w0]
lab = "init"
content = ["README.md"]
released = ["@m0.students"]

[wave.w1]
lab = "intro"
content = ["intro/"]
exclude = ["runs/"]
released = []
'''
FILES = {
    "README.md": "# Toy course\n",
    "intro/intro.ipynb": notebook([
        {"cell_type": "markdown", "id": "m", "metadata": {}, "source": "Count the trades."},
        code("# BEGIN SOLUTION\n%s\n# END SOLUTION\n# BEGIN PROMPT\n# activity = ...\n"
             "# raise NotImplementedError('count them')\n# END PROMPT\n" % ANSWER,
             outputs=[{"output_type": "stream", "name": "stdout", "text": "42 trades\n"}]),
    ]),
    "intro/helper.py": "def f():\n    # BEGIN SOLUTION\n    return 41 + 1\n    # END SOLUTION\n"
                       "    # BEGIN PROMPT\n    # return ...\n    # END PROMPT\n",
    "intro/notes.teacher.md": "the answer is 42\n",
    "intro/runs/model.bin": "weights",
    "teacher/plan.md": "week 1\n",
}


class TestSpec(unittest.TestCase):
    def test_released_is_a_list_of_cohorts(self):
        who = ["@m1.students", "@m2.students"]
        self.assertEqual(spec.released_to(None, who), ([], []))
        self.assertEqual(spec.released_to([], who), ([], []))
        self.assertEqual(spec.released_to(["m2.students"], who), (["@m2.students"], []))
        for bad in (True, False, "@m2.students"):
            self.assertIn("must be a list", spec.released_to(bad, who)[1][0])
        self.assertIn("not in who", spec.released_to(["@m3.students"], who)[1][0])

    def test_course_toml_first_package_toml_still_read(self):
        c = Course(TOML, {})
        (c.root / "package.toml").write_text('[package]\nname = "old"\n', encoding="utf-8")
        self.assertEqual(spec.load(c.root)[0]["name"], "toy")
        (c.root / "course.toml").unlink()
        self.assertEqual(spec.load(c.root)[0]["name"], "old")

    def test_waves(self):
        c = Course(TOML, {})
        w = spec.waves(spec.parse((c.root / "course.toml").read_text()))
        self.assertEqual(w["w0"]["who"], ["@m0.students", "@m1.students"])
        self.assertEqual(w["w0"]["released"], ["@m0.students"])
        self.assertEqual(w["w1"]["released"], [])

    def test_mistakes_are_reported(self):
        with self.assertRaises(CourseError):
            spec.labs_of(spec.parse('[wave.a]\nlab = "x"\n[wave.b]\nlab = "x"\n'))
        w = spec.waves(spec.parse('[course]\nname="t"\n[wave.a]\nlab = "x"\nlabs = ["y"]\n'),
                       labs={"x": {}})
        self.assertIn("unknown lab", w["a"]["error"])


class TestBuild(unittest.TestCase):
    def setUp(self):
        self.c = Course(TOML, FILES)

    def test_structure_of_solution_is_kept(self):
        b = self.c.build("init")
        self.assertTrue((b / "student" / "init" / "README.md").is_file())
        b = self.c.build("intro")
        self.assertTrue((b / "student" / "intro" / "intro" / "intro.ipynb").is_file())

    def test_student_gets_no_answer_and_no_output(self):
        b = self.c.build("intro")
        nb = json.loads((b / "student" / "intro" / "intro" / "intro.ipynb").read_text())
        src = "".join("".join(c["source"]) for c in nb["cells"])
        self.assertNotIn(ANSWER, src)
        self.assertIn("NotImplementedError", src)
        self.assertTrue(all(not c.get("outputs") for c in nb["cells"] if c["cell_type"] == "code"))
        self.assertNotIn("41 + 1", (b / "student" / "intro" / "intro" / "helper.py").read_text())

    def test_teacher_gets_everything(self):
        b = self.c.build("intro")
        nb = json.loads((b / "teacher" / "intro" / "intro" / "intro.ipynb").read_text())
        src = "".join("".join(c["source"]) for c in nb["cells"])
        self.assertIn(ANSWER, src)
        self.assertTrue((b / "teacher" / "intro" / "intro" / "notes.teacher.md").is_file())

    def test_teacher_files_and_exclusions_stay_back(self):
        b = self.c.build("intro")
        self.assertFalse((b / "student" / "intro" / "intro" / "notes.teacher.md").exists())
        self.assertFalse((b / "student" / "intro" / "intro" / "runs").exists())
        self.assertFalse((b / "teacher" / "intro" / "intro" / "runs").exists())

    def test_an_answer_in_the_prompt_stops_the_build(self):
        leaky = dict(FILES)
        leaky["intro/intro.ipynb"] = notebook([code(
            "# BEGIN SOLUTION\n%s\n# END SOLUTION\n# BEGIN PROMPT\n# %s\n# END PROMPT\n" % (ANSWER, ANSWER))])
        with self.assertRaises(CourseError):
            Course(TOML, leaky).build("intro")


class TestPersonalise(unittest.TestCase):
    def test_login_and_course_filled_in_text_only(self):
        from course_manager.render import personalise
        v = {"login": "john.doe", "course": "toy"}
        self.assertEqual(personalise(b"clone .../{{course}}/{{ login }}.git {{other}}", "README.md", v),
                         b"clone .../toy/john.doe.git {{other}}")
        self.assertEqual(personalise(b"{{login}}", "weights.bin", v), b"{{login}}")


if __name__ == "__main__":
    unittest.main()


class Markers(unittest.TestCase):
    """Otter Grader's markers, the extensions, and the older names."""
    def r(self, src, variant="student"):
        from course_manager.render import render
        return "".join(render(textwrap.dedent(src).splitlines(True), variant))

    def test_otter_one_line(self):
        src = """\
            def square(x):
                y = x * x  # SOLUTION NO PROMPT
                return y  # SOLUTION
            nine = square(3)  # SOLUTION
            np.random.seed(42)  # SEED
            """
        self.assertEqual(self.r(src), "def square(x):\n    return ...\nnine = ...\n")
        self.assertEqual(self.r(src, "teacher"), "def square(x):\n    y = x * x\n    return y\nnine = square(3)\nnp.random.seed(42)\n")

    def test_otter_blocks(self):
        src = """\
            if True:
                # BEGIN SOLUTION
                radius = 3
                area = radius * pi * pi
                # END SOLUTION
                print(area)
            def circumference(r):
                # BEGIN SOLUTION NO PROMPT
                return 2 * pi * r
                # END SOLUTION
                \"\"\" # BEGIN PROMPT
                # Next, define a circumference function.
                pass
                \"\"\"; # END PROMPT
            """
        self.assertEqual(self.r(src), "if True:\n    ...\n    print(area)\ndef circumference(r):\n"
                                      "    # Next, define a circumference function.\n    pass\n")
        t = self.r(src, "teacher")
        self.assertIn("    return 2 * pi * r\n", t)
        self.assertNotIn("Next, define", t)

    def test_commented_prompt_takes_the_place_of_the_dots(self):
        src = """\
            # BEGIN SOLUTION
            x = solve()
            # END SOLUTION
            # BEGIN PROMPT
            # x = ...
            # END PROMPT
            """
        self.assertEqual(self.r(src), "x = ...\n")

    def test_extensions(self):
        src = """\
            def mean(xs):
                total = sum(xs)  # SOLUTION: 0
                return total / len(xs)  # SOLUTION: None
            k = compute_the_window_length(5)  # SOLUTION REPLACE: k = 5  # try others
            # PROMPT: # Hint: a rolling window
            """
        self.assertEqual(self.r(src), "def mean(xs):\n    total = 0\n    return None\n"
                                      "k = 5  # try others\n# Hint: a rolling window\n")
        t = self.r(src, "teacher")
        self.assertIn("    total = sum(xs)\n", t)
        self.assertNotIn("Hint", t)

    def test_ignore_cell(self):
        src = """\
            # %%
            x = 1
            # %%
            # IGNORE
            scratch_work_of_the_teacher()
            # %%
            y = 2
            """
        for v in ("student", "teacher"):
            self.assertEqual(self.r(src, v), "# %%\nx = 1\n# %%\ny = 2\n")

    def test_older_names_still_work(self):
        src = """\
            total = sum(xs)  # BULKHOURS.INIT: 0
            k = window(5)  # BKRESET.REPLACE: k = ...
            plot(k)  # BULKHOURS.REMOVE:LINE
            # BULKHOURS.PRINT: # Hint
            """
        self.assertEqual(self.r(src), "total = 0  # ...\nk = ...  # ...\n# ...\n# Hint\n")

    def test_exercises_counted(self):
        from course_manager.render import problems
        src = textwrap.dedent("""\
            a = compute_something_long(1)  # SOLUTION
            b = compute_something_long(2)  # SOLUTION: 0
            np.random.seed(42)  # SEED
            # BEGIN SOLUTION
            c = 3
            # END SOLUTION
            """).splitlines(True)
        self.assertEqual(problems(src), ([], 3))

    def test_a_misspelt_marker_stops_the_build(self):
        from course_manager.render import problems
        for bad in ("y = secret_answer()  # SOLUTION.INIT: 0\n", "# BEGIN SOLUTIONS\n",
                    "y = secret_answer()  # SOLUTIONS\n", "# END PROMPTS\n"):
            self.assertTrue(problems([bad])[0], bad)
        self.assertEqual(problems(["x = 1  # the solution of the exercise\n"])[0], [])   # lower case: a comment
        self.assertEqual(problems(["# Write `# SOLUTION` at the end of a line\n"])[0], [])   # quoted: prose

    def test_an_answer_left_outside_the_markers_is_a_leak(self):
        from course_manager.render import problems
        src = ["k = compute_the_window_length(5)  # SOLUTION\n", "k = compute_the_window_length(5)\n"]
        self.assertTrue(any("reaches the student" in e for e in problems(src)[0]))


class Program(unittest.TestCase):
    """The README's {{program}}: all waves, the summary only once received."""
    def test_no_spoil(self):
        from course_manager.render import program, personalise
        waves = {"w0": {"title": "Start", "labs": ["init"], "summary": ""},
                 "w1": {"title": "Intro", "labs": ["microintro"], "summary": "One exercise: the U."},
                 "w2": {"title": "The book.", "labs": ["orderbook"], "summary": "Eight exercises, Kyle's lambda."}}
        t = program(waves, {"init", "microintro"})
        self.assertEqual(t.splitlines()[2:], ["| 1 | **microintro** | *Intro.* One exercise: the U. |",
                                              "| 2 | **orderbook** | *The book.* Not released yet. |"])
        self.assertNotIn("lambda", t)
        out = personalise(b"# Course\n\n{{program}}\n", "README.md", {"program": t}).decode()
        self.assertIn("| 1 | **microintro**", out)
        self.assertIn("{{program}}", personalise(b"{{program}}", "README.md", {"login": "x"}).decode())  # no value: kept


class WaveId(unittest.TestCase):
    """A wave's name is its short name; waves keep the order of the file."""
    def test_name_order_and_old_keys(self):
        cfg = spec.parse(textwrap.dedent("""
            [course]
            name = "c"
            [wave.init]
            content = ["README.md"]
            [wave.w1]
            lab = "microintro"
            content = ["microintro/"]
            [wave.orderbook]
            [wave.alpha]
            content = ["a/", "b/"]
            """))
        w = spec.waves(cfg)
        self.assertEqual(list(w), ["init", "w1", "orderbook", "alpha"])          # the file's order, not sorted
        self.assertEqual([x["labs"] for x in w.values()], [["init"], ["microintro"], ["orderbook"], ["alpha"]])
        self.assertEqual([x["order"] for x in w.values()], [0, 1, 2, 3])
        self.assertEqual(spec.labs_of(cfg)["orderbook"]["content"], ["orderbook/"])


class Standalone(unittest.TestCase):
    """The invariants of a copy shared between segregated projects."""
    def test_imports_no_notebook_runtime(self):
        # A deploy engine imports this on a bare host: no host package and no
        # third-party module may come with it - the standard library only.
        import subprocess
        src = Path(__file__).resolve().parents[1] / "src"
        code = ("import sys; before = set(sys.modules); import course_manager, course_manager.render, "
                "course_manager.cli; new = {m.split('.')[0] for m in set(sys.modules) - before}; "
                "bad = new - set(sys.stdlib_module_names) - {'course_manager'}; "
                "print(sorted(bad))")
        r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, env={"PYTHONPATH": str(src), "PATH": "/usr/bin:/bin"})
        self.assertEqual(r.stdout.strip(), "[]", r.stderr)

    def test_renderer_names_are_one_renderer(self):
        from course_manager.render import render_with
        src = textwrap.dedent("""\
            total = sum(xs)  # BULKHOURS.INIT: 0
            k = f(5)  # SOLUTION
            """).splitlines(True)
        for v in ("student", "teacher"):
            self.assertEqual(render_with("bulkhours", src, v), render_with("markers", src, v))   # the older value of `renderer`
        with self.assertRaises(ValueError):
            render_with("other", src, "student")


class Cpp(unittest.TestCase):
    """The same words with `//`: C, C++ and CUDA sources; the hole is `...`."""
    def r(self, src, variant="student"):
        from course_manager.render import render
        return "".join(render(textwrap.dedent(src).splitlines(True), variant, leader="//"))

    def test_one_line_keeps_type_name_and_semicolon(self):
        src = """\
            int square(int x) {
                int y = x * x;  // SOLUTION NO PROMPT
                return y;  // SOLUTION
            }
            int nine = square(3);  // SOLUTION
            float eps = tolerance(grid);  // SOLUTION: 1e-3f
            std::vector<int>& v = pick(all);  // SOLUTION
            srand(42);  // SEED
            """
        self.assertEqual(self.r(src),
            "int square(int x) {\n    return /* ... */;\n}\nint nine = /* ... */;\nfloat eps = 1e-3f;\n"
            "std::vector<int>& v = /* ... */;\n")
        self.assertEqual(self.r(src, "teacher"),
            "int square(int x) {\n    int y = x * x;\n    return y;\n}\nint nine = square(3);\n"
            "float eps = tolerance(grid);\nstd::vector<int>& v = pick(all);\nsrand(42);\n")

    def test_blocks_prompt_as_comments_and_as_if0(self):
        src = """\
            __global__ void step(float2* p, int n) {
                // BEGIN SOLUTION
                const int i = blockIdx.x * blockDim.x + threadIdx.x;
                if (i < n) p[i].x += 1.f;
                // END SOLUTION
                // BEGIN PROMPT
                // // ... : un thread par particule, garde sur n
                // END PROMPT
            }
            void gpuInit(int count) {
            #if 0 // BEGIN PROMPT
                // ... : réserver count particules sur la carte
            #endif // END PROMPT
                // BEGIN SOLUTION NO PROMPT
                CUDA_CHECK(cudaMalloc(&d, count * sizeof(Particle)));
                // END SOLUTION
            }
            """
        self.assertEqual(self.r(src),
            "__global__ void step(float2* p, int n) {\n    // ... : un thread par particule, garde sur n\n}\n"
            "void gpuInit(int count) {\n    // ... : réserver count particules sur la carte\n}\n")
        t = self.r(src, "teacher")
        self.assertIn("    if (i < n) p[i].x += 1.f;\n", t)
        self.assertIn("    CUDA_CHECK(cudaMalloc(&d, count * sizeof(Particle)));\n", t)
        self.assertNotIn("...", t)
        self.assertNotIn("#if 0", t)

    def test_block_without_prompt_leaves_a_comment_hole(self):
        src = """\
            void f() {
                // BEGIN SOLUTION
                work();
                // END SOLUTION
            }
            """
        self.assertEqual(self.r(src), "void f() {\n    // ...\n}\n")

    def test_prompt_line_and_old_names_with_slashes(self):
        src = """\
            // PROMPT: // ... : compléter la boucle
            int n = count();  // BULKHOURS.INIT: 0
            launch(k);  // BULKHOURS.REMOVE:LINE
            """
        self.assertEqual(self.r(src), "// ... : compléter la boucle\nint n = 0  // ...\n// ...\n")

    def test_hash_is_prose_in_cpp_and_slashes_are_prose_in_python(self):
        from course_manager.render import problems, render
        cpp = ["#include <vector>\n", "#define N 4  // the grid\n", "int x = secret_value();  // SOLUTION\n", "int y = 2;  # SOLUTION\n"]
        errs, n = problems(cpp, leader="//")
        self.assertEqual((errs, n), ([], 1))
        self.assertIn("int y = 2;  # SOLUTION\n", "".join(render(cpp, "student", "//")))
        self.assertEqual(problems(["x = compute_the_answer()  // SOLUTION\n"])[1], 0)

    def test_a_cu_file_goes_through_the_markers_and_the_leak_check(self):
        toml = TOML.replace('content = ["intro/"]', 'content = ["kernel/"]')
        files = {"kernel/SimGpu.cu": "void gpuStep() {\n    // BEGIN SOLUTION\n    moveParticlesKernel<<<grid, block>>>(d, n, dt);\n"
                                     "    // END SOLUTION\n    // BEGIN PROMPT\n    // // ... : lancer le noyau\n    // END PROMPT\n}\n",
                 "kernel/README.md": "# Kernel\n"}
        c = Course(toml, files)                 # kept: its temporary folder lives as long as it does
        b = c.build("intro")
        student = (b / "student" / "intro" / "kernel" / "SimGpu.cu").read_text()
        self.assertEqual(student, "void gpuStep() {\n    // ... : lancer le noyau\n}\n")
        self.assertIn("moveParticlesKernel", (b / "teacher" / "intro" / "kernel" / "SimGpu.cu").read_text())
        leaky = dict(files); leaky["kernel/SimGpu.cu"] = files["kernel/SimGpu.cu"].replace("// // ... : lancer le noyau", "// moveParticlesKernel<<<grid, block>>>(d, n, dt);")
        c2 = Course(toml, leaky)
        with self.assertRaises(CourseError):
            c2.build("intro")

    def test_notebook_leader_from_kernel(self):
        from course_manager.render import notebook_leader
        self.assertEqual(notebook_leader({"metadata": {"kernelspec": {"language": "c++"}}}), "//")
        self.assertEqual(notebook_leader({"metadata": {"language_info": {"name": "python"}}}), "#")
        self.assertEqual(notebook_leader({}), "#")
