// The chat panel: conversations as tabs (src/vscode/tab.ts), each with its
// own agent session; the shown one is drawn, permission requests included.
import * as vscode from "vscode";
import { parseAgents, type AgentSpec } from "../core/agents.ts";
import { chooseAgent, chooseModel } from "../core/choices.ts";
import { MESSAGES, sayError, t, type Lang, type MessageKey } from "../core/i18n.ts";
import type { Key } from "../core/keys.ts";
import type { School } from "../core/school.ts";
import { ConversationStore, stateRoot, type Opened, type Summary } from "../core/conversationStore.ts";
import { homedir } from "node:os";
import type { KeySource } from "./credentials.ts";
import { Tab, type Pasted, type TabHost } from "./tab.ts";
import { avatarData, type FileRef } from "../core/fileLinks.ts";
import { userInfo } from "node:os";
import { existsSync } from "node:fs";
import { isAbsolute, join } from "node:path";

type FromPanel =
  | { type: "ready" } | { type: "signIn" } | { type: "cancel" } | { type: "newChat" }
  | { type: "send"; text: string; images?: Pasted[] } | { type: "model"; model: string }
  | { type: "compact" } | { type: "clear" } | { type: "pickAgent" }
  | { type: "choose"; agent: string; model?: string }
  | { type: "permission"; id: number; optionId: string | null }
  | { type: "tab"; id: number } | { type: "closeTab"; id: number } | { type: "rename"; id: number; title: string }
  | { type: "openFile"; path: string; line?: number; endLine?: number } | { type: "links" }
  | { type: "openConversation"; file: string };

type Credits = { spent: number; budget: number; currency: "USD" | "EUR" };
// LiteLLM writes spend in batches (about a minute, measured 2026-11-10): the
// meter is read after a turn, then once more when the batch has landed.
const SPEND_LANDS_MS = 75_000;
// An agent idle this long is stopped to free its memory (265 MB for dsh, about
// 500 MB for Claude Code, measured 2026-11-10; a shared GPU machine holds one
// per student) - only when it saves its sessions and can resume them.
const IDLE_MS = 15 * 60_000;
// Conversations kept this long after their last turn (ADR-0223).
const KEEP_DAYS = 90;
// The open tabs of a project, as conversation records, back after a reload:
// pointers only, the record stays the one source (ADR-0223).
const OPEN_TABS = "bulkhours.tabs";
// Agents working at once: each is a process (265 MB for dsh, measured
// 2026-11-10) on a machine many students share (architect bfd92a).
const MAX_RUNNING = 3;
// Conversations an empty tab presents.
const RECENT = 6;

export class ChatView implements vscode.WebviewViewProvider, vscode.Disposable, TabHost {
  private view: vscode.WebviewView | undefined;
  // The conversations open as tabs; one is shown, all of them run.
  private tabs: Tab[] = [];
  private active: Tab;
  private nextAsk = 1;
  readonly ctx: vscode.ExtensionContext;
  private readonly school: School;
  readonly creds: KeySource;
  readonly log: vscode.OutputChannel;
  readonly lang: Lang;
  private readonly meter: (c: Credits | undefined) => void;
  private credits: Credits | undefined;
  private spendTimer: ReturnType<typeof setTimeout> | undefined;
  readonly idleMs: number;
  // The variant's state folder (stateRoot): conversations and agent files.
  readonly stateDir: string;
  readonly store: ConversationStore;
  private restored = false;
  // What the tab strip showed last: a busy tab behind the shown one redraws
  // the strip only when this changes, never the whole conversation.
  private strip = "";

  constructor(ctx: vscode.ExtensionContext, school: School, creds: KeySource, log: vscode.OutputChannel,
              lang: Lang = "en", meter: (c: Credits | undefined) => void = () => {}, idleMs = IDLE_MS) {
    this.ctx = ctx;
    this.school = school;
    this.creds = creds;
    this.log = log;
    this.lang = lang;
    this.meter = meter;
    this.idleMs = idleMs;
    this.stateDir = stateRoot(process.env, homedir(), {
      setting: vscode.workspace.getConfiguration(school.prefix).get<string>("stateDirectory"), variant: school.stateDir });
    this.store = new ConversationStore(this.stateDir);
    this.active = this.addTab();
    creds.onDidChange(() => { this.tabs.forEach((t) => t.forget()); void this.render(); });
  }

  get schoolId(): string { return this.school.id; }

  get brand(): string { return this.school.title; }

