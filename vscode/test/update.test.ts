import { test } from "node:test";
import assert from "node:assert/strict";
import { newer, offeredUpdate } from "../src/core/update.ts";

test("a version is newer number by number, not as text", () => {
  assert.equal(newer("0.1.9", "0.1.8"), true);
  assert.equal(newer("0.1.10", "0.1.9"), true);
  assert.equal(newer("0.2.0", "0.1.12"), true);
  assert.equal(newer("0.1.8", "0.1.8"), false);
  assert.equal(newer("0.1.7", "0.1.8"), false);
  assert.equal(newer("nonsense", "0.1.8"), false);
});

test("the download area names this school's latest build, and only a newer one is offered", () => {
  const latest = { ipsa: "0.1.9", polytechnique: "0.1.8" };
  assert.deepEqual(offeredUpdate(latest, "ipsa", "0.1.8", "https://bulkhours.fr/bkfpage/vscode/"),
    { version: "0.1.9", url: "https://bulkhours.fr/bkfpage/vscode/bulkhours-ipsa-0.1.9.vsix" });
  assert.equal(offeredUpdate(latest, "polytechnique", "0.1.8", "https://bulkhours.fr/bkfpage/vscode/"), undefined);
  assert.equal(offeredUpdate({}, "ipsa", "0.1.8", "https://x/"), undefined);
  assert.equal(offeredUpdate({ ipsa: "1.0.0" }, "ipsa", "0.1.8", "http://plain/"), undefined, "only over https");
});
