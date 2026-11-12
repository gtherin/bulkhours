import { test } from "node:test";
import assert from "node:assert/strict";
import { parseSchool } from "../src/core/school.ts";

const ipsa = {
  id: "ipsa",
  name: "IPSA",
  accent: "#c8102e",
  signInUrl: "https://bulkhours.fr/workbench/sign-in?school=ipsa",
  keyUrl: "https://bulkhours.fr/api/workbench/key",
  creditsUrl: "https://bulkhours.fr/api/workbench/credits",
};

test("a school build file carries identity, addresses and a language", () => {
  assert.deepEqual(parseSchool(ipsa), { ...ipsa, language: "en", title: "BulkHours IPSA", prefix: "bulkhours" });
  assert.equal(parseSchool({ ...ipsa, language: "fr" }).language, "fr");
  assert.throws(() => parseSchool({ ...ipsa, language: "de" }), /school ipsa: "language" must be fr or en/);
});

test("every school needs its sign-in and key addresses over https", () => {
  assert.throws(() => parseSchool({ ...ipsa, keyUrl: "http://bulkhours.fr/api/workbench/key" }), /school ipsa: "keyUrl" must be an https address/);
  assert.throws(() => parseSchool({ ...ipsa, signInUrl: undefined }), /school ipsa: "signInUrl" must be an https address/);
});

test("the id is a slug, since it names the extension", () => {
  assert.throws(() => parseSchool({ ...ipsa, id: "IPSA Paris" }), /school id must be lowercase letters, digits or dashes/);
});

test("the accent is a colour", () => {
  assert.throws(() => parseSchool({ ...ipsa, accent: "red" }), /school ipsa: "accent" must be a #rrggbb colour/);
});

test("a school needs a name, and an empty file is refused", () => {
  assert.throws(() => parseSchool({ ...ipsa, name: "" }), /school ipsa: "name" must be a non-empty string/);
  assert.throws(() => parseSchool(undefined), /school id must be lowercase/);
});

// gateka, maqi, ipsa, bulkhours: one code, a config file each (owner,
// 2026-11-12). The title names it everywhere; the prefix names its commands,
// view and settings, so two of them installed side by side never collide.
test("a variant carries its own title, prefix and icon colours", () => {
  const maqi = parseSchool({ ...ipsa, id: "maqi", name: "MaQI", title: "MaQI", prefix: "maqi", tile: "#1a1c21" });
  assert.deepEqual([maqi.title, maqi.prefix, maqi.tile], ["MaQI", "maqi", "#1a1c21"]);
  assert.throws(() => parseSchool({ ...ipsa, prefix: "Ma QI" }), /school ipsa: "prefix" must be lowercase letters and digits/);
  assert.throws(() => parseSchool({ ...ipsa, tile: "dark" }), /school ipsa: "tile" must be a #rrggbb colour/);
});