  resolveWebviewView(view: vscode.WebviewView): void {
    this.view = view;
    const media = vscode.Uri.joinPath(this.ctx.extensionUri, "media");
    view.webview.options = { enableScripts: true, localResourceRoots: [media] };
    view.webview.html = panelHtml(view.webview, media, this.school, this.lang);
    view.webview.onDidReceiveMessage((m: FromPanel) => this.onPanel(m).catch((e) => this.fail(e)));
  }

  // VS Code closing: no agent process outlives the editor.
  dispose(): void {
    clearTimeout(this.spendTimer);
    this.tabs.forEach((t) => t.dispose());
  }

  // + : a new conversation in a new tab (an empty tab is reused).
  newChat(): void {
    const empty = this.tabs.find((t) => t.empty && !t.busy);
    this.show(empty ?? this.addTab());
  }

  private addTab(): Tab {
    const tab = new Tab(this);
    this.tabs.push(tab);
    return tab;
  }

  private show(tab: Tab): void {
    this.active = tab;
    this.showTitle(tab.title);
    this.saveTabs();
    void this.render();
  }

  // A closed tab's agent stops; its conversation stays in the history.
  private async closeTab(tab: Tab): Promise<void> {
    if (!(await this.stopFirst(tab, "closeStops", "stopAndClose"))) return;
    const at = this.tabs.indexOf(tab);
    tab.dispose();
    this.tabs.splice(at, 1);
    if (!this.tabs.length) this.addTab();
    this.show(this.active === tab ? this.tabs[Math.min(at, this.tabs.length - 1)] : this.active);
  }

  private saveTabs(): void {
    const files = this.tabs.filter((t) => t.conversation).map((t) => t.conversation!.file);
    void this.ctx.workspaceState?.update(OPEN_TABS, { files, active: this.active.conversation?.file ?? "" });
  }

  // At the panel's first opening: the tabs open before the reload come back
  // (or the project's last conversation), each resumed at its next message.
  private restore(): void {
    if (this.restored) return;
    this.restored = true;
    try {
      this.store.prune(KEEP_DAYS);
      const folder = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
      if (!folder || !this.active.empty) return;
      const saved = this.ctx.workspaceState?.get<{ files: string[]; active: string }>(OPEN_TABS);
      const opened = saved?.files.length
        ? saved.files.map((f) => this.reopen(f))
        : [this.store.latest(folder)];
      for (const o of opened) {
        if (!o) continue;
        const tab = this.active.empty ? this.active : this.addTab();
        tab.take(o);
        if (!saved || o.conversation.file === saved.active) this.active = tab;
      }
      this.showTitle(this.active.title);
    } catch (e) {
      this.log.append(`conversation record unreadable: ${(e as Error).message}\n`);
    }
  }

  // A tab saved before the reload whose record is gone is dropped, and said.
  private reopen(file: string): Opened | undefined {
    try {
      const o = this.store.read(file);
      if (o) return o;
    } catch (e) {
      this.log.append(`tab not reopened, ${file}: ${(e as Error).message}\n`);
      return undefined;
    }
    this.log.append(`tab not reopened, its record is gone: ${file}\n`);
    return undefined;
  }

  // The project's conversations, newest first (the history).
  conversations(): Summary[] {
    const folder = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    try { return folder ? this.store.list(folder) : []; } catch { return []; }
  }

  // From the history: its tab if it is open, else a tab of its own.
  async open(file: string): Promise<void> {
    const open = this.tabs.find((t) => t.conversation?.file === file);
    if (open) return this.show(open);
    const o = this.store.read(file);
    if (!o) return;
    const tab = this.active.empty && !this.active.busy ? this.active : this.addTab();
    tab.take(o);
    this.show(tab);
  }

  async rename(title: string, tab = this.active): Promise<void> {
    tab.rename(title);
    if (tab === this.active) this.showTitle(tab.title);
    await this.render();
  }

  get title(): string { return this.active.title; }

  // From the editor: a file or a selection, into the chat box (not sent).
  addReference(text: string): void {
    void this.view?.webview.postMessage({ type: "insert", text });
    this.view?.show?.(true);
  }

  // The conversation's name, beside the panel's own (as Claude Code shows it).
  private showTitle(title: string): void {
    if (this.view) this.view.description = title;
  }

  // The key lives in memory only, so after a window reload the menu would
  // know no school model until the first message. Fetch it as the panel
  // opens; a failure here is shown at the first message, not now.
  private async warmKey(): Promise<void> {
    if (this.creds.known() || !(await this.creds.signedIn())) return;
    try { await this.creds.currentKey(); } catch { return; }
    await this.render();
  }

