// The chat panel: one agent session per conversation, the transcript folded
// by the pure reducer, permission requests turned into buttons in the panel.
import * as vscode from "vscode";
import type { RequestPermissionOutcome, RequestPermissionRequest } from "@agentclientprotocol/sdk";
import { AgentSession } from "../core/acpSession.ts";
import { launchFor, parseAgents, type AgentSpec } from "../core/agents.ts";
import { chooseAgent, chooseModel } from "../core/choices.ts";
import { MESSAGES, Said, sayError, t, type Lang, type MessageKey } from "../core/i18n.ts";
import type { Key } from "../core/keys.ts";
import type { School } from "../core/school.ts";
import { addNotice, addUserPrompt, applyUpdate, type Transcript } from "../core/transcript.ts";
import type { Credentials } from "./credentials.ts";
import { readTextFile, writeTextFile } from "./editorHost.ts";

type FromPanel =
  | { type: "ready" } | { type: "signIn" } | { type: "cancel" } | { type: "newChat" }
  | { type: "send"; text: string; images?: Pasted[] } | { type: "model"; model: string }
  | { type: "compact" } | { type: "clear" } | { type: "pickAgent" }
  | { type: "choose"; agent: string; model?: string }
  | { type: "permission"; id: number; optionId: string | null };

type Pasted = { mimeType: string; data: string };
type Credits = { spent: number; budget: number };
// What a paste may carry into a prompt: pictures, nothing else.
const IMAGE_TYPES = new Set(["image/png", "image/jpeg", "image/gif", "image/webp"]);
// LiteLLM writes spend in batches (about a minute, measured 2026-11-10): the
// meter is read after a turn, then once more when the batch has landed.
const SPEND_LANDS_MS = 75_000;
// An agent idle this long is stopped to free its memory (265 MB for dsh, about
// 500 MB for Claude Code, measured 2026-11-10; a shared GPU machine holds one
// per student) - only when it saves its sessions and can resume them.
const IDLE_MS = 15 * 60_000;

export class ChatView implements vscode.WebviewViewProvider, vscode.Disposable {
  private view: vscode.WebviewView | undefined;
  private session: AgentSession | undefined;
  private transcript: Transcript = [];
  private busy = false;
  private starting = false;
  // Stop pressed while the agent was still starting: honoured once it is up.
  private stopAsked = false;
  private nextAsk = 1;
  private readonly asks = new Map<number, (o: RequestPermissionOutcome) => void>();
  private readonly ctx: vscode.ExtensionContext;
  private readonly school: School;
  private readonly creds: Credentials;
  private readonly log: vscode.OutputChannel;
  private readonly lang: Lang;
  private readonly meter: (c: Credits | undefined) => void;
  private credits: Credits | undefined;
  private usage: { used: number; size: number } | null = null;
  // Slash commands the agent announced (ACP available_commands_update).
  // "/compact" is sent only to an agent that offers it: dsh does not, and
  // took it for a question (owner, 2026-11-10).
  private commands: string[] = [];
  private spendTimer: ReturnType<typeof setTimeout> | undefined;
  private idleTimer: ReturnType<typeof setTimeout> | undefined;
  private readonly idleMs: number;
  // A conversation whose agent was paused: resumed at the next message if the
  // same agent and model are still chosen.
  private paused: { sessionId: string; launchKey: string } | undefined;

  constructor(ctx: vscode.ExtensionContext, school: School, creds: Credentials, log: vscode.OutputChannel,
              lang: Lang = "en", meter: (c: Credits | undefined) => void = () => {}, idleMs = IDLE_MS) {
    this.ctx = ctx;
    this.school = school;
    this.creds = creds;
    this.log = log;
    this.lang = lang;
    this.meter = meter;
    this.idleMs = idleMs;
    creds.onDidChange(() => { this.forget(); void this.render(); });
  }

  resolveWebviewView(view: vscode.WebviewView): void {
    this.view = view;
    const media = vscode.Uri.joinPath(this.ctx.extensionUri, "media");
    view.webview.options = { enableScripts: true, localResourceRoots: [media] };
    view.webview.html = panelHtml(view.webview, media, this.school, this.lang);
    view.webview.onDidReceiveMessage((m: FromPanel) => this.onPanel(m).catch((e) => this.fail(e)));
  }

  // VS Code closing: the agent process must not outlive the editor.
  dispose(): void {
    clearTimeout(this.spendTimer);
    clearTimeout(this.idleTimer);
    this.endSession();
  }

  newChat(): void {
    this.forget();
    this.transcript = [];
    this.usage = null;
    void this.render();
  }

  // The key lives in memory only, so after a window reload the menu would
  // know no school model until the first message. Fetch it as the panel
  // opens; a failure here is shown at the first message, not now.
  private async warmKey(): Promise<void> {
    if (this.creds.known() || !(await this.creds.signedIn())) return;
    try { await this.creds.currentKey(); } catch { return; }
    await this.render();
  }

