#!/usr/bin/env python3
"""course-manager - author and deliver a course: one source, two versions.

A COURSE is a git repository with a `course.toml`. On a platform that deploys
it, it maps to one organisation of the forge: `solution` for the teachers, one
repository per person. Its LABS are released in WAVES: a wave names what it
delivers (`content`) and records the cohorts it reached (`released`). A lab is
written once and delivered in two versions (student, teacher):

    use_cases/                     the course (forge org `use_cases`, repo `solution`)
      course.toml                 [course] + one [wave.<w>] per release
      microintro/                  a lab
        microintro.ipynb           a notebook with the markers in its code cells
                                   (or microintro.py, jupytext py:percent)
      teacher/                     never delivered ([course] teacher patterns)

The student version: markers applied in every .py and every notebook cell,
outputs and execution counts cleared (a saved output can print the answer),
teacher files left out. The teacher version keeps everything.

Run it from inside the course, in your own account:

    course-manager init <course>       start a course in ./<course>
    course-manager new <lab>           add a lab (source + a draft wave)
    course-manager check [lab]         markers, leaks, data declared
    course-manager render [lab]        write both versions under build/
    course-manager build [lab]         what is delivered: notebooks, under build/
    course-manager preview [lab]       render + notebooks in ~/preview/<course>/
    course-manager status              every wave, its lab, who it is released to

THE MARKERS: Otter Grader's format (COURSE.md, "Markers", has the full table)

    x = answer()   # SOLUTION                  student: x = ...
    y = step()     # SOLUTION NO PROMPT        student: (line removed)
    seed(42)       # SEED                      student: (line removed)
    # BEGIN SOLUTION ... # END SOLUTION        student: ...  (or the PROMPT next to it)
    # BEGIN SOLUTION NO PROMPT ... # END SOLUTION          student: (removed)
    \"\"\" # BEGIN PROMPT ... \"\"\"; # END PROMPT   student: the lines in between
    # IGNORE  (first line of a cell)           the cell is in neither version
  and, beyond Otter:
    x = answer()   # SOLUTION: 0               student: x = 0
    x = answer()   # SOLUTION REPLACE: x = f() student: x = f()
    # PROMPT: # a hint                         student: # a hint  (student only)
    # BEGIN PROMPT ... # END PROMPT, as comments           student: uncommented

The source runs end to end as it is: open it, run all, and the solutions are
checked (a prompt is a string or comments, never live code).

THE BULKHOURS NAMES, the older dialect (`BKRESET.` is accepted for
`BULKHOURS.`), still read; the markers above are what new labs write. Both
may be mixed in one file.

    x = answer          # BULKHOURS.INIT:0          student: x = 0  # ...
    # BULKHOURS.REMOVE:START ... # BULKHOURS.REMOVE:END     student: # ...
    print(result)       # BULKHOURS.REMOVE:LINE     student: # ...
    long_answer()       # BULKHOURS.REPLACE:hint()  student: hint()  # ...
    # BULKHOURS.PRINT:hint = ...                    student: hint = ...  (student only)

Only text is rewritten, at render time: a student's notebook imports nothing.
`renderer = "markers"` (default) in [course] or in a wave; its older value
names the same, single renderer (COURSE_RENDERER overrides both).

THE LEAK CHECK: every substantial line of the source that only the teacher
may see (inside a SOLUTION or REMOVE block, or the teacher's side of INIT /
REPLACE / REMOVE:LINE) must be absent from the student output - checked on
the rendered file AND on the final notebook.

WHAT IS DELIVERED, AND .bulkignore
A lab delivers its whole folder: the notebook, helper modules (every .py goes
through the markers), small data, images. `.bulkignore` lists what is NOT
installed for students - same syntax as .gitignore, at the course root and/or
in a lab folder. The teacher version ignores it and gets everything. A new
course starts with `teacher/` and `*.teacher.*` ignored.

DEPLOYING TO PEOPLE is the platform's job, not this command's: its deploy
engine calls `build` and commits the result into each person's repository
(COURSE.md, "The rules"). This command never reaches the forge.

Environment: COURSE_JUPYTEXT (the jupytext to run), COURSE_RENDERER (override),
COURSE_HUB and COURSE_PREVIEW_URL (a template with {hub}, {user}, {rel} for
the preview's link), WASABI_BUCKETS (the buckets a data key opens here).
"""
import argparse
import os
import shutil
import sys
import tomllib
from pathlib import Path