  // The person's avatar (the variant's address), once per window. Never
  // fails the panel: no picture, no avatar.
  private avatar: string | undefined;
  private async loadAvatar(): Promise<void> {
    if (this.avatar || !this.school.avatar) return;
    try {
      const r = await fetch(this.school.avatar.replace(/\$\{user\}/g, encodeURIComponent(userInfo().username)));
      if (r.status !== 200) return;
      this.avatar = avatarData(r.headers.get("content-type") ?? "", Buffer.from(await r.arrayBuffer()));
      await this.render();
    } catch { /* offline: no avatar */ }
  }

  // The budget meter, read from the key server. Never fails the panel.
  async refreshCredits(): Promise<void> {
    this.credits = await this.creds.credits();
    this.meter(this.credits);
    await this.render();
  }

  private async onPanel(m: FromPanel): Promise<void> {
    const tab = this.active;
    switch (m.type) {
      case "send": return this.send(tab, m.text, m.images ?? []);
      case "tab": case "closeTab": case "rename": return this.onStrip(m);
      case "openFile": return openFile(m);
      case "links": await vscode.commands.executeCommand(`${this.school.prefix}.links`); return;
      case "openConversation":
        // Only one the list offered: the page never names a file of its own.
        if (this.conversations().some((c) => c.file === m.file)) await this.open(m.file);
        return;
      case "ready": this.restore(); await this.render(); void this.loadAvatar(); await this.warmKey(); return this.refreshCredits();
      case "compact": return this.compact(tab);
      case "clear": return this.clear(tab);
      case "pickAgent": await vscode.commands.executeCommand(`${this.school.prefix}.pickAgent`); return;
      case "choose": return this.choose(m.agent, m.model);
      case "signIn": return this.creds.signIn();
      case "newChat": return this.newChat();
      case "cancel": return tab.stop();
      case "model": return this.choose("", m.model);
      case "permission":
        this.tabs.some((t) => t.answer(m.id, m.optionId));
        return this.render();
    }
  }

  // Compact: the agent's own /compact when it has one, else the tab's.
  private async compact(tab: Tab): Promise<void> {
    if (!(await this.stopFirst(tab, "compactStops", "stopAndCompact"))) return;
    if (tab.commands.includes("compact")) return tab.send("/compact");
    tab.compact();
    return this.render();
  }

  // Clear: a new conversation in the same tab.
  private async clear(tab: Tab): Promise<void> {
    if (!(await this.stopFirst(tab, "clearStops", "stopAndClear"))) return;
    tab.clear();
    this.show(tab);
  }

  private async send(tab: Tab, text: string, images: Pasted[]): Promise<void> {
    this.recentCache = undefined;
    if (!tab.busy && this.tabs.filter((x) => x.busy).length >= MAX_RUNNING) {
      tab.failed(t(this.lang, "tooManyRunning", { n: MAX_RUNNING }));
      return this.render();
    }
    const fresh = !tab.conversation;
    await tab.send(text, images);
    if (fresh && tab.conversation) this.saveTabs();
  }

  // The tab strip: show a tab, close it, rename it.
  private async onStrip(m: Extract<FromPanel, { type: "tab" | "closeTab" | "rename" }>): Promise<void> {
    const tab = this.tabs.find((x) => x.id === m.id);
    if (!tab) return;
    if (m.type === "tab") return this.show(tab);
    if (m.type === "closeTab") return this.closeTab(tab);
    return this.rename(m.title, tab);
  }

  // One menu: a school model (the school's agent on the school's credits)
  // or one of the student's own agents, such as Claude Code on their own
  // subscription. It changes the shown tab, whose next message starts the
  // agent chosen, handed the conversation so far; new tabs start with it.
  private async choose(agent: string, model?: string): Promise<void> {
    await vscode.workspace.getConfiguration(this.school.prefix).update("agent", agent, true);
    if (model) await this.ctx.globalState.update("bulkhours.model", model);
    this.active.choice = { agent, model: model ?? this.active.choice?.model };
    await this.render();
  }

  private agentChoices(key: Key | undefined): { id: string; label: string }[] {
    const extra = parseAgents(vscode.workspace.getConfiguration(this.school.prefix).get<unknown[]>("extraAgents") ?? []);
    return [...(key ? [{ id: "", label: key.agent.label }] : []), ...extra.map((a) => ({ id: a.id, label: a.label }))];
  }

