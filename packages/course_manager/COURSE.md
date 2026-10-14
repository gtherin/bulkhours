# The course standard

One format for every platform that teaches with it: `course.toml`, the
markers, the two renders, the waves and their record, and the rules a
deployer honours. The code that reads it is `course_manager` (this
folder), the **only** loader and renderer: what `course-manager check`
accepts is what a platform can deploy. A platform adds its own binding -
which forge, which teams, which engine - and never a second reader.

**A shared standard between segregated projects**: each project holds its
own, identical copy of this folder (`course-manager --version` shows version
and fingerprint) and documents its own binding - which forge, which teams,
which deploy engine - in its own repository. Nothing here names a project.

A **course** is one organisation of the forge. Its `solution` repository
is the only one edited by hand; everyone who takes the course gets their own
repository, `<course>/<login>`, written by deployments.

```
<course>/solution/
  course.toml         this file's subject: what the course is, who it is for, its waves
  README.md           the students' front page - delivered by the first wave
  TEACHERS.md         how to teach it - never delivered (outside every lab)
  teacher/            teacher-only material - never delivered
  <lab>/<lab>.ipynb   one folder per lab; answers between the markers
```

`course-manager init <course>` writes this skeleton, `course-manager new <lab>` adds
a lab and a draft wave. `course.toml` is read by `course-manager` and by a
platform's deploy engine through the same loader (`course_manager.spec`): what
`check` accepts is what can be deployed. `package.toml` with `[package]`, the earlier
name, is still read.

## `[course]`

| Key | | |
|---|---|---|
| `name` | required | the organisation, lowercase: `use_cases` |
| `title` | | shown on the course card |
| `status` | | `active` (default) or `past`: a past course is kept as a record - its people keep their repositories, nothing is deployed from it |
| `delivery` | | `engine` (default) or `external`: a course delivered by its own tool. The platform shows it (teachers, waves, who has them) and never deploys to it, nor creates, changes or audits its teams. Its file lives with the platform (`courses/<org>/course.toml`), not in the organisation; its `released` is written by hand. With it: `source` and `published`, the organisation's teacher and published repositories |
| `kernel` | | the kernel the notebooks ask for: `python3`, `<project>-env` |
| `teachers` | | the course's teachers, forge logins: `["ada", "guillaume"]`. Its `teachers` team is exactly this list (kept in step by the engine). Absent: the platform's teachers |
| `audience` | | the cohorts it is for: `["@m1.students", "@m2.students"]`. Default `who` of every wave. `@teachers` is the course's own `teachers` (to receive the student version as students do), not the platform team |
| `teacher` | | patterns never delivered to students, from any lab: `["teacher/", "*.teacher.*"]` |
| `renderer` | | `markers` (default); the older value of this key names the same, single renderer and is kept so older files still load |
| `moodle` | | the course's Moodle page: `https://moodle.example.org/course/view.php?id=123`, linked on its card |

No `hub`: which machine a cohort works on belongs to the deployment.

## `[wave.<name>]` - a release

A wave is named by what it delivers - `[wave.microintro]` - and the waves go
in the order of the file: that order is the course's, on the Courses page and
in the README program. The name labels the delivery (the `deploy <name>`
commit by which the engine knows who has it); **never rename a wave once it
has been delivered**: it would be a new delivery for everyone who has it.
Several deliveries in one wave: `[wave.<name>.lab.<x>]`, one table each.
`id` / `lab`, in files written before 2026-10-14, still override the name.

| Key | | |
|---|---|---|
| `title` | | shown on the card |
| `content` | | **what is delivered**: files and folders, at their paths in `solution`. Default `["<name>/"]` |
| `exclude` | | build output, caches, run artifacts: delivered to nobody |
| `who` | | the cohorts it may go to. Default: `[course] audience` |
| `summary` | | its row in the README's `{{program}}` - shown to a person once the wave reached them, the title only before |
| `released` | | **the cohorts it has been deployed to - a record, written by the deploy engine** after each deployment. A list, never true/false; `[]` or absent: not deployed yet |
| `at` | | `2026-10-20T09:00:00+02:00`: deployed on its own at that time to each cohort of `who` that does not have it yet (within 24 h; a date already long past waits for a click) |

```toml
[wave.microintro]
title = "Microstructure: introduction"
content = ["microintro/"]
summary = "The first notebook: the intraday activity profile."
released = ["@m2.students"]          # written by the engine: M2 has it, M1 not yet
```

## What a deployment writes

- **The same structure as `solution`:** a file is delivered at its own path.
  `README.md` at the root stays `README.md`; `microintro/microintro.ipynb`
  stays there.
- **The student version:** the markers below (Otter Grader's format, see
  *Markers*) remove the answers and leave `...` or the prompt in their place.
  Notebook outputs and execution counts are cleared. `teacher` patterns and
  `.bulkignore` keep files back.
