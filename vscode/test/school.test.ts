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
  assert.deepEqual(parseSchool(ipsa), { ...ipsa, language: "en", title: "BulkHours IPSA", prefix: "bulkhours", links: [] });
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

test("a variant may name its own state folder, absolute or under ~", () => {
  assert.equal(parseSchool({ ...ipsa, stateDir: "~/.maqi" }).stateDir, "~/.maqi");
  assert.equal(parseSchool(ipsa).stateDir, undefined);
  assert.throws(() => parseSchool({ ...ipsa, stateDir: ".maqi" }), /school ipsa: "stateDir" must start with ~\/ or \//);
});

test("a variant on its platform's own connection needs no sign-in addresses", () => {
  const { signInUrl, keyUrl, creditsUrl, ...rest } = ipsa;
  const connection = { keyFile: "/run/maqi/keys/${user}/llm.env",
    offer: { models: ["fast"], agent: { id: "maqi", label: "MaQI", command: "dsh" } } };
  const maqi = parseSchool({ ...rest, id: "maqi", connection });
  assert.equal(maqi.connection?.keyFile, "/run/maqi/keys/${user}/llm.env");
  assert.equal(maqi.signInUrl, undefined);
  assert.throws(() => parseSchool({ ...rest, connection: { ...connection, keyFile: "llm.env" } }), /school ipsa: "keyFile" must be an absolute path/);
  assert.throws(() => parseSchool({ ...rest, connection: { ...connection, offer: { models: [] } } }), /school ipsa: /);
  assert.throws(() => parseSchool(rest), /school ipsa: "signInUrl" must be an https address/, "without a connection, the sign-in stays required");
});

test("a platform may name its status command, absolute, with its arguments", () => {
  const { signInUrl, keyUrl, creditsUrl, ...rest } = ipsa;
  const connection = { keyFile: "/run/maqi/keys/${user}/llm.env", offer: { models: ["fast"], agent: { id: "maqi", label: "MaQI", command: "dsh" } },
    status: { command: "/opt/tljh/user/bin/python", args: ["${extensionPath}/media/platform/maqi-status.py", "${lang}"] } };
  assert.deepEqual(parseSchool({ ...rest, connection }).connection?.status?.args, ["${extensionPath}/media/platform/maqi-status.py", "${lang}"]);
  assert.throws(() => parseSchool({ ...rest, connection: { ...connection, status: { command: "python" } } }), /"status.command" must be an absolute path/);
});

test("a variant may list its platform's links, https only, for the panel's links button", () => {
  const links = [{ label: "Docs", url: "https://maqi.ai.msct.fr/handbook/getting-started/", icon: "book" },
    { label: "Git", url: "https://git.maqi.ai.msct.fr" }];
  assert.deepEqual(parseSchool({ ...ipsa, links }).links, links);
  assert.deepEqual(parseSchool(ipsa).links, []);
  assert.throws(() => parseSchool({ ...ipsa, links: [{ label: "x", url: "http://a.fr" }] }), /school ipsa: "links" must be \{label, https url, icon\?\} items/);
  assert.throws(() => parseSchool({ ...ipsa, links: [{ label: "", url: "https://a.fr" }] }), /"links"/);
});