  // The models that read images: the school's list, unless the student set
  // their own (bulkhours.imageModels), restricted to the models offered.
  vision(key: Key): string[] {
    const own = vscode.workspace.getConfiguration(this.school.prefix).get<unknown>("imageModels");
    const list = Array.isArray(own) && own.length ? own.filter((m): m is string => typeof m === "string") : key.modelVision;
    return key.models.filter((m) => list.includes(m));
  }

  model(key: Key | undefined, wanted = this.ctx.globalState.get<string>("bulkhours.model")): string {
    return chooseModel(wanted, key);
  }

  // The school's agent comes with the key; a student may pick one of their
  // own `bulkhours.extraAgents` instead.
  agent(key: Key | undefined, wanted?: string): AgentSpec {
    const cfg = vscode.workspace.getConfiguration(this.school.prefix);
    return chooseAgent(key, parseAgents(cfg.get<unknown[]>("extraAgents") ?? []), wanted ?? cfg.get<string>("agent") ?? "");
  }

  spent(): number | null { return this.credits?.spent ?? null; }

  askId(): number { return this.nextAsk++; }

  changed(tab: Tab): void {
    if (tab === this.active) { if (tab.title !== this.title || this.view?.description !== tab.title) this.showTitle(tab.title); void this.render(); }
    else if (this.stripOf() !== this.strip) void this.render();
  }

  turnTick(): void { void this.refreshCredits(); }

  turnEnded(): void {
    void this.refreshCredits();
    clearTimeout(this.spendTimer);
    this.spendTimer = setTimeout(() => void this.refreshCredits(), SPEND_LANDS_MS);
    this.spendTimer.unref?.();
  }

  // During a turn, Compact, Clear and closing the tab would end it: the
  // student says so first, then the turn is stopped and has ended before
  // they act.
  private async stopFirst(tab: Tab, question: MessageKey, yes: MessageKey): Promise<boolean> {
    if (!tab.busy) return true;
    const answer = await vscode.window.showWarningMessage(t(this.lang, question), { modal: true }, t(this.lang, yes));
    if (answer !== t(this.lang, yes)) return false;
    await tab.stop();
    for (let i = 0; i < 300 && tab.busy; i++) await new Promise((r) => setTimeout(r, 100));
    return !tab.busy;
  }

  // « Redémarrer l'assistant »: new agent processes (each conversation is
  // resumed, or handed over, at its next message) and a fresh panel page.
  // Only this extension restarts: VS Code's restartExtensionHost would restart
  // every extension of the window (owner, 2026-11-10).
  restart(): void {
    this.tabs.forEach((t) => t.restart());
    if (this.view) {
      const media = vscode.Uri.joinPath(this.ctx.extensionUri, "media");
      this.view.webview.html = panelHtml(this.view.webview, media, this.school, this.lang);
    }
    void this.render();
  }

  private fail(e: unknown): void {
    this.active.failed(sayError(this.lang, e));
    void this.render();
  }

  private stripOf(): string {
    return JSON.stringify(this.tabs.map((x) => ({ id: x.id, title: x.title, busy: x.busy, asking: x.asking.length > 0,
      named: Boolean(x.conversation) })));
  }

  // An empty tab presents the recent conversations (owner, 2026-11-12: "how
  // come you dont present my chats?"), as Claude Code's panel does. Reading
  // every record is not free: done for an empty tab only, at most every 30 s.
  private recentCache: { at: number; list: Summary[] } | undefined;
  private recent(): { file: string; title: string; updated: number; questions: number }[] {
    if (!this.recentCache || Date.now() - this.recentCache.at > 30_000) this.recentCache = { at: Date.now(), list: this.conversations() };
    return this.recentCache.list.slice(0, RECENT).map(({ file, title, updated, questions }) => ({ file, title, updated, questions }));
  }

  private async render(): Promise<void> {
    const key = this.creds.known();
    const tab = this.active;
    this.strip = this.stripOf();
    await this.view?.webview.postMessage({
      type: "state", transcript: tab.transcript, busy: tab.busy, starting: tab.starting,
      signedIn: await this.creds.signedIn(), interactive: this.creds.interactive, model: tab.model(key), models: key?.models ?? [],
      agent: key ? safeLabel(() => tab.agentSpec(key).label) : "",
      modelLabels: key?.modelLabels ?? {}, modelPrices: key?.modelPrices ?? {}, modelVision: key ? this.vision(key) : [],
      currency: key?.currency ?? "USD",
      agents: safeList(() => this.agentChoices(key)), agentId: key ? safeLabel(() => (tab.agentSpec(key) === key.agent ? "" : tab.agentSpec(key).id)) : "",
      credits: this.credits ?? null, usage: tab.usage, commands: tab.commands,
      activity: tab.busy ? tab.activity : null, asks: tab.asking,
      tabs: JSON.parse(this.strip), tab: tab.id,
      avatar: this.avatar ?? null, hasLinks: this.school.links.length > 0,
      recent: tab.empty ? this.recent() : [],
    });
  }
}

