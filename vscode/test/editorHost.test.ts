// File access through the editor, against a stand-in `vscode`.
import { mock, test } from "node:test";
import assert from "node:assert/strict";

const edits: { path: string; text: string }[] = [];
const saved: string[] = [];
const disk = new Map<string, string>();
let accept = true;
let open: { uri: { fsPath: string }; lineCount: number; save(): Promise<boolean> }[] = [];
const ranges: number[][] = [];
class WorkspaceEdit { ops: { path: string; text: string }[] = []; replace(uri: { fsPath: string }, r: { at: number[] }, text: string) { ranges.push(r.at); this.ops.push({ path: uri.fsPath, text }); } }
mock.module("vscode", {
  namedExports: {
    WorkspaceEdit,
    Range: class { at: number[]; constructor(...a: number[]) { this.at = a; } },
    Uri: { file: (p: string) => ({ fsPath: p }) },
    workspace: {
      get textDocuments() { return open; },
      applyEdit: async (e: WorkspaceEdit) => { if (accept) edits.push(...e.ops); return accept; },
      fs: { writeFile: async (u: { fsPath: string }, b: Uint8Array) => { disk.set(u.fsPath, new TextDecoder().decode(b)); } },
      openTextDocument: async (u: { fsPath: string }) => ({ getText: () => `1\n2\n3 of ${u.fsPath}` }),
    },
  },
});
const { readTextFile, writeTextFile } = await import("../src/vscode/editorHost.ts");

const doc = (path: string) => ({ uri: { fsPath: path }, lineCount: 3, save: async () => { saved.push(path); return true; } });

test("a file nobody has open is written to disk", async () => {
  open = [doc("/w/other.c")];
  await writeTextFile("/w/new.c", "int x;");
  assert.equal(disk.get("/w/new.c"), "int x;");
  assert.deepEqual(edits, []);
});

test("a file open in the editor changes as an undoable edit, then is saved", async () => {
  open = [doc("/w/other.c"), doc("/w/main.c")];
  await writeTextFile("/w/main.c", "int main() { return 0; }");
  assert.deepEqual(edits, [{ path: "/w/main.c", text: "int main() { return 0; }" }]);
  assert.deepEqual(saved, ["/w/main.c"]);
  assert.deepEqual(ranges, [[0, 0, 3, 0]], "the whole document, from its very first character");
  assert.equal(disk.has("/w/main.c"), false);
});

test("an edit the editor refuses is reported, not taken as done", async () => {
  accept = false;
  open = [doc("/w/main.c")];
  await assert.rejects(writeTextFile("/w/main.c", "x"), /the editor refused the edit of \/w\/main.c/);
  accept = true;
});

test("reading goes through the editor and can stop at a line range", async () => {
  assert.equal(await readTextFile("/w/a.c"), "1\n2\n3 of /w/a.c");
  assert.equal(await readTextFile("/w/a.c", 2, 1), "2");
});
