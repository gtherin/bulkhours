// node scripts/package-school.mjs <variant>  ->  dist/<name>-<version>.vsix
// (bulkhours-ipsa, maqi, gateka, bulkhours: one code, a config file each).
// Each school is its own extension (its own id on the Marketplace), built from
// the same code. The manifest is rewritten in a staging folder, never in place.
import { cpSync, existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { buildFor } from "./build.mjs";
import { packageName } from "../src/core/school.ts";

const id = process.argv[2];
if (!id) { console.error("usage: node scripts/package-school.mjs <school-id>"); process.exit(2); }

const root = new URL("..", import.meta.url).pathname;
const school = await buildFor(id);
const stage = `${root}build/${id}`;
rmSync(stage, { recursive: true, force: true });
mkdirSync(stage, { recursive: true });
for (const part of ["dist", "media", "README.md", "CHANGELOG.md", "LICENSE", "package.nls.json", "package.nls.fr.json"]) cpSync(`${root}${part}`, `${stage}/${part}`, { recursive: true });
// The listing students read: the school's own page when there is one.
if (existsSync(`${root}schools/${id}.md`)) cpSync(`${root}schools/${id}.md`, `${stage}/README.md`);
if (existsSync(`${root}schools/${id}.png`)) cpSync(`${root}schools/${id}.png`, `${stage}/media/icon.png`);
// The variant's own mark in the activity bar (one colour, as VS Code draws it).
if (existsSync(`${root}schools/${id}.svg`)) cpSync(`${root}schools/${id}.svg`, `${stage}/media/icon.svg`);

const manifest = JSON.parse(readFileSync(`${root}package.json`, "utf8"));
// Commands, view and settings under the variant's prefix: two variants
// installed side by side (bulkhours-ipsa and maqi) never collide.
manifest.contributes = JSON.parse(JSON.stringify(manifest.contributes)
  .replace(/"bulkhours\./g, `"${school.prefix}.`).replace(/(view == )bulkhours\./g, `$1${school.prefix}.`)
  .replace(/"bulkhours"/g, `"${school.prefix}"`).replace(/"BulkHours"/g, JSON.stringify(school.title)));
manifest.name = packageName(school);
manifest.displayName = school.title;
manifest.description = `${school.name}'s coding assistant: chat with an agent that reads and edits your project, on your credits.`;
manifest.activationEvents = (manifest.activationEvents ?? []).map((e) => e.replace(/^(onView:)bulkhours\./, `$1${school.prefix}.`));
if (existsSync(`${root}schools/${id}.png`)) manifest.icon = "media/icon.png";
delete manifest.devDependencies;
delete manifest.dependencies;
delete manifest.scripts;
writeFileSync(`${stage}/package.json`, JSON.stringify(manifest, null, 2));

const out = `${root}dist/${manifest.name}-${manifest.version}.vsix`;
execFileSync(`${root}node_modules/.bin/vsce`, ["package", "--no-dependencies", "-o", out],
  { cwd: stage, stdio: "inherit" });
console.log(`packaged ${out}`);
