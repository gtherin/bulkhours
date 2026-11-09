// node scripts/build.mjs <school>  ->  dist/extension.cjs for that school.
// The school file is checked here, at build time, with the same parser the
// extension uses: a bad school file never reaches a student.
import { readFileSync } from "node:fs";
import { build } from "esbuild";
import { parseSchool } from "../src/core/school.ts";

export async function buildFor(id) {
  const school = parseSchool(JSON.parse(readFileSync(new URL(`../schools/${id}.json`, import.meta.url), "utf8")));
  await build({
    entryPoints: [new URL("../src/vscode/extension.ts", import.meta.url).pathname],
    outfile: new URL("../dist/extension.cjs", import.meta.url).pathname,
    bundle: true, platform: "node", format: "cjs", target: "node20",
    external: ["vscode"], sourcemap: true, logLevel: "warning",
    define: { __SCHOOL__: JSON.stringify(school) },
  });
  return school;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const id = process.argv[2];
  if (!id) { console.error("usage: node scripts/build.mjs <school-id>"); process.exit(2); }
  const school = await buildFor(id);
  console.log(`built dist/extension.cjs for ${school.name}`);
}
