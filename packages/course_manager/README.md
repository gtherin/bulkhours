# course_manager

The course standard, and the one tool that reads it: `course.toml`, the markers
(Python and C++), the student and teacher renders with their leak check, the
waves and their record, the rules a deployer honours. The format is in
[COURSE.md](COURSE.md).

```
course-manager init <course>     the standard skeleton, with course.toml
course-manager new <lab>         a lab and a draft wave
course-manager check [lab]       markers balanced, no answer reaching the student version
course-manager preview [lab]     both versions under ~/preview/<course>/
course-manager status            every wave, its lab, who it is released to
course-manager build [lab]       what is delivered, under build/ (a deploy engine runs this)
course-manager --version         version and fingerprint of this copy
```

**A shared standard between segregated projects.** Each project that adopts
it holds its own, identical copy of this folder - no project depends on
another. `course-manager --version` prints the version and a fingerprint of
the copy's files: two copies that print the same line are the same standard.
A change is made in every copy or in none; the policy is the standard, not a
repository.

No dependency (jupytext only to turn `.py` notebooks into `.ipynb`:
`COURSE_JUPYTEXT` or on `PATH`). A host project may depend on its own copy for
its notebook markers; this package depends on nothing of its host, so importing
it loads no notebook runtime (asserted by a test).

Tests: `python3 -m unittest discover -s tests` (standard library only).
