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
//     {"t":"name","name":"..."}             the session's name (see below)
//
// A SESSION NAME (owner, 2026-11-12; architect 6e5893) is the conversation's
// key for what lives outside the record: its run directory
// <state>/sessions/<name>/ and, there, session.json for monitoring pages.
// A slug, claimed by creating that directory, written once (the header of a
// new record, a {"t":"name"} line for an older one), never rewritten. Several
// records may carry one name: they are one session.
//
// Compact: streamed chunks are joined into one message, a tool is written in
// its final state. Private: folder 0700, files 0600 (a shared GPU machine
// holds many students), never in the project (it may be shared or in git),
// never synced. Pruned after a retention.
import { createHash, randomUUID } from "node:crypto";
import { appendFileSync, chmodSync, closeSync, existsSync, mkdirSync, openSync, readdirSync, readFileSync, readSync, realpathSync, renameSync, statSync, unlinkSync, writeFileSync } from "node:fs";
import { basename, join } from "node:path";
import type { ContentBlock, SessionUpdate } from "@agentclientprotocol/sdk";
import { addUserPrompt, applyUpdate, type Entry, type Transcript } from "./transcript.ts";

// Where conversations, sessions and the agents' own files live. One rule,
// XDG (owner, 2026-11-12: "use the .local as behaviour"):
//   $XDG_STATE_HOME/<name>, i.e. ~/.local/state/<name>
// where <name> is the variant's (stateName; gateka by default). No dot-folder
// in the home. GATEKA_STATE_HOME, then the person's own setting
// (<prefix>.stateDirectory, an absolute or ~ path), come first.
export function stateRoot(env: Record<string, string | undefined>, home: string,
                          chosen: { setting?: string; name?: string } = {}): string {
  if (env.GATEKA_STATE_HOME) return env.GATEKA_STATE_HOME;
  const d = chosen.setting?.trim() ?? "";
  if (d.startsWith("/")) return d;
  if (d === "~" || d.startsWith("~/")) return join(home, d.slice(1));
  return join(env.XDG_STATE_HOME || join(home, ".local", "state"), chosen.name || "gateka");
}

export type Header = { agent: string; session: string; model: string; school: string; cwd: string; name?: string };
type Line =
  | ({ t: "header"; v: 1; created: string } & Header)
  | { t: "prompt"; content: ContentBlock[] }
  | { t: "update"; update: SessionUpdate }
  | { t: "stop"; reason: string }
  | ({ t: "session" } & Pick<Header, "agent" | "session" | "model">)
  | { t: "title"; title: string }
  | { t: "name"; name: string };

// What the history shows of one conversation.
// fresh: prepared with its first request, which no agent has run yet.
export type Summary = { file: string; title: string; name: string; fresh: boolean; updated: number; agent: string; model: string; questions: number };

// What a monitoring page reads of a session (its run directory's session.json).
export type Status = { name: string; title: string; cwd: string; agent: string; model: string;
  state: "working" | "waiting" | "idle"; since: number | null; last: number | null; tool: string;
  questions: number; updated: number; record: string };

// A session's page: a file to show, or (url) the address of a served page.
export type Page = { name: string; file: string; updated: number; url?: string };

// Pages a session's tab links at most.
const RENDERS_SHOWN = 12;