from . import spec
from .spec import CourseError, NAME
from .render import (VARIANTS, problems, chunks, is_notebook, sub_files, do_render, MARKED, file_leader)

TTY = sys.stdout.isatty() and not os.environ.get("NO_COLOR")
def _c(code, s): return "\033[%sm%s\033[0m" % (code, s) if TTY else s
def ok(msg): print("  %s %s" % (_c("32", "✓"), msg))
def warn(msg): print("  %s %s" % (_c("33", "⚠"), msg))
def fail(msg): print("  %s %s" % (_c("31", "✗"), msg))
def title(msg): print("\n%s" % _c("1;36", "▶ " + msg))
def die(msg): fail(msg); sys.exit(1)


def find_root():
    try:
        return spec.find_root()
    except CourseError as e:
        die(str(e))


def load(root):
    try:
        return spec.load(root)
    except CourseError as e:
        die(str(e))


def chosen(subs, only):
    if only:
        if only not in subs:
            die("no lab %r - known: %s" % (only, ", ".join(subs) or "none"))
        return {only: subs[only]}
    if not subs:
        die("the package has no lab yet: course-manager new <name>")
    return subs



STARTER = '''# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#   kernelspec:
#     display_name: {kernel}
#     language: python
#     name: {kernel}
# ---

# %% [markdown]
# # {title}
#
# Write the statement here. One source, two versions:
#
# - `# SOLUTION` at the end of a line: the student gets `...` in its place;
# - between `# BEGIN SOLUTION` and `# END SOLUTION`: for the teacher only, and
#   the PROMPT block next to it is what the student gets instead.
# The markers are Otter Grader's: see COURSE.md, "Markers".

# %%
start = 0
stop = 10  # SOLUTION

# %%
# BEGIN SOLUTION
answer = sum(range(start, stop))
# END SOLUTION
""" # BEGIN PROMPT
answer = ...  # the sum of the integers from start to stop - 1
raise NotImplementedError("compute `answer`")
"""; # END PROMPT

# %%
assert answer == 45
'''


def cmd_init(a):
    if not NAME.match(a.name): die("package name: lowercase letters, digits, _ or -")
    root = Path(a.name)
    if spec.course_file(root): die("%s already holds a course" % root)
    root.mkdir(parents=True, exist_ok=True)
    (root / "course.toml").write_text(
        '# A course: one organisation on the forge, its labs released in waves.\n'
        '# Read by course-manager and the platform\'s deploy engine; keys in COURSE.md.\n\n'
        '[course]\n'
        'name = "%s"\n'
        'title = "%s"\n'
        'kernel = "%s"                         # the kernel the notebooks ask for\n'
        'audience = []                                    # who a wave goes to by default, e.g. ["@m2.students"]\n'
        'teacher = ["teacher/", "*.teacher.*"]            # never delivered, from any lab\n\n'
        '# A wave is a release; its lab is declared with it. `lab` names the folder.\n'
        '# released: the cohorts the wave may go to; [] is a draft.\n'
        % (a.name, a.title or a.name, a.kernel), encoding="utf-8")
    (root / ".gitignore").write_text("build/\n.ipynb_checkpoints/\n__pycache__/\n", encoding="utf-8")
    (root / "README.md").write_text("# %s\n\nA MaQI course. `course-manager status` lists its waves and labs.\n" % (a.title or a.name), encoding="utf-8")
    title("Course %s" % a.name)
    ok("created in ./%s - next: cd %s && course-manager new <lab>" % (a.name, a.name))