- **The leak check:** a line only a teacher may see, found in the student
  version, stops the build - and so the deployment.
- **The teacher version** keeps everything; `course-manager preview` writes both
  under `~/preview/<course>/`.
- **Placeholders, filled for each person:** in a delivered text file
  (Markdown, notebooks, `.py`, config...), `{{login}}` becomes the person's
  forge login and `{{course}}` the course's name. `solution` and the teacher
  version keep them as written. For example, in the students' README:
  `git clone https://<forge>/{{course}}/{{login}}.git ~/{{course}}`.

## Markers

The format of [Otter Grader](https://otter-grader.readthedocs.io/en/latest/otter_assign/notebook_format.html)
(Berkeley, Data 8); `# BEGIN SOLUTION` / `# END SOLUTION` is also nbgrader's.
A lab written for Otter renders here unchanged. Markers work in every code
cell of a notebook and in every `.py`; they never span cells. Upper case only:
`# the solution` is an ordinary comment.

| In `solution` | The student gets | |
|---|---|---|
| `nine = square(3)  # SOLUTION` | `nine = ...` (an assignment keeps its left-hand side) | Otter |
| `return y  # SOLUTION` | `return ...` | Otter |
| `y = x * x  # SOLUTION NO PROMPT` | nothing: the line is removed | Otter |
| `np.random.seed(42)  # SEED` | nothing (the teacher's runs stay reproducible) | Otter |
| `# BEGIN SOLUTION` ... `# END SOLUTION` | `...` at the block's indentation, or the PROMPT block next to it | Otter |
| `# BEGIN SOLUTION NO PROMPT` ... `# END SOLUTION` | nothing | Otter |
| `""" # BEGIN PROMPT` ... `"""; # END PROMPT` | the lines in between, as written | Otter |
| `# IGNORE` as the first line of a cell | the cell is in neither version | Otter |
| `total = sum(xs)  # SOLUTION: 0` | `total = 0`: a starting value instead of `...` | extension |
| `k = window(5)  # SOLUTION REPLACE: k = 5` | `k = 5`: the whole line replaced | extension |
| `# PROMPT: # Hint: a rolling window` | `# Hint: a rolling window` (student only) | extension |
| `# BEGIN PROMPT` ... `# END PROMPT`, lines as comments | the lines, uncommented | extension |

- **The teacher version** keeps the code, drops the markers and the prompts.

### Languages: one set of words, two comment leaders

The words are the same in every language; only the comment leader changes:
`#` for Python, R and shell, `//` for C, C++, CUDA, Java, JavaScript, Rust and
Go. The file's suffix decides (`.py` `.ipynb` `.r` `.sh` / `.c` `.cc` `.cpp`
`.cxx` `.h` `.hpp` `.cu` `.cuh` `.java` `.js` `.ts` `.rs` `.go`); for a
notebook, the kernel's language. A file never mixes the two: in a `.cu`,
`# SOLUTION` is prose, as `// SOLUTION` is in a `.py`. Every file of these
suffixes goes through the markers - a helper module or a `.h` hides its
answers the same way as the notebook.

**The hole is `...`, in every language** - the convention since the first
renderer of these markers: `...` and `# ...` in Python, `/* ... */` and `// ...` in
C++. A consigne goes in a PROMPT: `// PROMPT: // ... : complete the loop` gives
the student `// ... : complete the loop`. (The CUDA course used
`// ___TODO___ :` before 2026-10-14; new stages use `// ... :`.)

| Python | C++ / CUDA | The student gets |
|---|---|---|
| `x = f(3)  # SOLUTION` | `int x = f(3);  // SOLUTION` | `int x = /* ... */;` - type, name and `;` kept; it does **not** compile, so the compiler points at every hole |
| `return y  # SOLUTION` | `return y;  // SOLUTION` | `return /* ... */;` |
| `x = f(3)  # SOLUTION: 0` | `int x = f(3);  // SOLUTION: 0` | `int x = 0;` - this is how a skeleton stays **compilable** |
| `# SOLUTION REPLACE: k = 5` | `// SOLUTION REPLACE: k = 5;` | the line given |
| `# SOLUTION NO PROMPT`, `# SEED` | `// SOLUTION NO PROMPT`, `// SEED` | nothing |
| `# BEGIN SOLUTION` ... `# END SOLUTION` | `// BEGIN SOLUTION` ... `// END SOLUTION` | `// ...` at the block's indentation (an empty body often compiles), or the PROMPT block next to it |
| `# BEGIN PROMPT`, lines as comments, `# END PROMPT` | `// BEGIN PROMPT`, lines as `//` comments, `// END PROMPT` | the lines, uncommented |
| `""" # BEGIN PROMPT` ... `"""; # END PROMPT` | `#if 0 // BEGIN PROMPT` ... `#endif // END PROMPT` | the lines as written - and the teacher's source compiles, the preprocessor drops the consigne |
| `# PROMPT: # a hint` | `// PROMPT: // ... : a hint` | `// ... : a hint` (student only) |
| `# IGNORE` | `// IGNORE` | the cell is in neither version (notebooks) |
| `# BULKHOURS.INIT:0` | `// BULKHOURS.INIT:0` | `int n = 0  // ...` - the older names, read with either leader |

The leak check, the exercise count and the two renders are the same code for
both leaders (`course_manager.render.MARKERS`).
- **Exercises:** each SOLUTION line or block counts one (SEED and PROMPT do not).
- **The leak check** covers every marker: a teacher line found in the
  student version stops the build. So does anything that looks like a marker
  and is not one (`# SOLUTIONS`, `# BEGIN SOLUTIONS`): a misspelt marker is a
  solution delivered.
- **bulkhours:** labs written for it keep working - `# BULKHOURS.<op>` and
  `# BKRESET.<op>` (INIT, REPLACE, REMOVE:LINE, REMOVE:START/END, PRINT).
- **Not taken from Otter:** its grading (`# BEGIN QUESTION`, tests, `# HIDDEN`).

## The rules

Each rule is enforced by code, never by someone remembering it. The standard
names the rule; the platform names the code (for MaQI: `package-deploy.py`
and the API behind its courses page). A platform with `delivery = "external"`
honours 5-7 and 17 and leaves the rest to the course's own tool.

**Rights** - checked by the platform's audit before every deployment, which
refuses to deploy anything while one of them is broken.

1. The organisation is private. Its only teams are `Owners` and `teachers`.
2. `teachers` has write on every repository of the course. Its members are the
   course's `teachers` list - exactly, kept in step by the engine (added and
   removed) - or, without one, the platform's teachers, owners and admins.
   Anyone else in it is refused.
