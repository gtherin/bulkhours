import { test } from "node:test";
import assert from "node:assert/strict";
import { parseFileRef, referenceText } from "../src/core/fileLinks.ts";

test("a path the agent writes as code is a link, with its lines", () => {
  assert.deepEqual(parseFileRef("topic_hormuz.py:42"), { path: "topic_hormuz.py", line: 42 });
  assert.deepEqual(parseFileRef("src/maqi_research/a.py:10-20"), { path: "src/maqi_research/a.py", line: 10, endLine: 20 });
  assert.deepEqual(parseFileRef("/home/users/g/dashboards/hormuz/app.py"), { path: "/home/users/g/dashboards/hormuz/app.py" });
  assert.deepEqual(parseFileRef("notebooks/CNN_Iran_War_scrapping.ipynb"), { path: "notebooks/CNN_Iran_War_scrapping.ipynb" });
});

test("code that is not a path stays code", () => {
  for (const s of ["np.mean(x)", "x = 1", "pandas", "../etc/passwd", "a/../b.py", "https://x.fr/a.py", "fit()"]) {
    assert.equal(parseFileRef(s), undefined, s);
  }
});

test("a selection arrives in the chat as its file, its lines and its code", () => {
  assert.equal(referenceText("app.py"), "`app.py` ");
  assert.equal(referenceText("app.py", { start: 3, end: 5, text: "a = 1\nb = 2\n", language: "python" }),
    "`app.py:3-5`\n```python\na = 1\nb = 2\n```\n");
  assert.equal(referenceText("a.md", { start: 7, end: 7, text: "```x```", language: "markdown" }),
    "`a.md:7`\n````markdown\n```x```\n````\n");
});
