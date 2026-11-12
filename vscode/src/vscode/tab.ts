// One conversation of the panel: its agent session, its messages, its record
// (ADR-0223). Each tab runs on its own, so a long job keeps going in one tab
// while the student asks something in another (owner, 2026-11-12).
import * as vscode from "vscode";
import type { RequestPermissionOutcome, RequestPermissionRequest, SessionUpdate } from "@agentclientprotocol/sdk";
import { AgentSession } from "../core/acpSession.ts";
import { agentHome, launchFor, type AgentSpec } from "../core/agents.ts";
import { mkdirSync } from "node:fs";
import { MESSAGES, Said, t, type Lang, type MessageKey } from "../core/i18n.ts";
import type { Key } from "../core/keys.ts";
import { addNotice, addUserPrompt, applyUpdate, runningTool, type Transcript } from "../core/transcript.ts";
import { condensed, type Conversation, type ConversationStore, type Opened, type Status } from "../core/conversationStore.ts";
import type { KeySource } from "./credentials.ts";
import { readTextFile, writeTextFile } from "./editorHost.ts";

export type Pasted = { mimeType: string; data: string };
export type Ask = { id: number; title: string; options: { id: string; name: string; kind: string }[] };

// What a tab takes from the panel that holds it: the student's choices and
// credentials are the panel's, shared by every tab.
export interface TabHost {
  readonly ctx: vscode.ExtensionContext;
  readonly creds: KeySource;
  readonly log: vscode.OutputChannel;
  readonly lang: Lang;
  readonly store: ConversationStore;
  readonly schoolId: string;
  readonly stateDir: string;
  // The variant's title (BulkHours IPSA, MaQI), for the agent's persona.
  readonly brand: string;
  readonly idleMs: number;
  // The agent and model a tab asks for, or the panel's choice for a tab
  // that has asked for none yet.
  agent(key: Key | undefined, wanted?: string): AgentSpec;
  model(key: Key | undefined, wanted?: string): string;
  vision(key: Key): string[];
  spent(): number | null;
  askId(): number;
  // Something the panel shows changed in this tab.
  changed(tab: Tab): void;
  // A turn is running (each minute) or has ended: the budget is read again.
  turnTick(): void;
  turnEnded(): void;
}

// What may go into a prompt from a paste: pictures, nothing else.
const IMAGE_TYPES = new Set(["image/png", "image/jpeg", "image/gif", "image/webp"]);
// How much of an earlier conversation a new agent is handed.
const PRIME_CHARS = 12_000;

let tabs = 0;

export class Tab {
  readonly id = ++tabs;
  title = "";
  // A request written in the record and never run (a conversation another
  // tool prepared): Start runs it as it is.
  pending = "";
  // The session's name (conversationStore): the key of its run directory
  // and of its status for monitoring pages. Empty until its first question.
  name = "";
  transcript: Transcript = [];
  busy = false;
  starting = false;
  usage: { used: number; size: number } | null = null;
  // Slash commands the agent announced (ACP available_commands_update).
  // "/compact" is sent only to an agent that offers it: dsh does not, and
  // took it for a question (owner, 2026-11-10).
  commands: string[] = [];
  // The turn in progress: when it began, the agent's last sign of life, the
  // tool it is running, and the spend when it began (owner, 2026-11-10: an
  // hour of sub-agents showed only "is thinking", and cost $26).
  activity: { since: number; last: number; tool: string; spentAtStart: number | null } | null = null;
  // The record of this conversation (ADR-0223).
  conversation: Conversation | undefined;
  // This conversation's agent and model, fixed when its agent starts or its
  // record is reopened: choosing in the menu changes the shown tab only.
  choice: { agent: string; model?: string } | undefined;
  private session: AgentSession | undefined;
  private launchKey = "";
  // Stop pressed while the agent was still starting: honoured once it is up.
  private stopAsked = false;
  // Whether the next prompt must hand the conversation so far to an agent
  // that was not part of it.
  private prime = false;
  // A conversation whose agent was paused: resumed at the next message if the
  // same agent and model are still chosen.
  private paused: { sessionId: string; launchKey: string } | undefined;
  private readonly asks = new Map<number, { ask: Ask; resolve: (o: RequestPermissionOutcome) => void }>();
  private activityTimer: ReturnType<typeof setInterval> | undefined;
  private idleTimer: ReturnType<typeof setTimeout> | undefined;
  private readonly host: TabHost;

  constructor(host: TabHost) { this.host = host; }