// A name fit for a directory: lowercase letters, digits, dots and dashes.
const NAME_CHARS = 40;
export function slug(text: string): string {
  const s = text.normalize("NFKD").replace(/[\u0300-\u036f]/g, "").toLowerCase()
    .replace(/[^a-z0-9.]+/g, "-").replace(/\.{2,}/g, ".").replace(/^[-.]+|[-.]+$/g, "").slice(0, NAME_CHARS).replace(/[-.]+$/, "");
  return s || "session";
}
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

  named(name: string): void { this.write({ t: "name", name }); }

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

  // Every record of the state folder, oldest first (file names begin with
  // their time), whatever folder holds it.
  private all(): string[] {
    const base = join(this.root, "conversations");
    if (!existsSync(base)) return [];
    const out: string[] = [];
    for (const d of readdirSync(base)) {
      let names: string[];
      try { names = readdirSync(join(base, d)); } catch { continue; }
      for (const f of names) if (f.endsWith(".jsonl")) out.push(join(base, d, f));
    }
    return out.sort((a, b) => (basename(a) < basename(b) ? -1 : basename(a) > basename(b) ? 1 : 0));
  }

  // A project's records: those whose header names its folder, wherever they
  // are - a record another tool seeded sits in a folder of its own naming.
  private readonly heads = new Map<string, { mtime: number; cwd: string }>();
  private files(cwd: string): string[] {
    const here = real(cwd);
    return this.all().filter((f) => {
      let mtime = 0;
      try { mtime = statSync(f).mtimeMs; } catch { return false; }
      let h = this.heads.get(f);
      if (!h || h.mtime !== mtime) { h = { mtime, cwd: real(headerOf(f)?.cwd ?? "") }; this.heads.set(f, h); }
      return h.cwd === here;
    });
  }

  // The session's name: its header's, else the one written in the record,
  // else claimed now from its title and written once. A name is never
  // rewritten (architect 6e5893): it is the key of the run directory.
  name(file: string): string {
    const o = this.read(file);
    if (!o) return "";
    if (o.name) { this.join(o.name); return o.name; }
    const name = this.reserve(o.title);
    o.conversation.named(name);
    return name;
  }

  // Renamed by the person: the title. The name stays.
  rename(file: string, title: string): string {
    const o = this.read(file);
    if (!o) return "";
    if (title.trim()) o.conversation.rename(title);
    return o.name || this.name(file);
  }

  // A name for a conversation about to start, from its first question,
  // CLAIMED by creating its run directory: creating a directory succeeds for
  // one caller only, so two windows asking for the same name get two (a scan
  // of the records would race, and forget names whose records were pruned).
  reserve(title: string): string {
    const base = join(this.root, "sessions");
    mkdirSync(base, { recursive: true, mode: 0o700 });
    const wanted = slug(firstLine(title));
    for (let n = 1; ; n++) {
      const name = n === 1 ? wanted : `${wanted.slice(0, NAME_CHARS - String(n).length - 1)}-${n}`;
      try { mkdirSync(join(base, name), { mode: 0o700 }); return name; }
      catch (e) { if ((e as NodeJS.ErrnoException).code !== "EEXIST") throw e; }
    }
  }

  // A record that carries a name belongs to that session: its run directory
  // is made if it is not there, never claimed again under another name.
  private join(name: string): void {
    mkdirSync(this.sessionDir(name), { recursive: true, mode: 0o700 });
  }

  // Where a session's own files live: tools, launchers, notes, session.json.
  sessionDir(name: string): string { return join(this.root, "sessions", slug(name)); }

  // What the session shows: pages its agent or its tools write. The code that
  // makes them is the session's too (<run directory>/tools/), never product
  // code (owner, 2026-11-12).
  rendersDir(name: string): string { return join(this.sessionDir(name), "renders"); }

  // The session's pages, newest first: the html files of its renders folder,
  // and its SERVED pages - <name>.url, a file whose first line is the address
  // of a page something serves (a Streamlit or marimo app, a monitor).
  renders(name: string): Page[] {
    const dir = this.rendersDir(name);
    let names: string[];
    try { names = readdirSync(dir); } catch { return []; }
    return names.map((f): Page | undefined => {
      const file = join(dir, f);
      try {
        const st = statSync(file);
        if (!st.isFile()) return undefined;
        if (/\.html?$/i.test(f)) return { name: f, file, updated: st.mtimeMs };
        if (!/\.url$/i.test(f) || st.size > 4096) return undefined;
        const url = readFileSync(file, "utf8").split("\n")[0].trim();
        return /^https?:\/\/[^\s"<>]+$/.test(url) ? { name: f.replace(/\.url$/i, ""), file, updated: st.mtimeMs, url } : undefined;
      } catch { return undefined; }
    }).filter((x): x is Page => Boolean(x))
      .sort((a, b) => b.updated - a.updated || (a.name < b.name ? -1 : 1)).slice(0, RENDERS_SHOWN);
  }

  // The session's status, for monitoring pages: whole or not at all.
  writeStatus(name: string, status: Status): void {
    const dir = this.sessionDir(name);
    this.join(name);
    const tmp = join(dir, `.session.json.${process.pid}`);
    writeFileSync(tmp, JSON.stringify(status, null, 1) + "\n", { mode: 0o600 });
    renameSync(tmp, join(dir, "session.json"));
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
    let name = "";
    let questions = 0;
    let pending = false;      // its last request has no answer and no end
    let started = false;      // an agent has answered something in it
    for (const raw of lines(file)) {
      if (!raw.trim()) continue;
      let l: Line;
      try { l = JSON.parse(raw); } catch { continue; }           // a torn last line is skipped
      if (l.t === "header") {
        header = { agent: l.agent, session: l.session, model: l.model, school: l.school, cwd: l.cwd,
          ...(typeof l.name === "string" && l.name ? { name: slug(l.name) } : {}) };
        name = header.name ?? "";
      } else if (l.t === "name") name = slug(l.name);
      else if (l.t === "session" && header) header = { ...header, agent: l.agent, session: l.session, model: l.model };
      else if (l.t === "title") title = l.title;
      else if (l.t === "prompt") {
        const text = promptText(l.content);
        if (!questions++ && !title) title = firstLine(text);
        transcript = addUserPrompt(transcript, text, promptImages(l.content));
        pending = true;
      } else if (l.t === "update") { transcript = applyUpdate(transcript, l.update); pending = false; started = true; }
      else if (l.t === "stop") { pending = false; started = true; }
    }
    return header ? { header, transcript, title, name, questions, pending, started, conversation: new Conversation(file) } : undefined;
  }

  // The project's conversations that hold at least one question, newest first.
  list(cwd: string): Summary[] {
    return this.files(cwd).map((file) => {
      const o = this.read(file);
      return o && o.questions ? { file, title: o.title, name: o.name, fresh: o.pending && !o.started, updated: statSync(file).mtimeMs, agent: o.header.agent,
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

export type Opened = { header: Header; transcript: Transcript; title: string; name: string; questions: number;
  pending: boolean; started: boolean; conversation: Conversation };

// A folder as the disk knows it (a link and its target are one project).
function real(path: string): string {
  if (!path) return "";
  try { return realpathSync(path); } catch { return path; }
}

// A record's first line, read alone: which project it belongs to.
function headerOf(file: string): { cwd?: string } | undefined {
  try {
    for (const raw of lines(file)) {
      const l = JSON.parse(raw);
      return l?.t === "header" ? l : undefined;
    }
  } catch { /* unreadable: not ours */ }
  return undefined;
}

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
