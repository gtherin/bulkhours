// node scripts/package-school.mjs <school>  ->  dist/bulkhours-<school>-<version>.vsix
// Each school is its own extension (its own id on the Marketplace), built from
// the same code. The manifest is rewritten in a staging folder, never in place.
import { cpSync, existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { buildFor } from "./build.mjs";

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

const manifest = JSON.parse(readFileSync(`${root}package.json`, "utf8"));
manifest.name = `bulkhours-${school.id}`;
manifest.displayName = `BulkHours ${school.name}`;
manifest.description = `${school.name}'s coding assistant: chat with an agent that reads and edits your project, on your school credits.`;
manifest.contributes.viewsContainers.activitybar[0].title = `BulkHours ${school.name}`;
if (existsSync(`${root}schools/${id}.png`)) manifest.icon = "media/icon.png";
delete manifest.devDependencies;
delete manifest.dependencies;
delete manifest.scripts;
writeFileSync(`${stage}/package.json`, JSON.stringify(manifest, null, 2));

const out = `${root}dist/bulkhours-${school.id}-${manifest.version}.vsix`;
execFileSync(`${root}node_modules/.bin/vsce`, ["package", "--no-dependencies", "-o", out],
  { cwd: stage, stdio: "inherit" });
console.log(`packaged ${out}`);
