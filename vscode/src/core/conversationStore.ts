// The conversation record Gateka keeps, whatever agent answers (architect
// 2026-11-10 26f2ee; ADR-0223 "client-side agent conversation record").
//
// Each agent saves its own sessions in its own format (dsh in $DSH_HOME,
// Claude Code in ~/.claude...): switching agent would lose them. This record
// is ACP's own wire shape - the student's prompt blocks and the agent's
// session/update notifications - so any agent's conversation reads back the
// same, and a new agent can be handed the conversation so far.
//
//   <state>/conversations/<project hash>/<time>-<id>.jsonl
//     {"t":"header","v":1,"agent","session","model","school","cwd","created"}
//     {"t":"prompt","content":[...]}        one per question
//     {"t":"update","update":{...}}         one per message, tool or plan
//     {"t":"stop","reason":"end_turn"}      one per turn
//     {"t":"session",...}                   when another agent session takes over
//     {"t":"title","title":"..."}           when the student names it
//
// Compact: streamed chunks are joined into one message, a tool is written in
// its final state. Private: folder 0700, files 0600 (a shared GPU machine
// holds many students), never in the project (it may be shared or in git),
// never synced. Pruned after a retention.
import { createHash, randomUUID } from "node:crypto";
import { appendFileSync, chmodSync, closeSync, existsSync, mkdirSync, openSync, readdirSync, readSync, statSync, unlinkSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import type { ContentBlock, SessionUpdate } from "@agentclientprotocol/sdk";
import { addUserPrompt, applyUpdate, type Entry, type Transcript } from "./transcript.ts";

export function stateRoot(env: Record<string, string | undefined>, home: string): string {
  if (env.GATEKA_STATE_HOME) return env.GATEKA_STATE_HOME;
  return join(env.XDG_STATE_HOME || join(home, ".local", "state"), "gateka");
}

export type Header = { agent: string; session: string; model: string; school: string; cwd: string };
type Line =
  | ({ t: "header"; v: 1; created: string } & Header)
  | { t: "prompt"; content: ContentBlock[] }
  | { t: "update"; update: SessionUpdate }
  | { t: "stop"; reason: string }
  | ({ t: "session" } & Pick<Header, "agent" | "session" | "model">)
  | { t: "title"; title: string };

// What the history shows of one conversation.
export type Summary = { file: string; title: string; updated: number; agent: string; model: string; questions: number };
const TITLE_CHARS = 52;

const STREAMED = new Set(["agent_message_chunk", "agent_thought_chunk", "user_message_chunk"]);
const KEPT = new Set([...STREAMED, "tool_call", "tool_call_update", "plan"]);

export class Conversation {
  readonly file: string;
  // The turn being written: entries in the order they first appeared.
  private turn: { key: string; update: Record<string, unknown> }[] = [];

  constructor(file: string) { this.file = file; }

  prompt(content: ContentBlock[]): void { this.write({ t: "prompt", content }); }

  update(u: SessionUpdate): void {
    if (!KEPT.has(u.sessionUpdate)) return;                    // usage, commands...: not the conversation
    const last = this.turn[this.turn.length - 1];
    if (STREAMED.has(u.sessionUpdate)) {
      const text = textOf(u);
      if (last && last.key === u.sessionUpdate) (last.update.content as { text: string }).text += text;
      else this.turn.push({ key: u.sessionUpdate, update: { ...u, content: { type: "text", text } } });
      return;
    }
    if (u.sessionUpdate === "plan") {
      const at = this.turn.find((e) => e.key === "plan");
      if (at) at.update = { ...u }; else this.turn.push({ key: "plan", update: { ...u } });
      return;
    }
    const id = (u as { toolCallId: string }).toolCallId;
    const at = this.turn.find((e) => e.key === `tool:${id}`);
    const defined = Object.fromEntries(Object.entries(u).filter(([, v]) => v !== undefined && v !== null));
    if (Array.isArray(defined.content)) defined.content = defined.content.map(withoutPicture);
    if (at) at.update = { ...at.update, ...defined, sessionUpdate: "tool_call" };
    else this.turn.push({ key: `tool:${id}`, update: { ...defined, sessionUpdate: "tool_call" } });
  }

  end(reason: string): void {
    for (const e of this.turn) this.write({ t: "update", update: e.update as SessionUpdate });
    this.turn = [];
    this.write({ t: "stop", reason });
  }

  switched(h: Pick<Header, "agent" | "session" | "model">): void { this.write({ t: "session", ...h }); }

  rename(title: string): void { this.write({ t: "title", title: title.trim() }); }

  private write(line: Line): void { appendFileSync(this.file, JSON.stringify(line) + "\n", { mode: 0o600 }); }
}

// A picture a tool showed the agent (a screenshot it read) is not kept: the
// panel shows it as [image], and a job reading hundreds of screenshots made a
// 584 MB record that no longer loaded (2026-11-11).
function withoutPicture(c: { type: string; content?: { type: string } }): unknown {
  return c.type === "content" && c.content?.type === "image" ? { ...c, content: { ...c.content, data: "" } } : c;
}

function textOf(u: SessionUpdate): string {
  const c = (u as { content?: { type: string; text?: string } }).content;
  return c && c.type === "text" ? c.text ?? "" : "";
}

let seq = 0;

export class ConversationStore {
  private readonly root: string;
  constructor(root: string) { this.root = root; }

  private dir(cwd: string): string {
    return join(this.root, "conversations", createHash("sha256").update(cwd).digest("hex").slice(0, 16));
  }

  start(h: Header): Conversation {
    const dir = this.dir(h.cwd);
    mkdirSync(dir, { recursive: true, mode: 0o700 });
    chmodSync(dir, 0o700);
    // Time, then a counter: two conversations started in the same millisecond
    // still sort in the order they began.
    const file = join(dir, `${Date.now()}-${String(seq++).padStart(4, "0")}-${randomUUID().slice(0, 8)}.jsonl`);
    writeFileSync(file, JSON.stringify({ t: "header", v: 1, ...h, created: new Date().toISOString() }) + "\n", { mode: 0o600 });
    return new Conversation(file);
  }

  private files(cwd: string): string[] {
    const dir = this.dir(cwd);
    if (!existsSync(dir)) return [];
    return readdirSync(dir).filter((f) => f.endsWith(".jsonl")).sort().map((f) => join(dir, f));
  }

  // The project's last conversation, as the panel showed it.
  latest(cwd: string): Opened | undefined {
    const file = this.files(cwd).pop();
    return file ? this.read(file) : undefined;
  }

  // One conversation, as the panel showed it, with the agent session that
  // held it last (another may have taken over) and its title.
  read(file: string): Opened | undefined {
    let header: Header | undefined;
    let transcript: Transcript = [];
    let title = "";
    let questions = 0;
    for (const raw of lines(file)) {
      if (!raw.trim()) continue;
      let l: Line;
      try { l = JSON.parse(raw); } catch { continue; }           // a torn last line is skipped
      if (l.t === "header") header = { agent: l.agent, session: l.session, model: l.model, school: l.school, cwd: l.cwd };
      else if (l.t === "session" && header) header = { ...header, agent: l.agent, session: l.session, model: l.model };
      else if (l.t === "title") title = l.title;
      else if (l.t === "prompt") {
        const text = promptText(l.content);
        if (!questions++ && !title) title = firstLine(text);
        transcript = addUserPrompt(transcript, text, promptImages(l.content));
      } else if (l.t === "update") transcript = applyUpdate(transcript, l.update);
    }
    return header ? { header, transcript, title, questions, conversation: new Conversation(file) } : undefined;
  }

  // The project's conversations that hold at least one question, newest first.
  list(cwd: string): Summary[] {
    return this.files(cwd).map((file) => {
      const o = this.read(file);
      return o && o.questions ? { file, title: o.title, updated: statSync(file).mtimeMs, agent: o.header.agent,
        model: o.header.model, questions: o.questions } : undefined;
    }).filter((x): x is Summary => Boolean(x)).sort((a, b) => b.updated - a.updated || (a.file < b.file ? 1 : -1));
  }

  // Conversations not touched for `days` are deleted. Returns how many.
  prune(days: number, now = Date.now()): number {
    const base = join(this.root, "conversations");
    if (!existsSync(base)) return 0;
    let gone = 0;
    for (const d of readdirSync(base)) {
      for (const f of readdirSync(join(base, d))) {
        const p = join(base, d, f);
        if (now - statSync(p).mtimeMs > days * 86_400_000) { unlinkSync(p); gone++; }
      }
    }
    return gone;
  }
}

// A file's lines, read a chunk at a time: a record past Node's longest string
// (512 MB) still reads back.
function* lines(file: string): Generator<string> {
  const fd = openSync(file, "r");
  const buf = Buffer.alloc(1 << 20);
  let rest = Buffer.alloc(0);
  try {
    for (let n; (n = readSync(fd, buf, 0, buf.length, null)) > 0;) {
      let data = Buffer.concat([rest, buf.subarray(0, n)]);
      for (let i; (i = data.indexOf(10)) >= 0; data = data.subarray(i + 1)) yield data.subarray(0, i).toString("utf8");
      rest = Buffer.from(data);
    }
    if (rest.length) yield rest.toString("utf8");
  } finally { closeSync(fd); }
}

export type Opened = { header: Header; transcript: Transcript; title: string; questions: number; conversation: Conversation };

function firstLine(text: string): string {
  const line = text.trim().split("\n")[0].trim();
  if (line.length <= TITLE_CHARS) return line;
  return line.slice(0, TITLE_CHARS).replace(/\s+\S*$/, "") + "…";
}

function promptText(content: ContentBlock[]): string {
  return content.filter((b) => b.type === "text").map((b) => (b as { text: string }).text).join("\n");
}

function promptImages(content: ContentBlock[]): string[] {
  return content.filter((b) => b.type === "image").map((b) => {
    const i = b as { mimeType: string; data: string };
    return `data:${i.mimeType};base64,${i.data}`;
  });
}

// The conversation so far, for an agent that was not part of it: the most
// recent turns kept whole, within `maxChars`, older ones marked as cut.
export function condensed(t: Transcript, maxChars: number): string {
  const parts = t.filter((e): e is Extract<Entry, { kind: "user" | "agent" }> => e.kind === "user" || e.kind === "agent")
    .map((e) => `${e.kind === "user" ? "Student" : "Assistant"}: ${e.text.trim()}`);
  const kept: string[] = [];
  let size = 0;
  const marker = "[…]";
  for (let i = parts.length - 1; i >= 0; i--) {
    const add = parts[i].length + (kept.length ? 2 : 0);
    const room = i > 0 ? maxChars - marker.length - 2 : maxChars;
    if (size + add > room) break;
    kept.unshift(parts[i]);
    size += add;
  }
  if (kept.length < parts.length) kept.unshift(marker);
  return kept.join("\n\n");
}