// From the chat: a path the agent wrote, opened in the editor at its lines.
// Relative paths are the workspace's; a file that does not exist opens nothing.
async function openFile(ref: FileRef): Promise<void> {
  const folder = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath ?? homedir();
  const full = isAbsolute(ref.path) ? ref.path : join(folder, ref.path);
  if (!existsSync(full)) {
    void vscode.window.showInformationMessage(`${ref.path}: not found in ${folder}`);
    return;
  }
  const uri = vscode.Uri.file(full);
  if (!ref.line || full.endsWith(".ipynb")) {
    await vscode.commands.executeCommand("vscode.open", uri);
    return;
  }
  const start = new vscode.Position(ref.line - 1, 0);
  const end = new vscode.Position((ref.endLine ?? ref.line) - 1, 0);
  await vscode.window.showTextDocument(uri, { selection: new vscode.Range(start, end), preview: false });
}

function safeList<T>(f: () => T[]): T[] {
  try { return f(); } catch { return []; }
}

function safeLabel(f: () => string): string {
  try { return f(); } catch (e) { return `(${(e as Error).message})`; }
}

// The panel's own words, sent once in the page as data (never as script).
const PANEL_WORDS: MessageKey[] = ["signIn", "emptyChat", "placeholder", "send", "stop", "model", "thinking", "output", "noChange", "startingAgent",
  "compact", "compactHint", "clear", "clearHint", "thinkingVerb", "budgetTitle", "contextTitle", "removeImage",
  "suggestExplain", "suggestBuild", "suggestFaster", "schoolModels", "yourAgents", "mic", "micWindows", "micMac", "seesImages", "lastActivity", "thisTurn",
  "newTab", "closeTab", "renameHint", "renameTab", "openInEditor", "linksTitle", "recentTitle", "questionsCount"];

function panelHtml(webview: vscode.Webview, media: vscode.Uri, school: School, lang: Lang): string {
  const css = webview.asWebviewUri(vscode.Uri.joinPath(media, "chat.css"));
  const js = webview.asWebviewUri(vscode.Uri.joinPath(media, "chat.js"));
  const md = webview.asWebviewUri(vscode.Uri.joinPath(media, "markdown.js"));
  const nonce = Math.random().toString(36).slice(2) + Math.random().toString(36).slice(2);
  // Raw: the panel fills in its own placeholders ({ago}, {cost}).
  const words: Record<string, string> = Object.fromEntries(PANEL_WORDS.map((k) => [k, MESSAGES[lang][k]]));
  words.signInPrompt = t(lang, "signInPrompt", { school: school.name });
  words.platformOnly = t(lang, "platformOnly");
  words.accent = school.accent;
  words.title = school.title;
  const data = JSON.stringify(words).replace(/</g, "\\u003c");
  return `<!doctype html><html lang="${lang}"><head><meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src ${webview.cspSource}; img-src data:; script-src 'nonce-${nonce}';">
<link rel="stylesheet" href="${css}"></head>
<body>
<nav id="tabs" role="tablist" hidden></nav>
<div id="log" role="log" aria-live="polite"></div>
<script type="application/json" id="words">${data}</script>
<form id="ask" hidden><div id="budgetline" hidden><span class="fill"></span></div>
<div id="thumbs" hidden></div><textarea id="input" rows="1"></textarea>
<div class="tools"><select id="model" class="pill"></select>
<span class="spacer"></span><button type="button" id="mic" class="icon" hidden></button><button type="submit" id="go"></button></div></form>
<div id="meters" class="meters" hidden><span id="budget" class="m" hidden></span>
<span id="context" class="m"><svg class="ring" viewBox="0 0 16 16" aria-hidden="true" hidden><circle class="track" cx="8" cy="8" r="6"/><circle class="used" cx="8" cy="8" r="6"/></svg><span class="txt"></span></span>
<span class="spacer"></span><button type="button" id="compact" class="link"></button><button type="button" id="clear" class="link"></button></div>
<script nonce="${nonce}" src="${md}"></script><script nonce="${nonce}" src="${js}"></script></body></html>`;
}
