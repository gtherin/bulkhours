"""course_manager: the course standard - course.toml, markers, two renders (COURSE.md).

A SHARED STANDARD BETWEEN SEGREGATED PROJECTS. Each project that adopts it holds
its own, identical copy of this folder and depends on no other project. A change
is made in every copy or in none; `course-manager --version` prints the version
and a fingerprint so two copies can be compared at a glance. Nothing in here
names a project, a host, a forge or a machine.
"""
from .spec import CourseError, course_file, find_root, load, labs_of, waves, audience_of, released_to, wave_labs  # noqa: F401

__version__ = "0.3.0"
