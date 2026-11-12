// The conversation record Gateka keeps, whatever agent answered (architect
// 2026-11-10 26f2ee, ADR-0223): ACP's own shape, under the XDG state folder,
// readable by its owner only, compact, and read back into the panel.
import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, statSync, utimesSync, existsSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { ConversationStore, condensed, stateRoot } from "../src/core/conversationStore.ts";

const root = () => mkdtempSync(join(tmpdir(), "bh-state-"));
const header = { agent: "gateka", session: "s-1", model: "fast", school: "ipsa", cwd: "/work/cuda" };
const chunk = (sessionUpdate: string, text: string) => ({ sessionUpdate, content: { type: "text", text } }) as any;

test("the state folder follows XDG, and GATEKA_STATE_HOME wins", () => {
  assert.equal(stateRoot({ GATEKA_STATE_HOME: "/s" }, "/home/a"), "/s");
  assert.equal(stateRoot({ XDG_STATE_HOME: "/x" }, "/home/a"), "/x/gateka");
  assert.equal(stateRoot({}, "/home/a"), "/home/a/.local/state/gateka");
});

test("a turn is written as one prompt, one message per kind, and each tool in its final state", () => {
  const r = root();
  const store = new ConversationStore(r);
  const c = store.start(header);
  c.prompt([{ type: "text", text: "why slow?" }]);
  c.update(chunk("agent_thought_chunk", "let me "));
  c.update(chunk("agent_thought_chunk", "look"));
  c.update({ sessionUpdate: "tool_call", toolCallId: "t1", title: "Read k.cu", status: "pending" } as any);
  c.update({ sessionUpdate: "tool_call_update", toolCallId: "t1", status: "completed" } as any);
  c.update(chunk("agent_message_chunk", "Use "));
  c.update(chunk("agent_message_chunk", "shared memory."));
  c.end("end_turn");
  const lines = readFileSync(c.file, "utf8").trim().split("\n").map((l) => JSON.parse(l));
  assert.deepEqual(lines.map((l) => l.t), ["header", "prompt", "update", "update", "update", "stop"]);
  assert.deepEqual(lines[0], { t: "header", v: 1, ...header, created: lines[0].created });
  assert.equal(lines[2].update.content.text, "let me look");
  assert.deepEqual(lines[3].update, { sessionUpdate: "tool_call", toolCallId: "t1", title: "Read k.cu", status: "completed" });
  assert.equal(lines[4].update.content.text, "Use shared memory.");
});

test("only its owner can read a conversation, and it never lives in the project", () => {
  const r = root();
  const c = new ConversationStore(r).start(header);
  c.end("end_turn");
  assert.equal(statSync(c.file).mode & 0o777, 0o600);
  assert.equal(statSync(join(c.file, "..")).mode & 0o777, 0o700);
  assert.ok(c.file.startsWith(r) && !c.file.startsWith(header.cwd));
});

test("the last conversation of a project is read back as the panel showed it", () => {
  const r = root();
  const store = new ConversationStore(r);
  const old = store.start({ ...header, session: "s-old" });
  old.prompt([{ type: "text", text: "old" }]); old.end("end_turn");
  const c = store.start(header);
  c.prompt([{ type: "text", text: "hello" }]);
  c.update(chunk("agent_message_chunk", "hi"));
  c.end("end_turn");
  const other = store.start({ ...header, cwd: "/work/other" });
  other.end("end_turn");
  const back = store.latest("/work/cuda")!;
  assert.equal(back.header.session, "s-1");
  assert.deepEqual(back.transcript, [{ kind: "user", text: "hello" }, { kind: "agent", text: "hi" }]);
  assert.equal(store.latest("/work/nothing"), undefined);
});

test("a turn cut short still keeps what was said", () => {
  const r = root();
  const c = new ConversationStore(r).start(header);
  c.prompt([{ type: "text", text: "go" }]);
  c.update(chunk("agent_message_chunk", "half"));
  c.end("cancelled");
  assert.deepEqual(new ConversationStore(r).latest("/work/cuda")!.transcript, [{ kind: "user", text: "go" }, { kind: "agent", text: "half" }]);
});

