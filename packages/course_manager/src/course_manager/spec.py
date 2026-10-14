"""The course file: one loader, for the command line and the deploy engine.

A course lives in one organisation of a git forge; its `solution` repository holds a
`course.toml` (`package.toml`, its earlier name, is still read). The format is
described key by key in COURSE.md; this module is its only reader, so what
`course-manager check` accepts and what the engine deploys cannot drift apart.

Nothing here prints or exits: problems raise CourseError, and the caller
decides what a problem means (a CLI stops, the engine marks the course).
"""
import os
import re
import tomllib
from pathlib import Path

NAME = re.compile(r"^[a-z0-9][a-z0-9_-]{1,39}$")   # labs may be numbered: 00-getting-started
FILES = ("course.toml", "package.toml")          # the first one found wins
RENDERERS = ("markers", "bulkhours")             # the second is the OLDER NAME of the one renderer, kept so files still load
STATUSES = ("active", "past")                    # [course] status; absent = active
DELIVERIES = ("engine", "external")              # [course] delivery; absent = engine


class CourseError(Exception):
    """A course file or a lab that cannot be used as it is."""


def course_file(root):
    """The course file of a folder, or None."""
    for name in FILES:
        if (Path(root) / name).is_file():
            return Path(root) / name
    return None


def find_root(start=None):
    """The folder holding the course file, from `start` upwards."""
    p = Path(start or os.getcwd()).resolve()
    for d in (p, *p.parents):
        if course_file(d):
            return d
    raise CourseError("no course.toml here or above: run this inside a course "
                      "(or `course-manager init <name>`)")


def parse(text):
    """The raw TOML of a course file."""
    try:
        return tomllib.loads(text)
    except tomllib.TOMLDecodeError as e:
        raise CourseError("course.toml: %s" % e)


def status_of(course):
    """[course] status: "active" (the default) or "past" - a course kept as a
    record, from which nothing is deployed any more."""
    s = str(course.get("status") or "active").strip().lower()
    if s not in STATUSES:
        raise CourseError("course.toml: status must be active or past (got %r)" % s)
    return s


def delivery_of(course):
    """[course] delivery: "engine" (the default: the deploy engine writes the
    labs into each person's repository) or "external" - a course delivered by
    its own tool, which the platform shows and never deploys to, nor changes
    the teams of. An external course's file lives with the platform
    (`courses/<org>/course.toml`), not in the organisation."""
    d = str(course.get("delivery") or "engine").strip().lower()
    if d not in DELIVERIES:
        raise CourseError("course.toml: delivery must be engine or external (got %r)" % d)
    return d


LOGIN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,39}$")


def teachers_of(course):
    """[course] teachers: the forge logins of the course's teachers, or
    None when the key is absent (the platform's teachers then)."""
    t = course.get("teachers")
    if t is None:
        return None
    t = [t] if isinstance(t, str) else [str(x) for x in t]
    bad = [x for x in t if not LOGIN.match(x)]
    if bad:
        raise CourseError("course.toml: teachers must be forge logins (got %s)" % ", ".join(map(repr, bad)))
    return list(dict.fromkeys(t))


def course_table(cfg):
    """[course], or [package] in a file written before 2026-10-14."""
    return cfg.get("course") or cfg.get("package") or {}


def _list(v):
    return [v] if isinstance(v, str) else list(v or [])


def labs_of(cfg, renderer_env=None):
    """{lab: spec}. A LAB is what one deployment writes into a person's
    repository, at the paths it has in `solution`. Declared by the waves:

        [wave.microintro]
        content = ["microintro/"]        # default: <lab>/
        exclude = ["runs/"]              # delivered to nobody

    Several labs in one wave: [wave.<name>.lab.<x>], one table each. The older
    [subpackage.<name>] sections are read into the same shape."""
    course = course_table(cfg)
    teacher = _list(course.get("teacher"))
    renderer_env = os.environ.get("COURSE_RENDERER") if renderer_env is None else renderer_env
    labs = {}

    def add(name, spec, title, wave):
        if not NAME.match(name):
            raise CourseError("course.toml: lab name %r is not valid (lowercase letters, digits, _ or -)" % name)
        if name in labs:
            raise CourseError("course.toml: lab %s is declared twice" % name)
        labs[name] = {"name": name, "title": spec.get("title") or title or name, "wave": wave,
                      "content": _list(spec.get("content")) or [name + "/"],
                      "exclude": _list(spec.get("exclude")), "teacher": teacher,
                      "buckets": _list(spec.get("buckets")), "files": _list(spec.get("files")),
                      "data": _list(spec.get("data")),
                      "renderer": renderer_env or spec.get("renderer") or course.get("renderer") or "markers"}
        if labs[name]["renderer"] not in RENDERERS:
            raise CourseError("course.toml: lab %s: renderer must be markers (or its older name)" % name)

    for name, s in (cfg.get("subpackage") or {}).items():
        nb = Path(s.get("notebook") or "%s/%s.py" % (name, name))
        add(name, dict(s, content=[str(nb) if nb.parent == Path(".") else str(nb.parent) + "/"]), s.get("title"), "")
    for wave, w in (cfg.get("wave") or {}).items():
        if not isinstance(w, dict):
            continue
        lab = w.get("lab")
        if isinstance(lab, dict):
            for name, spec in lab.items():
                add(name, spec if isinstance(spec, dict) else {}, w.get("title"), wave)
        else:
            add(wave_id(wave, w), w, w.get("title"), wave)
    return labs


