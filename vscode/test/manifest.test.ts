import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const manifest = JSON.parse(readFileSync(new URL("../package.json", import.meta.url), "utf8"));

test("the extension runs where the code is: on the Vast machine under Remote-SSH", () => {
  // IPSA's HPC students work over Remote-SSH (moodle/local/hpc/index.php): the
  // agent must see and build the files on the GPU machine, not on the laptop.
  assert.deepEqual(manifest.extensionKind, ["workspace"]);
});

test("every text the manifest shows exists in English and French", () => {
  const keys = [...JSON.stringify(manifest.contributes).matchAll(/"%([\w.]+)%"/g)].map((m) => m[1]);
  assert.ok(keys.length >= 7, "commands, view and settings are all translatable");
  for (const file of ["package.nls.json", "package.nls.fr.json"]) {
    const nls = JSON.parse(readFileSync(new URL(`../${file}`, import.meta.url), "utf8"));
    for (const k of keys) assert.ok(nls[k], `${file} lacks ${k}`);
  }
});

test("the publisher is the Marketplace publisher Gateka created", () => {
  assert.equal(manifest.publisher, "gateka");
});

test("the listing is publishable and links to the public source, under MIT", () => {
  assert.equal(manifest.private, undefined, "vsce refuses to publish a private manifest");
  assert.equal(manifest.license, "MIT");
  assert.match(readFileSync(new URL("../LICENSE", import.meta.url), "utf8"), /^MIT License/);
  assert.deepEqual(manifest.repository, { type: "git", url: "https://github.com/gtherin/bulkhours.git", directory: "vscode" });
  assert.equal(manifest.bugs.url, "https://github.com/gtherin/bulkhours/issues");
});
