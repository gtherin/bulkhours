import { test } from "node:test";
import assert from "node:assert/strict";
import { addUserPrompt, applyUpdate, type Transcript } from "../src/core/transcript.ts";

const text = (t: string) => ({ type: "text" as const, text: t });

test("consecutive agent chunks read as one message", () => {
  let t: Transcript = addUserPrompt([], "explain malloc");
  t = applyUpdate(t, { sessionUpdate: "agent_message_chunk", content: text("malloc ") });
  t = applyUpdate(t, { sessionUpdate: "agent_message_chunk", content: text("reserves memory.") });
  assert.deepEqual(t, [
    { kind: "user", text: "explain malloc" },
    { kind: "agent", text: "malloc reserves memory." },
  ]);
});

test("a thought between two answers splits them", () => {
  let t: Transcript = [];
  t = applyUpdate(t, { sessionUpdate: "agent_message_chunk", content: text("first") });
  t = applyUpdate(t, { sessionUpdate: "agent_thought_chunk", content: text("hmm") });
  t = applyUpdate(t, { sessionUpdate: "agent_message_chunk", content: text("second") });
  assert.deepEqual(t.map((e) => e.kind), ["agent", "thought", "agent"]);
});

test("a tool call is updated in place, never duplicated", () => {
  let t: Transcript = [];
  t = applyUpdate(t, {
    sessionUpdate: "tool_call", toolCallId: "t1", title: "Read main.c", kind: "read", status: "pending",
    locations: [{ path: "/w/main.c" }],
  });
  t = applyUpdate(t, { sessionUpdate: "agent_message_chunk", content: text("reading") });
  t = applyUpdate(t, {
    sessionUpdate: "tool_call_update", toolCallId: "t1", status: "completed",
    content: [{ type: "content", content: text("int main() {}") }],
  });
  assert.equal(t.length, 2);
  assert.deepEqual(t[0], {
    kind: "tool", id: "t1", title: "Read main.c", toolKind: "read", status: "completed",
    locations: ["/w/main.c"], diffs: [], output: "int main() {}",
  });
});

test("an edit keeps its diff so the student can review it", () => {
  const t = applyUpdate([], {
    sessionUpdate: "tool_call", toolCallId: "e1", title: "Edit main.c", kind: "edit",
    content: [{ type: "diff", path: "/w/main.c", oldText: "a", newText: "b" }],
  });
  assert.deepEqual(t[0], {
    kind: "tool", id: "e1", title: "Edit main.c", toolKind: "edit", status: "pending",
    locations: [], diffs: [{ path: "/w/main.c", oldText: "a", newText: "b" }], output: "",
  });
});

test("an update for an unknown tool call still shows it", () => {
  const t = applyUpdate([], { sessionUpdate: "tool_call_update", toolCallId: "x", status: "failed" });
  assert.deepEqual(t[0], {
    kind: "tool", id: "x", title: "Tool", toolKind: "other", status: "failed",
    locations: [], diffs: [], output: "",
  });
});

test("the plan is one entry, replaced where it stands", () => {
  let t: Transcript = [];
  t = applyUpdate(t, { sessionUpdate: "plan", entries: [{ content: "read", priority: "high", status: "in_progress" }] });
  t = applyUpdate(t, { sessionUpdate: "agent_message_chunk", content: text("ok") });
  t = applyUpdate(t, { sessionUpdate: "plan", entries: [{ content: "read", priority: "high", status: "completed" }] });
  assert.deepEqual(t, [
    { kind: "plan", entries: [{ content: "read", status: "completed" }] },
    { kind: "agent", text: "ok" },
  ]);
});

test("updates the chat does not draw leave the transcript unchanged", () => {
  const before: Transcript = [{ kind: "user", text: "hi" }];
  const after = applyUpdate(before, { sessionUpdate: "available_commands_update", availableCommands: [] });
  assert.equal(after, before);
});