  // Nothing said in it yet: a new chat may reuse it.
  get empty(): boolean { return !this.transcript.length && !this.conversation; }

  get asking(): Ask[] { return [...this.asks.values()].map((a) => a.ask); }

  // Becomes the conversation the record holds: its messages, and its agent
  // session resumed at the next message (or handed over).
  take(o: Opened): void {
    this.forget();
    this.transcript = o.transcript;
    this.conversation = o.conversation;
    this.paused = { sessionId: o.header.session, launchKey: `${o.header.agent}|${o.header.model}` };
    this.prime = o.transcript.length > 0;
    this.title = o.title;
    this.name = o.name || this.host.store.name(o.conversation.file);
    const last = o.transcript[o.transcript.length - 1];
    this.pending = o.pending && !o.started && last?.kind === "user" ? last.text : "";
    this.choice = { agent: o.header.agent, model: o.header.model };
  }

  agentSpec(key: Key | undefined): AgentSpec { return this.host.agent(key, this.choice?.agent); }

  model(key: Key | undefined): string { return this.host.model(key, this.choice?.model); }

  // Clear: a new conversation in this tab (the old one stays in the history).
  clear(): void {
    this.forget();
    this.conversation = undefined;
    this.prime = false;
    this.title = "";
    this.name = "";
    this.pending = "";
    this.transcript = [];
    this.usage = null;
    this.choice = undefined;
  }

  rename(title: string): void {
    if (!this.conversation || !title.trim()) return;
    this.name = this.host.store.rename(this.conversation.file, title);
    this.title = title.trim();
  }

  // What a monitoring page reads of this session (its run directory's
  // session.json), or nothing before its first question.
  status(key: Key | undefined): Status | undefined {
    if (!this.name || !this.conversation) return undefined;
    const a = this.activity;
    return { name: this.name, title: this.title, cwd: vscode.workspace.workspaceFolders?.[0]?.uri.fsPath ?? "",
      agent: this.choice?.agent ?? "", model: this.choice?.model ?? this.model(key),
      state: this.asks.size ? "waiting" : this.busy ? "working" : "idle",
      since: a?.since ?? null, last: a?.last ?? null, tool: a?.tool ?? "",
      questions: this.transcript.filter((e) => e.kind === "user").length, updated: Date.now(), record: this.conversation.file };
  }

  async stop(): Promise<void> {
    if (!this.busy) return;
    this.stopAsked = true;
    await this.session?.cancel();
  }

  // Start: the request the record already holds is run, not asked again.
  async runPending(): Promise<void> {
    if (this.pending) await this.send(this.pending, [], true);
  }

  async send(text: string, pasted: Pasted[] = [], written = false): Promise<void> {
    if (this.busy || !text.trim()) return;
    this.pending = "";
    this.busy = true;
    this.stopAsked = false;
    this.activity = { since: Date.now(), last: Date.now(), tool: "", spentAtStart: this.host.spent() };
    // During a long turn the budget is read again every minute (LiteLLM
    // writes spend in batches of about a minute).
    clearInterval(this.activityTimer);
    this.activityTimer = setInterval(() => this.host.turnTick(), 60_000);
    this.activityTimer.unref?.();
    const images = pasted.filter((i) => IMAGE_TYPES.has(i.mimeType) && /^[A-Za-z0-9+/=]+$/.test(i.data));
    if (!written) this.transcript = addUserPrompt(this.transcript, text, images.map((i) => `data:${i.mimeType};base64,${i.data}`));
    this.host.changed(this);
    try {
      // A new conversation is named from its first question, before its
      // agent starts: the agent is told its name and its run directory.
      if (!this.name) this.name = this.host.store.reserve(text);
      const session = await this.ensureSession();
      if (this.stopAsked) {
        this.transcript = addNotice(this.transcript, t(this.host.lang, "stoppedBeforeStart"));
        return;
      }
      if (images.length && !session.acceptsImages) this.transcript = addNotice(this.transcript, t(this.host.lang, "noImages"));
      // An agent that was not part of the conversation is handed it first.
      const earlier = this.prime && !session.resumed ? condensed(this.transcript.slice(0, -1), PRIME_CHARS) : "";
      const preface = earlier ? `The conversation so far (the student may have asked another assistant):\n\n${earlier}` : "";
      this.prime = false;
      if (!written) this.conversation?.prompt([{ type: "text", text }, ...images.map((i) => ({ type: "image" as const, mimeType: i.mimeType, data: i.data }))]);
      if (this.conversation && !this.title) this.title = this.host.store.read(this.conversation.file)?.title ?? "";
      let stop = "error";
      try {
        stop = await session.prompt(text, activeFileContext(), images, preface, this.sessionNote(session));
      } finally {
        this.conversation?.end(stop);
      }
      if (stop !== "end_turn") this.transcript = addNotice(this.transcript, t(this.host.lang, "stopped", { reason: reason(this.host.lang, stop) }));
    } finally {
      this.busy = false;
      this.activity = null;
      clearInterval(this.activityTimer);
      this.host.changed(this);
      this.host.turnEnded();
      this.armIdle();
    }
  }