  // The budget meter, read from the key server. Never fails the panel.
  async refreshCredits(): Promise<void> {
    this.credits = await this.creds.credits();
    this.meter(this.credits);
    await this.render();
  }

  private async onPanel(m: FromPanel): Promise<void> {
    switch (m.type) {
      case "ready": await this.render(); await this.warmKey(); return this.refreshCredits();
      case "compact": return this.commands.includes("compact") ? this.send("/compact") : undefined;
      case "clear": return this.newChat();
      case "pickAgent": await vscode.commands.executeCommand("bulkhours.pickAgent"); return;
      case "choose": return this.choose(m.agent, m.model);
      case "signIn": return this.creds.signIn();
      case "newChat": return this.newChat();
      case "cancel": return this.stop();
      case "model":
        await this.ctx.globalState.update("bulkhours.model", m.model);
        this.forget();
        return this.render();
      case "permission": return this.answer(m.id, m.optionId);
      case "send": return this.send(m.text, m.images ?? []);
    }
  }

  // One menu: a school model (the school's agent on the school's credits)
  // or one of the student's own agents, such as Claude Code on their own
  // subscription. Either way the next message starts a fresh agent.
  private async choose(agent: string, model?: string): Promise<void> {
    await vscode.workspace.getConfiguration("bulkhours").update("agent", agent, true);
    if (model) await this.ctx.globalState.update("bulkhours.model", model);
    this.forget();
    await this.render();
  }

  private agentChoices(key: Key | undefined): { id: string; label: string }[] {
    const extra = parseAgents(vscode.workspace.getConfiguration("bulkhours").get<unknown[]>("extraAgents") ?? []);
    return [...(key ? [{ id: "", label: key.agent.label }] : []), ...extra.map((a) => ({ id: a.id, label: a.label }))];
  }

  private model(key: Key | undefined): string {
    return chooseModel(this.ctx.globalState.get<string>("bulkhours.model"), key);
  }

  // The school's agent comes with the key; a student may pick one of their
  // own `bulkhours.extraAgents` instead.
  private agent(key: Key | undefined): AgentSpec {
    const cfg = vscode.workspace.getConfiguration("bulkhours");
    return chooseAgent(key, parseAgents(cfg.get<unknown[]>("extraAgents") ?? []), cfg.get<string>("agent") ?? "");
  }

  private async stop(): Promise<void> {
    if (!this.busy) return;
    this.stopAsked = true;
    await this.session?.cancel();
  }

  private async send(text: string, pasted: Pasted[] = []): Promise<void> {
    if (this.busy || !text.trim()) return;
    this.busy = true;
    this.stopAsked = false;
    const images = pasted.filter((i) => IMAGE_TYPES.has(i.mimeType) && /^[A-Za-z0-9+/=]+$/.test(i.data));
    this.transcript = addUserPrompt(this.transcript, text, images.map((i) => `data:${i.mimeType};base64,${i.data}`));
    await this.render();
    try {
      const session = await this.ensureSession();
      if (this.stopAsked) {
        this.transcript = addNotice(this.transcript, t(this.lang, "stoppedBeforeStart"));
        return;
      }
      if (images.length && !session.acceptsImages) this.transcript = addNotice(this.transcript, t(this.lang, "noImages"));
      const stop = await session.prompt(text, activeFileContext(), images);
      if (stop !== "end_turn") this.transcript = addNotice(this.transcript, t(this.lang, "stopped", { reason: reason(this.lang, stop) }));
    } finally {
      this.busy = false;
      await this.render();
      void this.refreshCredits();
      clearTimeout(this.spendTimer);
      this.spendTimer = setTimeout(() => void this.refreshCredits(), SPEND_LANDS_MS);
      this.spendTimer.unref?.();
      this.armIdle();
    }
  }

  private armIdle(): void {
    clearTimeout(this.idleTimer);
    if (!this.session?.canResume) return;
    this.idleTimer = setTimeout(() => this.pause(), this.idleMs);
    this.idleTimer.unref?.();
  }

  private pause(): void {
    if (this.busy || !this.session) return;
    this.paused = { sessionId: this.session.sessionId, launchKey: this.launchKey };
    this.endSession();
    this.transcript = addNotice(this.transcript, t(this.lang, "agentPaused"));
    void this.render();
  }

  // A new chat, another agent or model, a sign-out: nothing to resume.
  private forget(): void {
    clearTimeout(this.idleTimer);
    this.paused = undefined;
    this.endSession();
  }

  private launchKey = "";

