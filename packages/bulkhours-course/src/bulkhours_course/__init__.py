"""bulkhours-course: the course standard - course.toml, markers, two renders (see COURSE.md)."""
from .spec import CourseError, course_file, find_root, load, labs_of, waves, audience_of, released_to, wave_labs  # noqa: F401

__version__ = "0.3.0"
