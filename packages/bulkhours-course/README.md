# bulkhours-course

The course standard, and the one tool that reads it. The format - `course.toml`,
the markers, the two renders, the waves and their record, the rules a deployer
honours - is in [COURSE.md](COURSE.md).

```
bulkhours-course init <course>     the standard skeleton, with course.toml
bulkhours-course new <lab>         a lab and a draft wave
bulkhours-course check [lab]       markers balanced, no answer reaching the student version
bulkhours-course preview [lab]     both versions under ~/preview/<course>/
bulkhours-course status            every wave, its lab, who it is released to
bulkhours-course build [lab]       what is delivered, under build/ (a deploy engine runs this)
```

No dependency: a teacher installs it alone (`pip install ./packages/bulkhours-course`),
a platform's deploy engine imports `bulkhours_course.spec` for its loader. The
`bulkhours` notebook package depends on it for its own markers; this package
depends on nothing of `bulkhours`, so importing it loads no notebook runtime.

Born as `maqi-course` in MScT-AI-MaQI/maqi-instance (`packages/maqi-course`,
up to commit 31dd5aa, 2026-10-14); moved here so both platforms read one source.

Tests: `python3 -m unittest discover -s tests` (no dependency).
