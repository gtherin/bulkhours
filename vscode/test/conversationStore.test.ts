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

// Owner 2026-11-12, after a day of ~/.maqi and ~/.gateka: "use the .local as
// behaviour" - one rule, XDG: $XDG_STATE_HOME/<the variant's name>, gateka by
// default. No dot-folder in the home; the person's setting can still move it.
test("the state folder: the environment, then the setting, then XDG under the variant's name", () => {
  assert.equal(stateRoot({}, "/home/a", { name: "maqi" }), "/home/a/.local/state/maqi");
  assert.equal(stateRoot({ XDG_STATE_HOME: "/x" }, "/home/a", { name: "maqi" }), "/x/maqi");
  assert.equal(stateRoot({}, "/home/a", { name: "maqi", setting: "/data/a/maqi" }), "/data/a/maqi");
  assert.equal(stateRoot({ GATEKA_STATE_HOME: "/s" }, "/home/a", { name: "maqi", setting: "~/x" }), "/s");
  assert.equal(stateRoot({}, "/home/a", { name: "maqi", setting: "  " }), "/home/a/.local/state/maqi", "an empty setting is no setting");
  assert.equal(stateRoot({}, "/home/a", { setting: "relative/dir" }), "/home/a/.local/state/gateka", "only an absolute or ~ path is taken");
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

// -- session names, run directories, status for monitoring (owner 2026-11-12:
// "do you keep track of the name of the sessions? we will soon allocate a run
// directory per session and monitoring pages... prepare that") ----------------
import { mkdirSync as mkdir, writeFileSync as write, readdirSync as ls } from "node:fs";
import { slug } from "../src/core/conversationStore.ts";

test("a name is a slug: lowercase, plain letters, digits, dots and dashes", () => {
  assert.equal(slug("Why is my kernel slow?"), "why-is-my-kernel-slow");
  assert.equal(slug("  Stealth 2026-11 — étape n°2  "), "stealth-2026-11-etape-n-2");
  assert.equal(slug("second.brain"), "second.brain");
  assert.equal(slug("???"), "session");
  assert.ok(slug("x".repeat(100)).length <= 40);
  assert.equal(slug("../../etc/passwd"), "etc-passwd");
});

test("a conversation's name is claimed once with its run directory, and kept through a reload and a rename", () => {
  const r = root(); const store = new ConversationStore(r);
  const a = store.start({ ...header, name: store.reserve("Why is my kernel slow?\nsecond line") });
  a.prompt([{ type: "text", text: "Why is my kernel slow?" }]); a.end("end_turn");
  assert.equal(store.read(a.file)!.name, "why-is-my-kernel-slow");
  assert.equal(statSync(store.sessionDir("why-is-my-kernel-slow")).mode & 0o777, 0o700);
  assert.equal(store.rename(a.file, "Stealth 2026-11"), "why-is-my-kernel-slow", "a rename is the title's: the name is the directory's key");
  assert.equal(new ConversationStore(r).read(a.file)!.title, "Stealth 2026-11");
  assert.equal(store.list(header.cwd)[0].name, "why-is-my-kernel-slow");
});

test("two windows asking for the same name get two run directories", () => {
  const r = root();
  const one = new ConversationStore(r), two = new ConversationStore(r);
  assert.deepEqual([one.reserve("hello"), two.reserve("hello"), one.reserve("hello")], ["hello", "hello-2", "hello-3"]);
  assert.deepEqual(ls(join(r, "sessions")).sort(), ["hello", "hello-2", "hello-3"]);
});

test("an older record with no name gets one when it is opened, not when it is listed", () => {
  const r = root(); const store = new ConversationStore(r);
  const c = store.start(header); c.prompt([{ type: "text", text: "hello" }]); c.end("end_turn");
  assert.equal(store.list(header.cwd)[0].name, "");
  assert.equal(existsSync(join(r, "sessions")), false, "listing allocates nothing");
  assert.equal(store.name(c.file), "hello");
  assert.equal(store.name(c.file), "hello", "asked again: the same, written once");
  assert.equal(readFileSync(c.file, "utf8").split("\n").filter((l) => l.includes('"t":"name"')).length, 1);
});

test("a record another tool seeded with a name, in any folder, is one of the project's sessions and joins its run directory", () => {
  const r = root(); const store = new ConversationStore(r);
  const dir = join(r, "conversations", "849f5076722b7e18"); mkdir(dir, { recursive: true });
  const seeded = join(dir, "1794504546332-0000-821a929e.jsonl");
  write(seeded,
    JSON.stringify({ t: "header", v: 1, agent: "claude", name: "alpha", session: "s-9", model: "fast", school: "ipsa", cwd: header.cwd, created: "2026-11-12T17:29:06.358Z" }) + "\n"
    + JSON.stringify({ t: "prompt", content: [{ type: "text", text: "alpha — read HANDOFF.md and take over." }] }) + "\n");
  write(join(dir, "1794504546999-0000-aaaaaaaa.jsonl"),
    JSON.stringify({ t: "header", v: 1, agent: "claude", name: "elsewhere", session: "s-8", model: "fast", school: "ipsa", cwd: "/other/project", created: "2026-11-12T17:30:00.000Z" }) + "\n"
    + JSON.stringify({ t: "prompt", content: [{ type: "text", text: "not this project" }] }) + "\n");
  assert.deepEqual(store.list(header.cwd).map((c) => [c.name, c.questions]), [["alpha", 1]], "listed by its header's folder, not by where it sits");
  mkdir(store.sessionDir("alpha"), { recursive: true }); write(join(store.sessionDir("alpha"), "HANDOFF.md"), "notes");
  assert.equal(store.name(seeded), "alpha", "it joins the run directory that is there");
  assert.deepEqual(ls(store.sessionDir("alpha")), ["HANDOFF.md"]);
  assert.equal(store.reserve("alpha"), "alpha-2", "a new conversation never takes a session's directory");
});

test("a session's status is written in its run directory, whole or not at all; pruning never touches run directories", () => {
  const r = root(); const store = new ConversationStore(r);
  const c = store.start(header); c.prompt([{ type: "text", text: "long job" }]); c.end("end_turn");
  const name = store.name(c.file);
  store.writeStatus(name, { name, title: "long job", cwd: header.cwd, agent: "gateka", model: "fast", state: "working",
    since: 1, last: 2, tool: "nvcc k.cu", questions: 1, updated: 3, record: c.file });
  const dir = store.sessionDir(name);
  assert.deepEqual(ls(dir), ["session.json"]);
  assert.equal(JSON.parse(readFileSync(join(dir, "session.json"), "utf8")).state, "working");
  assert.equal(statSync(dir).mode & 0o777, 0o700);
  utimesSync(c.file, new Date(0), new Date(0));
  assert.equal(store.prune(90), 1);
  assert.equal(existsSync(join(dir, "session.json")), true);
});

test("a session's pages are the html files of its renders folder, newest first", () => {
  const r = root(); const store = new ConversationStore(r);
  const name = store.reserve("stealth explorer");
  assert.deepEqual(store.renders(name), [], "no folder yet: no page");
  const dir = store.rendersDir(name); mkdir(join(dir, "sub"), { recursive: true });
  assert.equal(dir, join(r, "sessions", "stealth-explorer", "renders"));
  write(join(dir, "old.html"), "<p>1</p>"); utimesSync(join(dir, "old.html"), new Date(1e9), new Date(1e9));
  write(join(dir, "explorer.html"), "<p>2</p>"); write(join(dir, "notes.md"), "x"); write(join(dir, "sub", "deep.html"), "x");
  assert.deepEqual(store.renders(name).map((p) => p.name), ["explorer.html", "old.html"]);
  assert.equal(store.renders(name)[0].file, join(dir, "explorer.html"));
});
