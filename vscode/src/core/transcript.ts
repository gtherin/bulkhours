// The chat as the student reads it, folded from the agent's stream of
// `session/update` notifications. Pure: no VS Code, no I/O.
import type { ContentBlock, SessionUpdate, ToolCallContent } from "@agentclientprotocol/sdk";

export type ToolStatus = "pending" | "in_progress" | "completed" | "failed";
export type Diff = { path: string; oldText: string | null; newText: string };
export type PlanItem = { content: string; status: string };

export type Entry =
  | { kind: "user"; text: string; images?: string[] }
  | { kind: "agent"; text: string }
  | { kind: "thought"; text: string }
  | { kind: "plan"; entries: PlanItem[] }
  | { kind: "notice"; text: string }
  | {
      kind: "tool"; id: string; title: string; toolKind: string; status: ToolStatus;
      locations: string[]; diffs: Diff[]; output: string;
    };

export type Transcript = readonly Entry[];
type Tool = Extract<Entry, { kind: "tool" }>;

export function addUserPrompt(t: Transcript, text: string, images: string[] = []): Transcript {
  return [...t, images.length ? { kind: "user", text, images } : { kind: "user", text }];
}

export function addNotice(t: Transcript, text: string): Transcript {
  return [...t, { kind: "notice", text }];
}

export function applyUpdate(t: Transcript, u: SessionUpdate): Transcript {
  switch (u.sessionUpdate) {
    case "agent_message_chunk": return appendText(t, "agent", blockText(u.content));
    case "agent_thought_chunk": return appendText(t, "thought", blockText(u.content));
    case "user_message_chunk": return appendText(t, "user", blockText(u.content));
    case "tool_call":
    case "tool_call_update": return upsertTool(t, u);
    case "plan": return upsertPlan(t, u.entries.map((e) => ({ content: e.content, status: e.status })));
    default: return t;
  }
}

function appendText(t: Transcript, kind: "agent" | "thought" | "user", text: string): Transcript {
  const last = t[t.length - 1];
  if (last && last.kind === kind) return [...t.slice(0, -1), { kind, text: last.text + text }];
  return [...t, { kind, text }];
}

function blockText(b: ContentBlock): string {
  switch (b.type) {
    case "text": return b.text;
    case "resource_link": return `[${b.name}](${b.uri})`;
    case "resource": return "text" in b.resource ? b.resource.text : `[${b.resource.uri}]`;
    case "image": return "[image]";
    case "audio": return "[audio]";
  }
}

type ToolUpdate = Extract<SessionUpdate, { sessionUpdate: "tool_call" | "tool_call_update" }>;

function upsertTool(t: Transcript, u: ToolUpdate): Transcript {
  const at = t.findIndex((e) => e.kind === "tool" && e.id === u.toolCallId);
  const base: Tool = at >= 0 ? (t[at] as Tool) : {
    kind: "tool", id: u.toolCallId, title: "Tool", toolKind: "other", status: "pending",
    locations: [], diffs: [], output: "",
  };
  const next: Tool = {
    ...base,
    title: u.title ?? base.title,
    toolKind: u.kind ?? base.toolKind,
    status: (u.status ?? base.status) as ToolStatus,
    locations: u.locations ? u.locations.map((l) => l.path) : base.locations,
    ...(u.content ? splitContent(u.content) : {}),
  };
  return at >= 0 ? [...t.slice(0, at), next, ...t.slice(at + 1)] : [...t, next];
}

function splitContent(content: ToolCallContent[]): Pick<Tool, "diffs" | "output"> {
  const diffs: Diff[] = [];
  const out: string[] = [];
  for (const c of content) {
    if (c.type === "diff") diffs.push({ path: c.path, oldText: c.oldText ?? null, newText: c.newText });
    else if (c.type === "content") out.push(blockText(c.content));
    else out.push(`[terminal ${c.terminalId}]`);
  }
  return { diffs, output: out.join("\n") };
}

function upsertPlan(t: Transcript, entries: PlanItem[]): Transcript {
  const at = t.findIndex((e) => e.kind === "plan");
  const plan: Entry = { kind: "plan", entries };
  return at >= 0 ? [...t.slice(0, at), plan, ...t.slice(at + 1)] : [...t, plan];
}
