// Takes a Claude Code session over as a conversation of the panel:
//   node --experimental-strip-types scripts/import-claude.ts <session.jsonl>... --state <state folder> --cwd <folder opened in VS Code> --school <variant id>
// Run where the session lives: nothing leaves the machine. Run again after
// the session went on in Claude Code: its one record is replaced.
import { readFileSync } from "node:fs";
import { parseArgs } from "node:util";
import { ConversationStore } from "../src/core/conversationStore.ts";
import { fromClaude } from "../src/core/claudeImport.ts";

const { values, positionals } = parseArgs({ allowPositionals: true,
  options: { state: { type: "string" }, cwd: { type: "string" }, school: { type: "string" } } });
if (!positionals.length || !values.state || !values.cwd || !values.school) {
  console.error("usage: import-claude <session.jsonl>... --state <folder> --cwd <folder> --school <id>");
  process.exit(2);
}
const store = new ConversationStore(values.state);
for (const path of positionals) {
  const got = fromClaude(readFileSync(path, "utf8").split("\n"));
  if (!got) { console.error(`${path}: not a Claude Code session`); process.exitCode = 1; continue; }
  const file = store.adopt({ agent: "claude-code", session: got.session, model: got.model, school: values.school, cwd: values.cwd,
    ...(got.title ? { name: got.title } : {}) }, got);
  const name = store.read(file)?.name ?? "";
  console.log(`${got.title || got.session}: ${got.prompts} requests, ${got.tools} tools, session ${name || "(named at first open)"} -> ${file}`);
}