  // Compaction for an agent that has no /compact of its own (dsh over ACP):
  // its session is let go - not resumed - and the next message starts a fresh
  // one, handed the conversation condensed (recent exchanges whole), as when
  // switching model. The record and the panel keep everything.
  compact(): void {
    if (this.busy || !this.transcript.length) return;
    this.forget();
    this.prime = true;
    this.usage = null;
    this.transcript = addNotice(this.transcript, t(this.host.lang, "compacted"));
  }

  // « Redémarrer l'assistant »: a new agent process at the next message, the
  // conversation resumed or handed over.
  restart(): void {
    if (this.session?.canResume) this.paused = { sessionId: this.session.sessionId, launchKey: this.launchKey };
    else if (this.session) this.prime = this.transcript.length > 0;
    this.busy = false;
    this.endSession();
  }

  // A sign-out, a closed tab: nothing to resume.
  forget(): void {
    clearTimeout(this.idleTimer);
    this.paused = undefined;
    this.endSession();
  }

  dispose(): void {
    clearInterval(this.activityTimer);
    this.forget();
  }

  // An error the turn did not catch: said in the conversation.
  failed(message: string): void {
    this.transcript = addNotice(this.transcript, t(this.host.lang, "error", { message }));
    this.busy = false;
  }

  answer(id: number, optionId: string | null): boolean {
    const a = this.asks.get(id);
    if (!a) return false;
    this.asks.delete(id);
    a.resolve(optionId ? { outcome: "selected", optionId } : { outcome: "cancelled" });
    return true;
  }

  // The session's rules, told once to each agent that joins it (not shown in
  // the conversation): where its run directory is and what goes there.
  private told: AgentSession | undefined;
  private sessionNote(session: AgentSession): string {
    if (this.told === session || session.resumed || !this.name) return "";
    this.told = session;
    const dir = this.host.store.sessionDir(this.name);
    return `[session "${this.name}"] Run directory, outside the project: ${dir}. `
      + `What serves this session only goes there, never in the project: code that only displays or renders results in ${dir}/tools/, `
      + `pages to show the person as .html files in ${dir}/renders/ (the panel links each one). Product code stays in the project.`;
  }

  private armIdle(): void {
    clearTimeout(this.idleTimer);
    if (!this.session?.canResume) return;
    this.idleTimer = setTimeout(() => this.pause(), this.host.idleMs);
    this.idleTimer.unref?.();
  }

  // An agent idle for a while is stopped to free its memory, and resumed at
  // the next message.
  private pause(): void {
    if (this.busy || !this.session) return;
    this.paused = { sessionId: this.session.sessionId, launchKey: this.launchKey };
    this.endSession();
    this.transcript = addNotice(this.transcript, t(this.host.lang, "agentPaused"));
    this.host.changed(this);
  }

  private record(key: Key, model: string, folder: string): void {
    const s = this.session!;
    const who = { agent: this.agentSpec(key).id, session: s.sessionId, model };
    try {
      if (!this.conversation) this.conversation = this.host.store.start({ ...who, school: this.host.schoolId, cwd: folder, name: this.name });
      else if (!s.resumed) this.conversation.switched(who);
    } catch (e) {
      this.host.log.append(`conversation record not written: ${(e as Error).message}\n`);
    }
  }