  private async ensureSession(): Promise<AgentSession> {
    const { key, renewed } = await this.creds.currentKey();
    if (this.session && !renewed) return this.session;
    if (this.session) this.transcript = addNotice(this.transcript, t(this.lang, "keyRenewed"));
    // A renewed key restarts the agent (it reads its key once): it resumes
    // the conversation when it can, as after a pause.
    if (this.session?.canResume) this.paused = { sessionId: this.session.sessionId, launchKey: this.launchKey };
    this.endSession();
    const folder = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!folder) throw new Said("openFolder");
    const model = this.model(key);
    const launch = launchFor(this.agent(key), {
      baseUrl: key.baseUrl, apiKey: key.apiKey, model, extensionPath: this.ctx.extensionPath,
    });
    launch.env.BULKHOURS_MODEL = model;
    launch.env.BULKHOURS_MODELS = key.models.join(",");
    const launchKey = `${this.agent(key).id}|${model}`;
    const resume = this.paused?.launchKey === launchKey ? this.paused.sessionId : undefined;
    this.paused = undefined;
    // The first start on a machine can download the agent (minutes, measured
    // 2026-11-10): the panel says so instead of staying silent.
    this.starting = true;
    await this.render();
    try {
      this.session = await AgentSession.start(launch, folder, {
        readTextFile, writeTextFile,
        askPermission: (req) => this.ask(req),
        onUpdate: (u) => {
          if (u.sessionUpdate === "usage_update") this.usage = { used: u.used, size: u.size };
          if (u.sessionUpdate === "available_commands_update") this.commands = u.availableCommands.map((c) => c.name);
          this.transcript = applyUpdate(this.transcript, u);
          void this.render();
        },
        log: (line) => this.log.append(line),
      }, this.ctx.extension.packageJSON.version, resume);
      this.launchKey = launchKey;
    } finally {
      this.starting = false;
    }
    return this.session;
  }

  private ask(req: RequestPermissionRequest): Promise<RequestPermissionOutcome> {
    const id = this.nextAsk++;
    void this.view?.webview.postMessage({
      type: "permission", id, title: req.toolCall.title ?? t(this.lang, "agentWantsToAct"),
      options: req.options.map((o) => ({ id: o.optionId, name: o.name, kind: o.kind })),
    });
    return new Promise((resolve) => this.asks.set(id, resolve));
  }

  private answer(id: number, optionId: string | null): void {
    const resolve = this.asks.get(id);
    this.asks.delete(id);
    resolve?.(optionId ? { outcome: "selected", optionId } : { outcome: "cancelled" });
  }

  private endSession(): void {
    this.commands = [];
    for (const resolve of this.asks.values()) resolve({ outcome: "cancelled" });
    this.asks.clear();
    this.session?.dispose();
    this.session = undefined;
  }

  private fail(e: unknown): void {
    this.transcript = addNotice(this.transcript, t(this.lang, "error", { message: sayError(this.lang, e) }));
    this.busy = false;
    void this.render();
  }

  private async render(): Promise<void> {
    const key = this.creds.known();
    await this.view?.webview.postMessage({
      type: "state", transcript: this.transcript, busy: this.busy, starting: this.starting,
      signedIn: await this.creds.signedIn(), model: this.model(key), models: key?.models ?? [],
      agent: key ? safeLabel(() => this.agent(key).label) : "",
      modelLabels: key?.modelLabels ?? {}, modelPrices: key?.modelPrices ?? {},
      agents: safeList(() => this.agentChoices(key)), agentId: key ? safeLabel(() => (this.agent(key) === key.agent ? "" : this.agent(key).id)) : "",
      credits: this.credits ?? null, usage: this.usage, commands: this.commands,
    });
  }
}

function safeList<T>(f: () => T[]): T[] {
  try { return f(); } catch { return []; }
}

function safeLabel(f: () => string): string {
  try { return f(); } catch (e) { return `(${(e as Error).message})`; }
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

// The panel's own words, sent once in the page as data (never as script).
const PANEL_WORDS: MessageKey[] = ["signIn", "emptyChat", "placeholder", "send", "stop", "model", "thinking", "output", "noChange", "startingAgent",
  "compact", "compactHint", "clear", "clearHint", "thinkingVerb", "budgetTitle", "contextTitle", "removeImage",
  "suggestExplain", "suggestBuild", "suggestFaster", "schoolModels", "yourAgents", "mic", "micWindows", "micMac"];

function panelHtml(webview: vscode.Webview, media: vscode.Uri, school: School, lang: Lang): string {
  const css = webview.asWebviewUri(vscode.Uri.joinPath(media, "chat.css"));
  const js = webview.asWebviewUri(vscode.Uri.joinPath(media, "chat.js"));
  const md = webview.asWebviewUri(vscode.Uri.joinPath(media, "markdown.js"));
  const nonce = Math.random().toString(36).slice(2) + Math.random().toString(36).slice(2);
  const words = Object.fromEntries(PANEL_WORDS.map((k) => [k, t(lang, k)]));
  words.signInPrompt = t(lang, "signInPrompt", { school: school.name });
  words.accent = school.accent;
  words.title = `BulkHours ${school.name}`;
  const data = JSON.stringify(words).replace(/</g, "\\u003c");
  return `<!doctype html><html lang="${lang}"><head><meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src ${webview.cspSource}; img-src data:; script-src 'nonce-${nonce}';">
<link rel="stylesheet" href="${css}"></head>
<body>
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
