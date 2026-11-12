import { test } from "node:test";
import assert from "node:assert/strict";
import { DEFAULT_PORT, parsePort } from "../src/core/dashboard.ts";

test("a dashboard port is a user port, typed as digits", () => {
  assert.equal(DEFAULT_PORT, 8501);
  assert.equal(parsePort(" 8501 "), 8501);
  assert.equal(parsePort("2718"), 2718);
  assert.equal(parsePort("80"), undefined, "below 1024: not a user's app");
  assert.equal(parsePort("70000"), undefined);
  assert.equal(parsePort("85o1"), undefined);
  assert.equal(parsePort(undefined), undefined);
});