  private async ensureSession(): Promise<AgentSession> {
    const { key, renewed } = await this.host.creds.currentKey();
    const model = this.model(key);
    const spec = this.agentSpec(key);
    const launchKey = `${spec.id}|${model}`;
    this.choice = { agent: spec.id, model };
    if (this.session && !renewed && launchKey === this.launchKey) return this.session;
    this.letGo(renewed);
    const folder = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!folder) throw new Said("openFolder");
    const launch = launchFor(spec, {
      baseUrl: key.baseUrl, apiKey: key.apiKey, model, extensionPath: this.host.ctx.extensionPath,
      state: this.host.stateDir,
    });
    // Every agent is told where the state folder and its own home are; the
    // home is made when its spec uses it (${agentHome}).
    const home = agentHome(this.host.stateDir, spec.id);
    if ([...launch.args, ...Object.values(launch.env)].some((v) => v.includes(home))) mkdirSync(home, { recursive: true, mode: 0o700 });
    launch.env.GATEKA_STATE_HOME = this.host.stateDir;
    launch.env.GATEKA_AGENT_HOME = home;
    launch.env.BULKHOURS_MODEL = model;
    launch.env.BULKHOURS_BRAND = this.host.brand;
    // The session's own place for what it produces (tools, runs, notes).
    launch.env.GATEKA_SESSION_NAME = this.name;
    launch.env.GATEKA_SESSION_DIR = this.host.store.sessionDir(this.name);
    // Where its pages go: the panel links every .html found there.
    launch.env.GATEKA_SESSION_RENDERS = this.host.store.rendersDir(this.name);
    mkdirSync(launch.env.GATEKA_SESSION_RENDERS, { recursive: true, mode: 0o700 });
    launch.env.BULKHOURS_MODELS = key.models.join(",");
    launch.env.BULKHOURS_VISION_MODELS = this.host.vision(key).join(",");
    const resume = this.paused?.launchKey === launchKey ? this.paused.sessionId : undefined;
    if (this.paused && !resume) this.prime = this.transcript.length > 0;
    this.paused = undefined;
    // The first start on a machine can download the agent (minutes, measured
    // 2026-11-10): the panel says so instead of staying silent.
    this.starting = true;
    this.host.changed(this);
    try {
      this.session = await AgentSession.start(launch, folder, {
        readTextFile, writeTextFile,
        askPermission: (req) => this.ask(req),
        onUpdate: (u) => this.onUpdate(u),
        log: (line) => this.host.log.append(line),
      }, this.host.ctx.extension.packageJSON.version, resume);
      this.launchKey = launchKey;
      this.record(key, model, folder);
    } finally {
      this.starting = false;
    }
    return this.session;
  }

  // The session in place is let go before another starts.
  private letGo(renewed: boolean): void {
    if (this.session && renewed) {
      // A renewed key restarts the agent (it reads its key once): it resumes
      // the conversation when it can, as after a pause.
      this.transcript = addNotice(this.transcript, t(this.host.lang, "keyRenewed"));
      if (this.session.canResume) this.paused = { sessionId: this.session.sessionId, launchKey: this.launchKey };
    } else if (this.session) {
      // Another agent or model was chosen: it is handed the conversation.
      this.paused = undefined;
      this.prime = this.transcript.length > 0;
    }
    this.endSession();
  }

  private onUpdate(u: SessionUpdate): void {
    if (this.activity) {
      this.activity.last = Date.now();
      this.activity.tool = runningTool(u, this.activity.tool);
    }
    if (u.sessionUpdate === "usage_update") this.usage = { used: u.used, size: u.size };
    if (u.sessionUpdate === "available_commands_update") this.commands = u.availableCommands.map((c) => c.name);
    this.conversation?.update(u);
    this.transcript = applyUpdate(this.transcript, u);
    this.host.changed(this);
  }

  private ask(req: RequestPermissionRequest): Promise<RequestPermissionOutcome> {
    const id = this.host.askId();
    const ask: Ask = { id, title: req.toolCall.title ?? t(this.host.lang, "agentWantsToAct"),
      options: req.options.map((o) => ({ id: o.optionId, name: o.name, kind: o.kind })) };
    return new Promise((resolve) => {
      this.asks.set(id, { ask, resolve });
      this.host.changed(this);
    });
  }

  private endSession(): void {
    this.commands = [];
    for (const a of this.asks.values()) a.resolve({ outcome: "cancelled" });
    this.asks.clear();
    this.session?.dispose();
    this.session = undefined;
  }
}

function activeFileContext(): { uri: string; name: string }[] {
  const doc = vscode.window.activeTextEditor?.document;
  if (!doc || doc.uri.scheme !== "file") return [];
  return [{ uri: doc.uri.toString(), name: vscode.workspace.asRelativePath(doc.uri) }];
}

function reason(lang: Lang, stop: string): string {
  const key = `reason_${stop}`;
  return key in MESSAGES[lang] ? t(lang, key as MessageKey) : stop.replace(/_/g, " ");
}