def cmd_new(a):
    root = find_root(); pkg, subs = load(root)
    if not NAME.match(a.name): die("lab name: lowercase letters, digits, _ or -")
    if a.name in subs: die("lab %s already exists" % a.name)
    d = root / a.name
    d.mkdir(exist_ok=True)
    src = d / (a.name + ".py")
    if not src.exists():
        src.write_text(STARTER.format(title=a.title or a.name, kernel=pkg.get("kernel", "python3")), encoding="utf-8")
    waves = tomllib.loads(spec.course_file(root).read_text(encoding="utf-8")).get("wave") or {}
    if a.name in waves:
        die("course.toml already has a wave %s" % a.name)
    with spec.course_file(root).open("a", encoding="utf-8") as f:
        f.write('\n[wave.%s]\ntitle = "%s"\ncontent = ["%s/"]\n'
                'released = []                                    # a draft until a cohort is named\n'
                % (a.name, a.title or a.name, a.name))
    title("Lab %s (wave %s, last in the course)" % (a.name, a.name))
    ok("source: %s/%s.py - edit it, then: course-manager preview %s" % (a.name, a.name, a.name))


def cmd_check(a):
    root = find_root(); pkg, subs = load(root)
    title("Course %s - check" % pkg["name"])
    bad = 0
    allowed = set((os.environ.get("WASABI_BUCKETS") or "").replace(",", " ").split())
    for name, sub in chosen(subs, a.subpackage).items():
        files = sub_files(root, sub)
        errs, nsol, nbs = [], 0, 0
        for f, rel, hidden in files:
            if f.suffix not in MARKED or hidden: continue
            nbs += f.suffix == ".ipynb" or (f.suffix == ".py" and is_notebook(f.read_text(encoding="utf-8")))
            for ch in chunks(f):
                e, n = problems(ch, sub["renderer"], file_leader(f))
                errs += ["%s: %s" % (rel, x) for x in e]; nsol += n
        for e in errs: fail("%s: %s" % (name, e))
        bad += len(errs)
        kept = sorted({str(rel) for f, rel, hidden in files if hidden})
        for f in sub["files"]:
            if not (root / f).exists(): fail("%s: declared file %s is missing" % (name, f)); bad += 1
        if not errs:
            ok("%s: %d file(s), %d notebook(s), %d exercise(s), markers balanced, no solution in the student version"
               % (name, len(files) - len(kept), nbs, nsol))
        if kept:
            print("      kept from students (teacher / .bulkignore): %s" % ", ".join(kept[:8]) + (" ..." if len(kept) > 8 else ""))
        if nsol == 0 and nbs:
            warn("%s: no solution marker - the two versions are identical" % name)
        for b in sub["buckets"]:
            if allowed and b not in allowed:
                warn("%s: bucket %s is not among those your data key opens on this hub (%s)"
                     % (name, b, " ".join(sorted(allowed))))
    sys.exit(1 if bad else 0)


def cmd_render(a):
    root = find_root(); pkg, subs = load(root)
    title("Course %s - render" % pkg["name"])
    for name, sub in chosen(subs, a.subpackage).items():
        out, nsol, kept = do_render(root, pkg, name, sub, notebooks=False)
        ok("%s: %d exercise(s) -> build/student/%s and build/teacher/%s%s" % (
            name, nsol, name, name, (", %d file(s) kept from students" % kept) if kept else ""))


def cmd_build(a):
    """What is delivered, under build/<variant>/<lab>/: notebooks instead of
    their jupytext sources. What the platform's deploy engine runs."""
    root = find_root(); pkg, subs = load(root)
    title("Course %s - build" % pkg["name"])
    for name, sub in chosen(subs, a.subpackage).items():
        out, nsol, kept = do_render(root, pkg, name, sub, notebooks=True)
        ok("%s: %d exercise(s), %d notebook(s), %d file(s) kept from students" % (name, nsol, len(out["student"]), kept))


