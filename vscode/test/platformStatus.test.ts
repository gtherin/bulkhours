// A platform's own status bar (owner 2026-11-12: "expect to see the wasabi
// rights", "and the ram usage", "can we have cpu as well"): the platform's
// command prints items, the extension only shows them.
import { test } from "node:test";
import assert from "node:assert/strict";
import { parseStatus } from "../src/core/platformStatus.ts";

test("status items are taken as the platform prints them, checked one by one", () => {
  const out = JSON.stringify({ items: [
    { id: "memory", text: "RAM 1.7 Go / 28.0 Go", tooltip: "Your session", level: "ok" },
    { id: "data", text: "$(database) 14/14 · 15 jeux", tooltip: "✓ maqi-derived", level: "warn" },
    { id: "Bad Id", text: "x", level: "ok" },
    { id: "cpu", text: 3, level: "ok" },
    { id: "egress", text: "$(cloud-upload) 32 GB", level: "loud" },
  ] });
  assert.deepEqual(parseStatus(out), [
    { id: "memory", text: "RAM 1.7 Go / 28.0 Go", tooltip: "Your session", level: "ok" },
    { id: "data", text: "$(database) 14/14 · 15 jeux", tooltip: "✓ maqi-derived", level: "warn" },
    { id: "egress", text: "$(cloud-upload) 32 GB", tooltip: "", level: "ok" },
  ]);
});

test("anything but the expected JSON shows nothing, never an error", () => {
  assert.deepEqual(parseStatus("Traceback (most recent call last):"), []);
  assert.deepEqual(parseStatus(JSON.stringify({ items: "no" })), []);
  assert.equal(parseStatus(JSON.stringify({ items: [{ id: "a", text: "x".repeat(200), level: "ok" }] }))[0].text.length, 80);
});