def wave_id(wave, w):
    """The short name of what a wave delivers: the wave's own name -
    [wave.microintro] delivers `microintro` (`id` or `lab`, in files written
    before 2026-10-14, still override it). What is delivered is decided by
    `content` alone; the name labels the delivery - on the Courses page, in
    the README program, and in the `deploy <name>` commit by which the engine
    finds what a person already has. Never rename a wave already delivered:
    it would be a new delivery for everyone who has it."""
    for key in ("id", "lab"):
        if isinstance(w.get(key), str) and w[key]:
            return w[key]
    return wave


def load(root):
    """(course, labs) of the course in `root`: what the command line works on."""
    f = course_file(root)
    if not f:
        raise CourseError("no course.toml in %s" % root)
    cfg = parse(f.read_text(encoding="utf-8"))
    course = course_table(cfg)
    if not NAME.match(course.get("name", "")):
        raise CourseError("course.toml: [course] name must be lowercase letters, digits, _ or -")
    status_of(course)
    delivery_of(course)
    teachers_of(course)
    return course, labs_of(cfg)


# ── Who a wave goes to, and when ───────────────────────────────────────────
def audience_of(course):
    """[course] audience as wave recipients: "m2.students", "@m2.students",
    or a list of either -> ["@m2.students", ...]; empty -> []."""
    a = course.get("audience") or []
    a = a.split() if isinstance(a, str) else [str(x) for x in a]
    return [x if x.startswith("@") or x == "all" else "@" + x for x in a if x]


def wave_labs(w, wave=""):
    """The deliveries of a wave: [wave.<w>.lab.<x>] tables, `labs = [...]`, or
    its one `id` (see wave_id)."""
    labs = _list(w.get("labs"))
    lab = w.get("lab")
    if isinstance(lab, dict):
        labs += list(lab)
    elif not labs:
        labs.append(wave_id(wave, w))
    return [l for i, l in enumerate(labs) if l not in labs[:i]]


def released_to(r, who):
    """`released` -> (the cohorts the wave has been deployed to, problems).

    A RECORD, written by the deploy engine after each deployment (a commit
    "<wave> deployed to <cohorts>"), not a gate: any cohort of `who` can
    receive the wave. One syntax, a list of cohorts of `who`:

        released = []                                   not deployed yet (also: absent)
        released = ["@m2.students"]                     M2 has it, M1 not yet

    true/false and a bare string are refused. "m2.students" and
    "@m2.students" name the same cohort."""
    if r is None:
        return [], []
    if not isinstance(r, list):
        return [], ["released must be a list of cohorts, e.g. released = [\"@m2.students\"] (got %r)" % (r,)]
    out, bad = [], []
    for x in (str(x) for x in r):
        c = x if x in who else "@" + x if "@" + x in who else None
        if c is None:
            bad.append("released to %s, which is not in who" % x)
        elif c not in out:
            out.append(c)
    return out, bad


def waves(cfg, labs=None):
    """{wave: {title, labs, who, at, released, order[, error]}} - what the
    engine deploys, in the order of the file (`order`: its position, for
    readers that do not keep key order). `at` (optional) has the wave deployed on its own at that time."""
    course = course_table(cfg)
    labs = labs_of(cfg) if labs is None else labs
    out = {}
    for name, w in (cfg.get("wave") or {}).items():
        if not isinstance(w, dict):
            continue
        ls = wave_labs(w, name)
        who = w.get("who") or audience_of(course) or "all"
        who = who.split() if isinstance(who, str) else [str(x) for x in who]
        at = w.get("at") or ""
        if hasattr(at, "isoformat"):
            at = at.isoformat()
        released, problems = released_to(w.get("released"), who)
        out[name] = {"title": w.get("title") or name, "labs": ls, "who": who, "at": str(at),
                     "released": released, "order": len(out),
                     # The README's {{program}}: shown to a person once the wave reached them.
                     "summary": " ".join(str(w.get("summary") or "").split())}
        bad = [l for l in ls if l not in labs]
        if not ls:
            problems.append("no labs")
        elif bad:
            problems.append("unknown lab(s): " + ", ".join(bad))
        if problems:
            out[name]["error"] = "; ".join(problems)
    return out
