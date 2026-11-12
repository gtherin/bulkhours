import { test } from "node:test";
import assert from "node:assert/strict";
import { isMarimo, marimoCandidates, RENDER_CSP, showable } from "../src/core/render.ts";

test("only a marimo notebook is rendered", () => {
  assert.equal(isMarimo('"""doc"""\nimport marimo\n\napp = marimo.App(width="medium")\n'), true);
  assert.equal(isMarimo("import pandas as pd\nprint(1)\n"), false);
  assert.equal(isMarimo("# import marimo is not an import\nx = 1\n"), false);
});

test("marimo is looked for where it can import the notebook's code, the PATH last", () => {
  assert.deepEqual(marimoCandidates("/opt/miniconda3/bin/marimo", "/opt/venvs/viterbi-26/bin/python"),
    ["/opt/miniconda3/bin/marimo", "/opt/venvs/viterbi-26/bin/marimo", "marimo"]);
  assert.deepEqual(marimoCandidates("", "python"), ["marimo"]);
  assert.deepEqual(marimoCandidates(undefined, undefined), ["marimo"]);
});

test("the page may load marimo's code from jsdelivr, and send nothing anywhere", () => {
  const out = showable("<html><head><title>x</title></head><body></body></html>");
  assert.match(out, /^<html><head><meta http-equiv="Content-Security-Policy"/);
  assert.match(RENDER_CSP, /connect-src 'none'/);
  assert.match(RENDER_CSP, /script-src https:\/\/cdn\.jsdelivr\.net /);
  assert.match(showable("<p>no head</p>"), /^<meta http-equiv/);
});

// A session's pages (owner, 2026-11-12: "a rendering directory for each
// session; if there are html files in there, clickable links to display them").
test("a session page is shown with its own files, scripts from known CDNs, and nothing sent anywhere", async () => {
  const { pageHtml } = await import("../src/core/render.ts");
  const out = pageHtml("<html><head><title>x</title></head><body><img src='plot.png'></body></html>", "vscode-res://renders/", "vscode-res:");
  assert.match(out, /<head><meta http-equiv="Content-Security-Policy" content="default-src 'none';/);
  assert.match(out, /<base href="vscode-res:\/\/renders\/">/);
  assert.match(out, /connect-src 'none'/);
  assert.match(out, /img-src vscode-res: data: blob:;/);
  assert.doesNotMatch(out, /img-src[^;]*https:/, "no picture from anywhere: a picture address can carry data out");
  assert.match(pageHtml("<p>bare</p>", "b/", "c:"), /^<meta http-equiv/);
});
