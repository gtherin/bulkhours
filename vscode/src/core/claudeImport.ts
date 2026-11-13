// A Claude Code session file (~/.claude/projects/<folder>/<id>.jsonl) read as
// one conversation record (ADR-0223): what the person typed, what was
// answered, and each tool once, with its result cut short. Thinking, what
// the harness injected around the person's words, sub-agent talk and compact
// summaries are not part of the conversation. Pictures are left behind.
import type { SessionUpdate } from "@agentclientprotocol/sdk";
import type { Line } from "./conversationStore.ts";

export type Imported = { title: string; session: string; model: string; created: string; updated: string;
  body: Line[]; prompts: number; tools: number };

const OUTPUT_CHARS = 1500;
const TITLE_CHARS = 80;
const KINDS: Record<string, string> = { Bash: "execute", Read: "read", Edit: "edit", Write: "edit", Grep: "search", Glob: "search",
  WebFetch: "fetch", WebSearch: "fetch" };

// Added by the harness, never typed: <ide_opened_file>, <task-notification>,
// <system-reminder>, <command-name>..., and the note left for a pasted picture.
const INJECTED = /^(<[a-z_-]+>|\[Image: source:)/;
const INTERRUPTED = /^\[Request interrupted/;

type Block = { type?: string; text?: string; id?: string; name?: string; input?: Record<string, unknown>;
  tool_use_id?: string; content?: unknown; is_error?: boolean };
type Row = { type?: string; timestamp?: string; sessionId?: string; customTitle?: string; aiTitle?: string;
  isMeta?: boolean; isSidechain?: boolean; isCompactSummary?: boolean; isVisibleInTranscriptOnly?: boolean;
  message?: { model?: string; content?: string | Block[] } };
type Result = { text: string; failed: boolean };
const HIDDEN = ["isSidechain", "isMeta", "isCompactSummary", "isVisibleInTranscriptOnly"] as const;

function blocks(r: Row): Block[] {
  const c = r.message?.content;
  return typeof c === "string" ? [{ type: "text", text: c }] : Array.isArray(c) ? c : [];
}

function cut(text: string, chars: number, mark: string): string {
  return text.length > chars ? text.slice(0, chars) + mark : text;
}

function resultText(content: unknown): string {
  if (typeof content === "string") return content;
  if (!Array.isArray(content)) return "";
  return (content as Block[]).map((b) => (b.type === "text" ? b.text ?? "" : b.type === "image" ? "[image]" : "")).filter(Boolean).join("\n");
}

function toolTitle(name: string, input: Record<string, unknown>): string {
  const detail = [input.description, input.command, input.file_path, input.pattern, input.url, input.query]
    .find((v): v is string => typeof v === "string" && v.length > 0);
  return detail ? `${name}: ${cut(detail.split("\n")[0], TITLE_CHARS, "…")}` : name;
}

function toolCall(b: Block, result: Result | undefined): SessionUpdate {
  const input = b.input ?? {};
  const name = b.name ?? "Tool";
  const path = input.file_path;
  return {
    sessionUpdate: "tool_call", toolCallId: b.id, title: toolTitle(name, input), kind: KINDS[name] ?? "other",
    // No result: the turn was interrupted before the tool answered.
    status: result?.failed === false ? "completed" : "failed",
    locations: typeof path === "string" ? [{ path }] : [],
    content: result?.text ? [{ type: "content", content: { type: "text", text: result.text } }] : [],
  } as SessionUpdate;
}

function* parsed(raw: Iterable<string>): Generator<Row> {
  for (const line of raw) {
    try {
      const r = JSON.parse(line);
      if (r && typeof r === "object") yield r;
    } catch { /* a torn line */ }
  }
}

function speaks(r: Row): boolean {
  return (r.type === "user" || r.type === "assistant") && !HIDDEN.some((k) => r[k]);
}

// The rows that speak, and the session's title: the person's, else the generated one.
function scan(raw: Iterable<string>): { rows: Row[]; title: string } {
  const rows: Row[] = [];
  let custom = "", generated = "";
  for (const r of parsed(raw)) {
    if (r.type === "custom-title") custom = r.customTitle || custom;
    else if (r.type === "ai-title") generated = r.aiTitle || generated;
    else if (speaks(r)) rows.push(r);
  }
  return { rows, title: custom || generated };
}

function resultsOf(rows: Row[]): Map<string, Result> {
  const results = new Map<string, Result>();
  for (const b of rows.flatMap(blocks)) {
    if (b.type === "tool_result" && b.tool_use_id)
      results.set(b.tool_use_id, { text: cut(resultText(b.content), OUTPUT_CHARS, "\n[…]"), failed: Boolean(b.is_error) });
  }
  return results;
}

// The model that answered last (Claude Code marks its own notices "<synthetic>").
function modelOf(rows: Row[]): string {
  const named = rows.map((r) => (r.type === "assistant" && r.message?.model) || "").filter((m) => m && !m.startsWith("<"));
  return named[named.length - 1] ?? "";
}

// The record being written: turns, each closed by one stop.
class Turns {
  readonly body: Line[] = [];
  prompts = 0;
  tools = 0;
  private open = false;      // the turn holds something no stop has closed

  stop(reason: string): void {
    if (this.open) this.body.push({ t: "stop", reason });
    this.open = false;
  }

  ask(text: string): void {
    this.stop("end_turn");
    this.body.push({ t: "prompt", content: [{ type: "text", text }] });
    this.open = true;
    this.prompts++;
  }

  say(update: SessionUpdate): void {
    this.body.push({ t: "update", update });
    this.open = true;
  }
}

function person(turns: Turns, r: Row): void {
  const texts = blocks(r).map((b) => (b.type === "text" ? b.text?.trim() ?? "" : "")).filter(Boolean);
  if (texts.some((t) => INTERRUPTED.test(t))) turns.stop("cancelled");
  const typed = texts.filter((t) => !INJECTED.test(t) && !INTERRUPTED.test(t));
  if (typed.length) turns.ask(typed.join("\n\n"));
}

function assistant(turns: Turns, r: Row, results: Map<string, Result>): void {
  for (const b of blocks(r)) {
    if (b.type === "text" && b.text?.trim())
      turns.say({ sessionUpdate: "agent_message_chunk", content: { type: "text", text: b.text.trim() + "\n\n" } } as SessionUpdate);
    else if (b.type === "tool_use" && b.id) { turns.say(toolCall(b, results.get(b.id))); turns.tools++; }
  }
}

export function fromClaude(raw: Iterable<string>): Imported | undefined {
  const { rows, title } = scan(raw);
  const stamps = rows.map((r) => r.timestamp ?? "").filter(Boolean);
  const session = rows[0]?.sessionId;
  if (!session || !stamps.length) return undefined;
  const results = resultsOf(rows);
  const turns = new Turns();
  for (const r of rows) {
    if (r.type === "user") person(turns, r);
    else assistant(turns, r, results);
  }
  turns.stop("end_turn");
  return { title, session, model: modelOf(rows), created: stamps[0], updated: stamps[stamps.length - 1],
    body: turns.body, prompts: turns.prompts, tools: turns.tools };
}