def cmd_preview(a):
    root = find_root(); pkg, subs = load(root)
    title("Course %s - preview in your account only" % pkg["name"])
    dest = Path.home() / "preview" / pkg["name"]
    user = os.environ.get("JUPYTERHUB_USER") or os.environ.get("USER") or ""
    hub = os.environ.get("COURSE_HUB") or pkg.get("hub", "")
    for name, sub in chosen(subs, a.subpackage).items():
        out, nsol, kept = do_render(root, pkg, name, sub, notebooks=True)
        for v in VARIANTS:
            d = dest / v / name
            if d.exists(): shutil.rmtree(d)
            shutil.copytree(root / "build" / v / name, d)
        ok("%s: %d exercise(s), student and teacher versions" % (name, nsol))
        if kept:
            print("      kept back %d file(s) from students (teacher / .bulkignore)" % kept)
        if sub["buckets"]:
            print("      data      read in place: %s" % ", ".join(sub["buckets"]))
        for v in VARIANTS:
            for nb in out[v] or [root / "build" / v / name]:
                rel = "preview/%s/%s/%s/%s" % (pkg["name"], v, name, nb.relative_to(root / "build" / v / name)) if out[v] else \
                      "preview/%s/%s/%s" % (pkg["name"], v, name)
                tpl = os.environ.get("COURSE_PREVIEW_URL", "")        # e.g. https://{hub}.example.org/user/{user}/lab/tree/{rel}
                url = tpl.format(hub=hub, user=user, rel=rel) if tpl and hub and user else "~/" + rel
                print("      %-9s %s" % (v, url))
    print("\n  Check   student: stops on NotImplementedError · teacher: runs end to end")


def cmd_status(a):
    root = find_root(); pkg, subs = load(root)
    cfg = tomllib.loads(spec.course_file(root).read_text(encoding="utf-8"))
    title("Course %s - %s" % (pkg["name"], pkg.get("title", "")))
    aud = pkg.get("audience") or []
    print("  kernel %s · audience %s\n" % (pkg.get("kernel") or "-", " ".join([aud] if isinstance(aud, str) else aud) or "nobody yet"))
    print("  %-6s %-14s %-24s %-10s %s" % ("WAVE", "LAB", "DEPLOYED TO", "EXERCISES", "DELIVERS"))
    for name, sub in subs.items():
        w = (cfg.get("wave") or {}).get(sub["wave"], {})
        rel = w.get("released")
        rel = "-" if not rel else " ".join(rel) if isinstance(rel, list) else "(invalid: %r)" % (rel,)
        n = 0
        try:
            for f, r, hidden in sub_files(root, sub):
                if f.suffix in MARKED and not hidden:
                    n += sum(problems(ch, sub["renderer"], file_leader(f))[1] for ch in chunks(f))
        except SystemExit:
            n = "(!)"
        print("  %-6s %-14s %-24s %-10s %s" % (sub["wave"] or "-", name, rel, n, ", ".join(sub["content"])))
    if not subs: print("  (none yet: course-manager new <name>)")


def version_line():
    """`course-manager --version`: the version and a fingerprint of THIS copy's
    files. The standard lives as identical copies in segregated projects: two
    copies that print the same line are the same standard; a different
    fingerprint at the same version is a drift to resolve."""
    import hashlib
    from . import __version__
    here = Path(__file__).resolve().parent
    h = hashlib.sha256()
    for f in sorted(list(here.glob("*.py")) + [here.parent.parent / "COURSE.md"]):
        if f.is_file():
            h.update(f.name.encode()); h.update(f.read_bytes())
    return "course-manager %s  fingerprint %s" % (__version__, h.hexdigest()[:12])


def main():
    p = argparse.ArgumentParser(prog="course-manager", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--version", action="version", version=version_line())
    sp = p.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("init"); s.add_argument("name"); s.add_argument("--title", default="")
    s.add_argument("--kernel", default="python3")
    s.set_defaults(f=cmd_init)
    s = sp.add_parser("new"); s.add_argument("name"); s.add_argument("--title", default=""); s.set_defaults(f=cmd_new)
    for name, f in (("check", cmd_check), ("render", cmd_render), ("build", cmd_build), ("preview", cmd_preview)):
        s = sp.add_parser(name); s.add_argument("subpackage", nargs="?", metavar="lab"); s.set_defaults(f=f)
    s = sp.add_parser("status"); s.set_defaults(f=cmd_status)
    a = p.parse_args()
    try:
        a.f(a)
    except CourseError as e:
        for line in str(e).splitlines():
            fail(line)
        sys.exit(1)


if __name__ == "__main__":
    main()
