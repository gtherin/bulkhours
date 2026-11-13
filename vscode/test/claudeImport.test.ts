// A Claude Code session taken over as a conversation of the panel (owner,
// 2026-11-13: "transform my claude session ... as maqi extension sessions").
// The record is ADR-0223's own: read back by the same store, under the
// session's name, with its run directory.
import { test } from "node:test";
import assert from "node:assert/strict";
import { existsSync, mkdtempSync, appendFileSync, statSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { ConversationStore } from "../src/core/conversationStore.ts";
import { fromClaude } from "../src/core/claudeImport.ts";

const root = () => mkdtempSync(join(tmpdir(), "bh-import-"));
const at = (s: number) => `2026-10-23T08:00:${String(s).padStart(2, "0")}.000Z`;
const row = (type: string, content: unknown, more: object = {}) =>
  JSON.stringify({ type, sessionId: "8903306c-e9b5-46a6", timestamp: at(seq++), message: { model: "claude-opus-5", content }, ...more });
let seq = 0;

const session = () => {
  seq = 0;
  return [
    JSON.stringify({ type: "ai-title", aiTitle: "Strait traffic study", sessionId: "8903306c-e9b5-46a6" }),
    row("user", [{ type: "text", text: "<ide_opened_file>app.py</ide_opened_file>" }, { type: "text", text: "plot the strait traffic" }]),
    row("assistant", [{ type: "thinking", thinking: "hidden" }]),
    row("assistant", [{ type: "text", text: "Reading the data." }]),
    row("assistant", [{ type: "tool_use", id: "toolu_1", name: "Bash", input: { command: "ls ~/data\nwc -l *", description: "List the data" } }]),
    row("user", [{ type: "tool_result", tool_use_id: "toolu_1", content: "x".repeat(4000) }]),
    row("assistant", [{ type: "tool_use", id: "toolu_2", name: "Read", input: { file_path: "/data/a.csv" } }]),
    row("user", [{ type: "tool_result", tool_use_id: "toolu_2", is_error: true, content: [{ type: "text", text: "no such file" }, { type: "image", source: {} }] }]),
    row("user", "summary of what came before", { isCompactSummary: true }),
    row("user", "sub-agent talk", { isSidechain: true }),
    row("user", "<task-notification>done</task-notification>"),
    row("assistant", [{ type: "tool_use", id: "toolu_3", name: "Bash", input: { command: "sleep 100" } }]),
    row("user", [{ type: "text", text: "[Request interrupted by user]" }]),
    row("user", "now the Arctic route"),
    row("assistant", [{ type: "text", text: "Done." }], { message: { model: "<synthetic>", content: [{ type: "text", text: "Done." }] } }),
    JSON.stringify({ type: "custom-title", customTitle: "hormuz", sessionId: "8903306c-e9b5-46a6" }),
    JSON.stringify({ type: "api-request-blob", message: { content: [{ type: "text", text: "never shown" }] } }),
    "{torn",
  ];
};

test("a Claude Code session reads as what was typed, what was answered, and each tool with its result", () => {
  const got = fromClaude(session())!;
  assert.equal(got.title, "hormuz", "the name the person gave wins over the generated one");
  assert.deepEqual([got.session, got.model, got.created, got.updated], ["8903306c-e9b5-46a6", "claude-opus-5", at(0), at(13)]);
  assert.deepEqual([got.prompts, got.tools], [2, 3]);
  assert.deepEqual(got.body.map((l) => l.t), ["prompt", "update", "update", "update", "update", "stop", "prompt", "update", "stop"]);
  const text = JSON.stringify(got.body);
  for (const absent of ["ide_opened_file", "hidden", "summary of what", "sub-agent", "task-notification", "never shown", "Request interrupted"])
    assert.ok(!text.includes(absent), `${absent} is not part of the conversation`);
  assert.equal(got.body[5].t === "stop" && got.body[5].reason, "cancelled", "an interrupted turn ends as cancelled");
});

test("an imported session opens in the panel under its name, with its run directory", () => {
  const dir = root();
  const store = new ConversationStore(dir);
  const got = fromClaude(session())!;
  const file = store.adopt({ agent: "claude-code", session: got.session, model: got.model, school: "maqi", cwd: "/home/u", name: got.title }, got);
  const o = store.read(file)!;
  assert.deepEqual([o.title, o.name, o.questions, o.pending, o.started], ["hormuz", "hormuz", 2, false, true]);
  assert.deepEqual(o.transcript.map((e) => e.kind), ["user", "agent", "tool", "tool", "tool", "user", "agent"]);
  const [list, read, hung] = o.transcript.filter((e) => e.kind === "tool") as any[];
  assert.deepEqual([list.title, list.toolKind, list.status], ["Bash: List the data", "execute", "completed"]);
  assert.ok(list.output.length < 1600 && list.output.endsWith("[…]"), "a long output is cut");
  assert.deepEqual([read.title, read.status, read.output, read.locations], ["Read: /data/a.csv", "failed", "no such file\n[image]", ["/data/a.csv"]]);
  assert.deepEqual([hung.title, hung.status], ["Bash: sleep 100", "failed"], "a tool that never answered did not succeed");
  assert.ok(existsSync(store.rendersDir("hormuz")));
  assert.equal(statSync(file).mtimeMs, Date.parse(at(13)), "it is dated when the session last spoke, not when it was imported");
  assert.deepEqual(store.list("/home/u").map((s) => [s.title, s.agent, s.questions]), [["hormuz", "claude-code", 2]]);
});

test("importing twice leaves one record; a record an agent here took over is not overwritten", () => {
  const store = new ConversationStore(root());
  const got = fromClaude(session())!;
  const h = { agent: "claude-code", session: got.session, model: got.model, school: "maqi", cwd: "/home/u", name: got.title };
  const file = store.adopt(h, got);
  assert.equal(store.adopt(h, got), file);
  assert.equal(store.list("/home/u").length, 1);
  appendFileSync(file, JSON.stringify({ t: "session", agent: "maqi", session: "s-2", model: "fast" }) + "\n");
  assert.throws(() => store.adopt(h, got), /continued here/);
});

test("a tool call that says nothing of itself, or whose result is empty, still shows", () => {
  seq = 0;
  const got = fromClaude([
    row("user", "go"),
    row("assistant", [{ type: "tool_use", id: "toolu_9" }, { type: "tool_use", id: "toolu_10", name: "Monitor", input: {} }]),
    row("user", [{ type: "tool_result", tool_use_id: "toolu_9" }, { type: "tool_result", tool_use_id: "toolu_10", content: [] }]),
  ])!;
  const calls = got.body.filter((l) => l.t === "update").map((l: any) => [l.update.title, l.update.kind, l.update.status, l.update.content, l.update.locations]);
  assert.deepEqual(calls, [["Tool", "other", "completed", [], []], ["Monitor", "other", "completed", [], []]]);
  assert.equal(got.title, "", "no title in the file: the panel takes the first request's");
});

test("a file that is not a Claude Code session imports nothing", () => {
  assert.equal(fromClaude(['{"t":"header"}', "", "not json", "null", '{"type":"user","message":{"content":"no session id"}}']), undefined);
});