3. `solution` is read by the teachers only: no other collaborator, no fork.
4. Each person's repository `<course>/<login>` has exactly one collaborator,
   that person, with write - never admin.

**Who deploys and who sees** - checked per course by the platform.

5. Only the admins, on every course, and the course's own `teachers` deploy.
   A course's teachers see and deploy it whatever their teams on the
   platform: being in its `teachers` list is enough, no cohort or platform
   team is needed.
6. A course opens for a cohort with its first deployment to that cohort.
   Before, its people have nothing: no repository, no access.
7. A student sees a course while they are in a cohort a deployment reached and
   have a repository in it. Taken out of the cohort, they keep their
   repository; the course leaves their courses page.

**Deploying a wave** - the platform's deploy engine.

8. A wave can be deployed to any cohort of its `who` (default: `[course]
   audience`) that has people in it. Nothing has to be opened first.
9. `released` is the **record** of where a wave went: after a deployment that
   reached people, the engine adds those cohorts to it in `course.toml` (a
   commit "<wave> deployed to <cohorts>", naming who asked). It is a list of
   cohorts of `who`; `true`, `false` or a bare string is an error.
10. A dated wave (`at`) goes once to each cohort of `who` that does not have
    it, within 24 hours of its time; a date already long past waits for a
    click. It never touches homes.

**What a deployment does** - the deploy engine.

11. It commits into people's repositories (git). Updating their copy in their
    home is a separate choice, **off by default**: people pull when they choose.
12. **The guard:** anyone who changed a file of the lab since its last
    deployment - pushed, or only in their clone - is skipped and named.
13. **Force** overrides the guard. In git their files are overwritten, their
    commits staying in the history. In their home the copy is reset to the
    repository, after everything they had (changes, new files, own commits)
    is committed on a local branch `before-deploy-<date>` (the platform may
    prefix it).
14. A deployment removes a file only if an earlier deployment of the same lab
    delivered it, the person has not changed it since, and no other lab of the
    run writes it.
15. A lab may deliver `README.md` at the root: it is then the students' front
    page, and the engine's own one stays out of the way.
16. A deployment request runs **once**: handled requests are remembered on
    their own list, and a request more than a day old is never run. A request
    refused before reaching anyone (a draft, an empty cohort) is not recorded
    as a cohort's result.
17. A `past` course is never deployed to, by hand or by date; its card says
    so, and its people still see it with their repository.

## Who sees what

| | sees | deploys |
|---|---|---|
| admins | every course | yes |
| the course's `teachers` team | `solution`, every person's repository | yes |
| someone in a cohort a wave reached | their own repository | no |
| anyone else | nothing - the organisation is private | no |

A course opens for a cohort with its first deployment. A person who leaves the
cohort keeps their repository; the course leaves their courses page.