test("a link chunk shows its name, not nothing", () => {
  const t = applyUpdate([], {
    sessionUpdate: "agent_message_chunk",
    content: { type: "resource_link", name: "notes.md", uri: "file:///w/notes.md" },
  });
  assert.deepEqual(t, [{ kind: "agent", text: "[notes.md](file:///w/notes.md)" }]);
});

test("every kind of chunk reads as something the student can see", () => {
  const chunk = (content: any) => applyUpdate([], { sessionUpdate: "agent_message_chunk", content })[0];
  assert.deepEqual(chunk({ type: "image", data: "", mimeType: "image/png" }), { kind: "agent", text: "[image]" });
  assert.deepEqual(chunk({ type: "audio", data: "", mimeType: "audio/wav" }), { kind: "agent", text: "[audio]" });
  assert.deepEqual(chunk({ type: "resource", resource: { uri: "file:///a", text: "body" } }), { kind: "agent", text: "body" });
  assert.deepEqual(chunk({ type: "resource", resource: { uri: "file:///b", blob: "AA==" } }), { kind: "agent", text: "[file:///b]" });
});

test("a terminal in a tool call is named, and a replayed user message is shown", () => {
  let t = applyUpdate([], {
    sessionUpdate: "tool_call", toolCallId: "r", title: "Run make",
    content: [{ type: "terminal", terminalId: "term-1" }],
  });
  assert.equal((t[0] as any).output, "[terminal term-1]");
  t = applyUpdate([], { sessionUpdate: "user_message_chunk", content: { type: "text", text: "earlier" } });
  assert.deepEqual(t, [{ kind: "user", text: "earlier" }]);
});

test("a notice is its own line", async () => {
  const { addNotice } = await import("../src/core/transcript.ts");
  assert.deepEqual(addNotice([], "stopped"), [{ kind: "notice", text: "stopped" }]);
});

test("an answer continues where it was, even deep in the conversation", () => {
  let t: Transcript = [{ kind: "user", text: "q1" }, { kind: "thought", text: "t" }, { kind: "agent", text: "a" }];
  t = applyUpdate(t, { sessionUpdate: "agent_message_chunk", content: text("b") });
  assert.deepEqual(t, [{ kind: "user", text: "q1" }, { kind: "thought", text: "t" }, { kind: "agent", text: "ab" }]);
});

test("two tool calls stay two, each updated where it stands", () => {
  let t: Transcript = [{ kind: "user", text: "go" }];
  t = applyUpdate(t, { sessionUpdate: "tool_call", toolCallId: "a", title: "Read a" });
  t = applyUpdate(t, { sessionUpdate: "tool_call", toolCallId: "b", title: "Read b" });
  t = applyUpdate(t, { sessionUpdate: "agent_message_chunk", content: text("done") });
  t = applyUpdate(t, { sessionUpdate: "tool_call_update", toolCallId: "b", status: "completed" });
  assert.deepEqual(t.map((e: any) => e.kind === "tool" ? `${e.title}:${e.status}` : e.kind),
    ["user", "Read a:pending", "Read b:completed", "agent"]);
});

test("the plan is replaced where it stands, between other entries", () => {
  const plan = (status: string) => ({ sessionUpdate: "plan" as const, entries: [{ content: "x", priority: "high" as const, status: status as any }] });
  let t: Transcript = [{ kind: "user", text: "go" }];
  t = applyUpdate(t, plan("pending"));
  t = applyUpdate(t, { sessionUpdate: "agent_message_chunk", content: text("ok") });
  t = applyUpdate(t, plan("completed"));
  assert.deepEqual(t.map((e) => e.kind), ["user", "plan", "agent"]);
  assert.deepEqual((t[1] as any).entries, [{ content: "x", status: "completed" }]);
});

test("an emptied file and a new file read differently in a diff", () => {
  const diff = (oldText: string | null) => (applyUpdate([], {
    sessionUpdate: "tool_call", toolCallId: "e", title: "Edit", content: [{ type: "diff", path: "/a", oldText, newText: "x" }],
  })[0] as any).diffs[0].oldText;
  assert.equal(diff(""), "");
  assert.equal(diff(null), null);
});
