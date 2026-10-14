"""One source, two versions: the markers, notebooks, and the leak check.

A lab is written once; `build` writes its student version (answers removed,
prompts shown, outputs cleared, teacher files left out) and its teacher
version (everything) under build/<variant>/<lab>/, at the paths the files
have in `solution`. The leak check refuses any line only a teacher may see
that reaches the student version - checked on every rendered file and on
every notebook actually written.

Problems raise CourseError; nothing here prints.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

from .spec import CourseError

# ── The markers: Otter Grader's, plus a few of the same style ─────────────
# Otter Assign's format (otter-grader.readthedocs.io, "Notebook Format") is the
# closest thing to a standard: `# BEGIN SOLUTION` / `# END SOLUTION` is also
# nbgrader's. A lab written for Otter renders here unchanged. COURSE.md has
# the full table; what Otter does not cover is marked "extension" there.
BEGIN_SOL = re.compile(r"^\s*#\s*BEGIN SOLUTION(?P<np>\s+NO PROMPT)?\s*$")
END_SOL = re.compile(r"^\s*#\s*END SOLUTION\s*$")
BEGIN_PRO = re.compile(r"""^\s*(?P<q>(?:\"\"\"|''')\s*)?#\s*BEGIN PROMPT\s*$""")
END_PRO = re.compile(r"""^\s*(?:(?:\"\"\"|''');?\s*)?#\s*END PROMPT\s*$""")
# One line. Otter: `# SOLUTION`, `# SOLUTION NO PROMPT`, `# SEED`.
# Extensions: `# SOLUTION: <value>`, `# SOLUTION REPLACE: <line>`, `# PROMPT: <line>`.
LINE = re.compile(r"^(?P<code>.*?)#\s*(?P<op>SOLUTION NO PROMPT|SOLUTION REPLACE|SOLUTION|SEED|PROMPT)\b(?:\s*:(?P<arg>.*))?\s*$")
IGNORE = re.compile(r"^\s*#\s*ignore\s*$", re.I)                # first line of a cell: in neither version
ASSIGN = re.compile(r"""^(?P<lhs>\s*[A-Za-z_][\w.\[\]'", ]*?)\s*=(?!=)\s*\S""")
# bulkhours' own names, for labs written for it.
BK = re.compile(r"^(?P<code>.*?)#\s*(?:BULKHOURS|BKRESET)\.(?P<op>INIT|REMOVE|REPLACE|PRINT):?(?P<arg>.*)$")
CELL = re.compile(r"^#\s*%%")
# What looks like a marker (upper case), not quoted in `backticks` as prose does.
MARKERISH = re.compile(r"(?:^|[^`])#\s*(?:(?:BEGIN|END)\s+(?:SOL|PRO)|SOLUTION|PROMPT|SEED)")
TODO = "# ..."
ELLIPSIS = "..."
VARIANTS = ("student", "teacher")
JUPYTEXT = os.environ.get("COURSE_JUPYTEXT") or shutil.which("jupytext") or "jupytext"


def line_marker(l):
    """(code, op, arg) of a line carrying a one-line marker, or None.
    SOLUTION and SEED need code before them (a lone `# SOLUTION` is a
    comment); PROMPT stands alone and needs its `:`."""
    m = LINE.match(l.rstrip("\n"))
    if not m:
        return None
    code, op, arg = m.group("code"), m.group("op"), (m.group("arg") or "").strip()
    if op == "PROMPT":
        return (code, op, arg) if not code.strip() and m.group("arg") is not None else None
    if not code.strip():
        return None
    if op == "SOLUTION REPLACE" and m.group("arg") is None:
        return None
    return code, op, arg


def solution_line(code, op, arg, variant, nl):
    """A one-line marker for `variant` -> the line, or None to drop it."""
    indent = code[:len(code) - len(code.lstrip())]
    if variant == "teacher":
        return None if op == "PROMPT" else code.rstrip() + nl
    if op in ("SOLUTION NO PROMPT", "SEED"):
        return None
    if op in ("PROMPT", "SOLUTION REPLACE"):
        return indent + arg + nl
    value = arg or ELLIPSIS                  # `# SOLUTION` -> ..., `# SOLUTION: 0` -> 0
    stripped = code.strip()
    if stripped == "return" or stripped.startswith("return "):
        return indent + "return " + value + nl
    a = ASSIGN.match(code)
    if a:
        return a.group("lhs").rstrip() + " = " + value + nl
    return indent + value + nl


def bulkhours_line(l, variant, state):
    """One line carrying a BULKHOURS./BKRESET. marker -> the line for `variant`,
    or None to drop it. `state["removing"]` is the open REMOVE block."""
    body, nl = (l[:-1], "\n") if l.endswith("\n") else (l, "")
    m = BK.match(body)
    code, op, arg = m.group("code"), m.group("op"), m.group("arg").strip()   # "# BULKHOURS.REPLACE: x" -> "x"
    indent = code[:len(code) - len(code.lstrip())]
    if op == "REMOVE" and arg in ("START", "END"):
        if arg == "START":
            if state["removing"]: raise ValueError("REMOVE:START inside an open REMOVE block")
            state["removing"] = True
            return None
        if not state["removing"]: raise ValueError("REMOVE:END without a START")
        state["removing"] = False
        return (indent + TODO + nl) if variant == "student" else None
    if variant == "teacher":
        # PRINT exists for the student only; the others lose their marker.
        return None if op == "PRINT" else (code.rstrip() + nl)
    if op == "PRINT":
        return indent + arg + nl
    if op == "REMOVE":                                   # REMOVE:LINE
        return indent + TODO + nl
    if op == "REPLACE":
        return indent + arg + "  " + TODO + nl
    # INIT: keep the left-hand side (or `return`), put the initial value.
    stripped = code.strip()
    if stripped.startswith("return ") or stripped == "return":
        return indent + "return " + arg + "  " + TODO + nl
    if "=" in code:
        return code.split("=")[0].rstrip() + " = " + arg + "  " + TODO + nl
    return indent + arg + "  " + TODO + nl


def ignored_cell(lines):
    """A cell whose first line is `# IGNORE` (Otter): in neither version."""
    first = next((l for l in lines if l.strip()), "")
    return bool(IGNORE.match(first))


def render(lines, variant):
    """One source -> the student or the teacher version.

    Blocks: `# BEGIN SOLUTION` ... `# END SOLUTION` is the teacher's; the
    student gets the PROMPT block next to it if there is one, else `...` at
    the block's indentation. `# BEGIN SOLUTION NO PROMPT` leaves nothing. A
    PROMPT block is the student's: written as comments (uncommented for the
    student) or, as in Otter, inside a `\"\"\" # BEGIN PROMPT` string (shown
    as written). One-line markers: `solution_line` and `bulkhours_line`. In a
    jupytext file, a cell whose first line is `# IGNORE` goes nowhere."""
    out, in_sol, in_pro, pro_raw = [], None, False, False
    pending = None            # the `...` of a solution block, until we know no prompt follows
    after_prompt = False      # a prompt block was just written: the next solution needs no `...`
    bk = {"removing": False}
    skipping = False          # inside an IGNORE cell of a jupytext file

    def flush():
        nonlocal pending
        if pending is not None and variant == "student":
            out.append(pending)
        pending = None

    for n, l in enumerate(lines, 1):
        nl = "\n" if l.endswith("\n") else ""
        if CELL.match(l) and in_sol is None and not in_pro:
            nxt = [x for x in lines[n:n + 5] if x.strip()]
            skipping = bool(nxt) and bool(IGNORE.match(nxt[0]))
            if skipping:
                continue
        elif skipping:
            continue
        mm = BK.match(l.rstrip("\n"))
        if bk["removing"] or mm:
            if mm and in_pro: raise ValueError("line %d: a line marker inside a PROMPT block" % n)
            if bk["removing"] and not (mm and mm.group("op") == "REMOVE" and mm.group("arg").strip() == "END"):
                # Inside a REMOVE block everything is solution: never for the
                # student, whatever marker the line carries.
                if variant == "teacher" and not (mm and mm.group("op") == "PRINT"):
                    out.append((mm.group("code").rstrip() + nl) if mm else l)
                continue
            flush()
            try:
                r = bulkhours_line(l, variant, bk)
            except ValueError as e:
                raise ValueError("line %d: %s" % (n, e))
            if r is not None and not (in_sol is not None and variant == "student"):
                out.append(r)
            continue
        m = BEGIN_SOL.match(l)
        if m:
            if in_sol is not None or in_pro: raise ValueError("line %d: BEGIN SOLUTION inside an open block" % n)
            flush()
            in_sol = "np" if m.group("np") else l[:len(l) - len(l.lstrip())]
            continue
        if END_SOL.match(l):
            if in_sol is None: raise ValueError("line %d: END SOLUTION without a beginning" % n)
            if in_sol != "np" and not after_prompt:
                pending = in_sol + ELLIPSIS + "\n"
            in_sol, after_prompt = None, False
            continue
        m = BEGIN_PRO.match(l)
        if m:
            if in_sol is not None or in_pro: raise ValueError("line %d: BEGIN PROMPT inside an open block" % n)
            pending = None                   # the prompt takes the solution's place
            in_pro, pro_raw = True, bool(m.group("q"))
            continue
        if END_PRO.match(l):
            if not in_pro: raise ValueError("line %d: END PROMPT without a beginning" % n)
            in_pro, after_prompt = False, True
            continue
        if in_sol is not None:
            if variant == "teacher":
                lm = line_marker(l)
                if not lm:
                    out.append(l)
                elif lm[1] != "PROMPT":
                    out.append(lm[0].rstrip() + nl)
            continue
        if in_pro:
            if variant == "student":
                if pro_raw:
                    out.append(l)
                else:
                    body = l[:-1] if nl else l
                    mc = re.match(r"^(\s*)#\s?(.*)$", body)
                    out.append((mc.group(1) + mc.group(2) + nl) if mc else l)
            continue
        if l.strip():
            flush()
            after_prompt = False
        lm = line_marker(l)
        if lm:
            r = solution_line(lm[0], lm[1], lm[2], variant, nl)
            if r is not None:
                out.append(r)
            continue
        out.append(l)
    flush()
    if in_sol is not None or in_pro or bk["removing"]:
        raise ValueError("a block is still open at the end of the file")
    return out


def render_with(renderer, lines, variant):
    """ONE renderer. `renderer = "bulkhours"` in a course.toml is accepted and
    means the same thing as `markers`: the BULKHOURS./BKRESET. names are an
    input dialect of this renderer (bulkhours_line), not a second engine.
    Until 2026-10-14 it loaded cell_reset/cell_solution from a clone of
    gtherin/bulkhours - two renderers for one notion, coupled the wrong way
    round; bulkhours now depends on this package instead."""
    if renderer not in ("markers", "bulkhours"):
        raise ValueError("unknown renderer %r (markers or bulkhours)" % renderer)
    return render(lines, variant)


def secret_lines(lines):
    """Every substantial line of a source that only the teacher may see: inside
    a SOLUTION or REMOVE block, or the teacher's side of a one-line marker.
    None of them may reach a student, whatever rendered it."""
    secret, inside = set(), False
    for l in lines:
        if BEGIN_SOL.match(l): inside = True; continue
        if END_SOL.match(l): inside = False; continue
        m = BK.match(l.rstrip("\n"))
        if m:
            if m.group("op") == "REMOVE" and m.group("arg").strip() in ("START", "END"):
                inside = m.group("arg").strip() == "START"; continue
            s = m.group("code").strip()              # the teacher's line on INIT / REPLACE / REMOVE:LINE
            if m.group("op") != "PRINT" and len(s) >= 16: secret.add(s)
            continue
        lm = line_marker(l)
        if lm:
            s = lm[0].strip()                        # the teacher's line of SOLUTION / SEED / REPLACE
            if lm[1] != "PROMPT" and len(s) >= 16: secret.add(s)
            continue
        s = l.strip()
        if inside and len(s) >= 16 and not s.startswith("#"):
            secret.add(s)
    return secret


def leaks(student_lines, secret):
    return sorted({l.strip() for l in student_lines if l.strip() in secret})


def problems(lines, renderer="markers"):
    """What must stop a render. Returns (errors, n_exercises)."""
    errs = []
    try:
        student = render_with(renderer, lines, "student")
    except ValueError as e:
        return [str(e)], 0
    # Exercises: a SOLUTION block, a one-line SOLUTION (not SEED, not PROMPT),
    # and each bulkhours INIT / REPLACE / REMOVE:LINE / REMOVE block.
    n = sum(1 for l in lines if BEGIN_SOL.match(l))
    for l in lines:
        m = BK.match(l.rstrip("\n"))
        if m:
            if m.group("op") != "PRINT" and m.group("arg").strip() != "END":
                n += 1
            continue
        lm = line_marker(l)
        if lm and lm[1].startswith("SOLUTION"):
            n += 1
    # A marker misspelt is a solution delivered: anything that looks like one
    # and is not one stops the build.
    for k, l in enumerate(lines, 1):
        if MARKERISH.search(l) and not (BEGIN_SOL.match(l) or END_SOL.match(l) or BEGIN_PRO.match(l)
                                         or END_PRO.match(l) or BK.match(l.rstrip("\n")) or line_marker(l)):
            errs.append("line %d: not a marker this tool knows: %s" % (k, l.strip()[:70]))
    # THE LEAK THAT CAN REALLY HAPPEN: the answer typed into the PROMPT, or
    # copied outside the markers, or a marker the renderer does not know.
    # Comparing the two renders with each other cannot find it (a line only in
    # the teacher's is, by construction, not in the student's): the reference
    # is the SOURCE's solution lines.
    leaked = leaks(student, secret_lines(lines))
    for s in leaked[:3]:
        errs.append("solution line also reaches the student: %s" % s[:70])
    return errs, n


def stable_ids(ipynb, key):
    """jupytext draws random cell ids at every conversion: an unchanged
    subpackage would differ at every render, and students who touched the
    notebook would get merge conflicts on `id` lines (seen 2026-09-28 on the
    course). Ids derive from (package, subpackage, variant, position): an
    unchanged source gives a byte-identical notebook."""
    nb = json.loads(ipynb.read_text(encoding="utf-8"))
    for i, cell in enumerate(nb.get("cells", [])):
        cell["id"] = hashlib.sha1(("%s/%d" % (key, i)).encode()).hexdigest()[:12]
    ipynb.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


JUNK = {".git", "build", ".ipynb_checkpoints", "__pycache__", ".bulkignore", ".gitignore"}


def bulkignore_rules(root, subdir):
    """The rules of `.bulkignore`: what is NOT installed for students.

    Same spirit and syntax as .gitignore, one pattern per line:
        solutions/          a directory, wherever it is
        *.teacher.md        a file name pattern
        /microintro/raw     a path from the folder holding this .bulkignore
        !keep-this.md       un-ignore (the last matching rule wins)
    Read from the package root and from the subpackage folder; each file's
    patterns are relative to its own folder. The teacher version ignores it:
    a teacher receives everything.
    """
    rules = []
    for base in dict.fromkeys((root, subdir)):
        f = base / ".bulkignore"
        if not f.is_file():
            continue
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            neg = line.startswith("!")
            pat = line[1:] if neg else line
            pat = pat.rstrip("/")
            anchored = "/" in pat
            rules.append((neg, pat.lstrip("/"), anchored, base))
    return rules


def ignored(path, rules):
    """Is this file kept from students? `path` is absolute."""
    from fnmatch import fnmatch
    verdict = False
    for neg, pat, anchored, base in rules:
        try:
            parts = path.relative_to(base).parts
        except ValueError:
            continue
        if anchored:        # against the path, and each folder above the file
            hit = any(fnmatch("/".join(parts[:k]), pat) for k in range(1, len(parts) + 1))
        else:               # against any single name on the way
            hit = any(fnmatch(part, pat) for part in parts)
        if hit:
            verdict = not neg
    return verdict


def pattern_hit(rel, pat):
    """A .gitignore-style pattern against a path relative to the lab:
    "runs/" or "*.teacher.*" match any name on the way; "data/raw" (a slash
    inside) matches from the lab's top."""
    from fnmatch import fnmatch
    pat = pat.strip().rstrip("/")
    parts = Path(rel).parts
    if "/" in pat:
        pat = pat.lstrip("/")
        return any(fnmatch("/".join(parts[:k]), pat) for k in range(1, len(parts) + 1))
    return any(fnmatch(x, pat) for x in parts)


def sub_files(root, sub):
    """[(file, path in the repository, kept from students)] for one lab.

    THE SAME STRUCTURE AS `solution`: a file is delivered at its own path -
    README.md at the root stays README.md, microintro/microintro.ipynb stays
    there. `content` decides what goes in (a folder: what it holds; a file:
    itself). `exclude` drops build output for everyone; `teacher` patterns
    and .bulkignore drop teacher material for students only. Patterns are
    matched from the content folder and from the repository root."""
    base_root = root.resolve()
    out, seen = [], {}
    for c in sub["content"]:
        p = (root / c).resolve()
        if p != base_root and base_root not in p.parents:
            raise CourseError("%s: content %s is outside the package" % (sub["name"], c))
        if p.is_dir():
            pairs = [(f, f.relative_to(p)) for f in sorted(p.rglob("*"))
                     if f.is_file() and not (set(f.relative_to(p).parts) & JUNK)]
            base = p
        elif p.is_file():
            pairs, base = [(p, Path(p.name))], p.parent
        else:
            raise CourseError("%s: content %s does not exist" % (sub["name"], c))
        pairs = [(f, inner, f.relative_to(base_root)) for f, inner in pairs]
        rules = bulkignore_rules(root, base)
        for f, inner, rel in pairs:
            hit = lambda pats: any(pattern_hit(inner, x) or pattern_hit(rel, x) for x in pats)
            if hit(sub["exclude"]):
                continue
            if str(rel) in seen:
                raise CourseError("%s: %s is delivered twice (from %s and %s)" % (sub["name"], rel, seen[str(rel)], c))
            seen[str(rel)] = c
            out.append((f, rel, hit(sub["teacher"]) or ignored(f, rules)))
    return out


def is_notebook(text):
    """A jupytext source: the YAML header, or py:percent cells."""
    return text.startswith("# ---") or re.search(r"^# %%", text, re.M) is not None


MARKED = (".py", ".ipynb")       # the files that go through the markers


def chunks(f):
    """The marked text of a source, as lists of lines: one for a .py, one per
    cell for an .ipynb (markers never span cells)."""
    if f.suffix == ".py":
        return [f.read_text(encoding="utf-8").splitlines(keepends=True)]
    nb = json.loads(f.read_text(encoding="utf-8"))
    return ["".join(c.get("source", "")).splitlines(keepends=True) for c in nb.get("cells", [])]


def render_ipynb(f, renderer, variant):
    """An authored notebook, rendered cell by cell. The student version loses
    every output and execution count: a saved output can print the answer.
    The teacher version keeps them."""
    nb = json.loads(f.read_text(encoding="utf-8"))
    nb["cells"] = [c for c in nb.get("cells", [])
                   if not ignored_cell("".join(c.get("source", "")).splitlines(keepends=True))]
    for c in nb.get("cells", []):
        lines = "".join(c.get("source", "")).splitlines(keepends=True)
        c["source"] = render_with(renderer, lines, variant)
        if variant == "student" and c.get("cell_type") == "code":
            c["outputs"], c["execution_count"] = [], None
            c.get("metadata", {}).pop("execution", None)
    return nb


def do_render(root, course, name, sub, notebooks):
    """build/<variant>/<lab>/ for both variants -> (notebooks {variant: [paths]},
    exercises, files kept from students). With `notebooks`, every jupytext
    source becomes its .ipynb and the .py is not delivered."""
    files = sub_files(root, sub)
    if not files:
        raise CourseError("%s: nothing to deliver (content %s)" % (name, ", ".join(sub["content"])))
    # Every .py goes through the markers, not only notebooks: a helper module
    # can hide its solutions the same way.
    texts, nsol, bad = {}, 0, []
    for f, rel, hidden in files:
        if f.suffix not in MARKED:
            continue
        texts[f] = chunks(f)
        if hidden:
            continue                       # never delivered to students: nothing to check
        for ch in texts[f]:
            errs, n = problems(ch, sub["renderer"])
            nsol += n
            bad += ["%s: %s: %s" % (name, rel, e) for e in errs]
    if bad:
        raise CourseError("\n".join(bad))
    secret = set()
    for f, t in texts.items():
        for ch in t:
            secret |= secret_lines(ch)
    out, kept_back = {v: [] for v in VARIANTS}, 0
    for v in VARIANTS:
        d = root / "build" / v / name
        if d.exists(): shutil.rmtree(d)     # a file removed from the source must leave the build
        d.mkdir(parents=True)
        for f, rel, hidden in files:
            if v == "student" and hidden:
                kept_back += 1
                continue
            target = d / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            if f.suffix == ".ipynb":
                nb = render_ipynb(f, sub["renderer"], v)
                if v == "student":
                    src_lines = [l for c in nb.get("cells", []) for l in "".join(c.get("source", "")).split("\n")]
                    if leaks(src_lines, secret):
                        raise CourseError("%s: %s: solution line in the student notebook: %s"
                            % (name, rel, leaks(src_lines, secret)[0][:70]))
                target.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
                out[v].append(target)
            elif f in texts:
                rendered = render_with(sub["renderer"], texts[f][0], v)
                if v == "student" and leaks(rendered, secret):
                    raise CourseError("%s: %s: solution line in the student version: %s"
                        % (name, rel, leaks(rendered, secret)[0][:70]))
                target.write_text("".join(rendered), encoding="utf-8")
                if notebooks and is_notebook("".join(texts[f][0])):
                    nb = target.with_suffix(".ipynb")
                    r = subprocess.run([JUPYTEXT, "--quiet", "--to", "ipynb", "--output", str(nb), str(target)],
                                       capture_output=True, text=True)
                    if r.returncode != 0:
                        raise CourseError("%s: %s: jupytext failed: %s" % (name, rel, (r.stderr or r.stdout).strip()[-300:]))
                    # The same key as before for <lab>/<lab>.py, so notebooks
                    # already deployed keep their cell ids.
                    key = "%s/%s/%s" % (course["name"], name, v) if str(rel) == "%s/%s.py" % (name, name) else \
                          "%s/%s/%s/%s" % (course["name"], name, rel, v)
                    stable_ids(nb, key)
                    if v == "student":
                        # Once more on what is actually delivered: the notebook.
                        cells = json.loads(nb.read_text(encoding="utf-8")).get("cells", [])
                        src_lines = [l for c in cells for l in "".join(c.get("source", "")).split("\n")]
                        if leaks(src_lines, secret):
                            raise CourseError("%s: %s: solution line in the student notebook: %s"
                                % (name, rel, leaks(src_lines, secret)[0][:70]))
                    target.unlink()            # a recipient opens the notebook: one file, one view
                    out[v].append(nb)
            else:
                shutil.copy2(f, target)
        for extra in sub["files"]:
            fsrc = root / extra
            if not fsrc.exists(): raise CourseError("%s: declared file %s does not exist" % (name, extra))
            for one in ([fsrc] if fsrc.is_file() else [x for x in sorted(fsrc.rglob("*")) if x.is_file()]):
                target = d / one.relative_to(fsrc.parent)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(one, target)
    return out, nsol, kept_back


# ── Commands ───────────────────────────────────────────────────────────────


# ── Per person: the placeholders a deployment fills ────────────────────────
PLACEHOLDER = re.compile(r"\{\{\s*(login|course|program)\s*\}\}")
TEXT_SUFFIXES = {".md", ".txt", ".py", ".ipynb", ".toml", ".cfg", ".ini", ".json",
                 ".yml", ".yaml", ".sh", ".r", ".R", ".tex", ".html", ".csv"}


def personalise(content, rel, values):
    """`content` (bytes) of the delivered file `rel`, with {{login}},
    {{course}} and {{program}} replaced by `values` - for one person, at
    deployment.

    Only text files, and only these names: anything else between braces
    stays as written. `solution` and the teacher version keep the
    placeholders, so a teacher sees where a student's own value goes."""
    if Path(rel).suffix not in TEXT_SUFFIXES or b"{{" not in content:
        return content
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        return content
    return PLACEHOLDER.sub(lambda m: str(values.get(m.group(1), m.group(0))), text).encode("utf-8")



def program(waves, received):
    """The README's {{program}}: a Markdown table of the course's waves that
    have a `summary`, in order. A wave the person has received shows its
    summary; one still to come shows its title only - the program without
    spoiling it. `received` is the set of labs they have."""
    rows = []
    for name in sorted(waves, key=lambda n: waves[n].get("order", 0)):   # the order of course.toml
        w = waves[name]
        if not w.get("summary"):
            continue
        labs = w.get("labs") or []
        got = bool(labs) and all(l in received for l in labs)
        title = (w.get("title") or name).rstrip(".")
        rows.append("| %d | **%s** | *%s.* %s |" % (
            len(rows) + 1, ", ".join(labs) or name, title,
            w["summary"] if got else "Not released yet."))
    if not rows:
        return ""
    return "\n".join(["| | Lab | What it is |", "|---|---|---|"] + rows)