test("conversations older than the retention are pruned, recent ones kept", () => {
  const r = root();
  const store = new ConversationStore(r);
  const old = store.start({ ...header, session: "s-old" }); old.end("end_turn");
  const fresh = store.start(header); fresh.end("end_turn");
  const past = Date.now() / 1000 - 100 * 86400;
  utimesSync(old.file, past, past);
  assert.equal(store.prune(90), 1);
  assert.deepEqual([existsSync(old.file), existsSync(fresh.file)], [false, true]);
});

test("another agent gets the conversation so far, condensed, recent turns first to keep", () => {
  const t = [{ kind: "user", text: "q1" }, { kind: "agent", text: "a1" }, { kind: "user", text: "q2" }, { kind: "agent", text: "a2" }] as any;
  assert.equal(condensed(t, 10_000), "Student: q1\n\nAssistant: a1\n\nStudent: q2\n\nAssistant: a2");
  assert.equal(condensed(t, 40), "[…]\n\nStudent: q2\n\nAssistant: a2");
  assert.equal(condensed([], 100), "");
});

test("a conversation is titled by its first question until it is renamed", () => {
  const store = new ConversationStore(root());
  const c = store.start(header);
  c.prompt([{ type: "text", text: "Pourquoi mon kernel CUDA est lent quand n dépasse un million ?\nvoici le code" }]);
  c.end("end_turn");
  assert.equal(store.read(c.file)!.title, "Pourquoi mon kernel CUDA est lent quand n dépasse…");
  c.rename("Kernel lent");
  assert.equal(store.read(c.file)!.title, "Kernel lent");
});

test("a project's conversations are listed newest first, with what the history shows", () => {
  const store = new ConversationStore(root());
  const a = store.start({ ...header, session: "s-a" });
  a.prompt([{ type: "text", text: "first one" }]); a.end("end_turn");
  const b = store.start({ ...header, session: "s-b", agent: "claude" });
  b.prompt([{ type: "text", text: "second" }]); b.update(chunk("agent_message_chunk", "ok")); b.end("end_turn");
  b.prompt([{ type: "text", text: "again" }]); b.end("end_turn");
  const empty = store.start({ ...header, session: "s-empty" });
  const list = store.list("/work/cuda");
  assert.deepEqual(list.map((c) => [c.title, c.agent, c.questions]), [["second", "claude", 2], ["first one", "gateka", 1]]);
  assert.ok(list[0].updated >= list[1].updated);
  assert.ok(!list.some((c) => c.file === empty.file), "a conversation with no question is not listed");
});

test("a picture a tool showed the agent is not kept: the record stays small, the panel still says [image]", () => {
  const store = new ConversationStore(root());
  const c = store.start(header);
  c.prompt([{ type: "text", text: "read the screenshot" }]);
  const picture = "A".repeat(2_000_000);
  c.update({ sessionUpdate: "tool_call", toolCallId: "t1", title: "read_image", status: "pending" } as any);
  c.update({ sessionUpdate: "tool_call_update", toolCallId: "t1", status: "completed",
    content: [{ type: "content", content: { type: "text", text: "1920x1080" } },
      { type: "content", content: { type: "image", mimeType: "image/jpeg", data: picture } }] } as any);
  c.end("end_turn");
  assert.ok(statSync(c.file).size < 10_000);
  const tool = store.latest(header.cwd)!.transcript.find((e) => e.kind === "tool") as any;
  assert.match(JSON.stringify(tool), /\[image\]/);
});

test("a long conversation reads back whole, lines across read chunks included", () => {
  const store = new ConversationStore(root());
  const c = store.start(header);
  for (let i = 0; i < 40; i++) {
    c.prompt([{ type: "text", text: `question ${i}` }]);
    c.update(chunk("agent_message_chunk", `answer ${i} ` + "x".repeat(100_000)));
    c.end("end_turn");
  }
  const o = store.latest(header.cwd)!;
  assert.equal(o.questions, 40);
  assert.equal(o.title, "question 0");
  assert.match((o.transcript.at(-1) as any).text, /^answer 39 x+$/);
});
