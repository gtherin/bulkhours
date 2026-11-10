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
  | { type: "send"; text: string } | { type: "model"; model: string }
  | { type: "permission"; id: number; optionId: string | null };

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

  constructor(ctx: vscode.ExtensionContext, school: School, creds: Credentials, log: vscode.OutputChannel,
              lang: Lang = "en") {
    this.ctx = ctx;
    this.school = school;
    this.creds = creds;
    this.log = log;
    this.lang = lang;
    creds.onDidChange(() => { this.endSession(); void this.render(); });
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
    this.endSession();
  }

  newChat(): void {
    this.endSession();
    this.transcript = [];
    void this.render();
  }

  private async onPanel(m: FromPanel): Promise<void> {
    switch (m.type) {
      case "ready": return this.render();
      case "signIn": return this.creds.signIn();
      case "newChat": return this.newChat();
      case "cancel": return this.stop();
      case "model":
        await this.ctx.globalState.update("bulkhours.model", m.model);
        this.endSession();
        return this.render();
      case "permission": return this.answer(m.id, m.optionId);
      case "send": return this.send(m.text);
    }
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

  private async send(text: string): Promise<void> {
    if (this.busy || !text.trim()) return;
    this.busy = true;
    this.stopAsked = false;
    this.transcript = addUserPrompt(this.transcript, text);
    await this.render();
    try {
      const session = await this.ensureSession();
      if (this.stopAsked) {
        this.transcript = addNotice(this.transcript, t(this.lang, "stoppedBeforeStart"));
        return;
      }
      const stop = await session.prompt(text, activeFileContext());
      if (stop !== "end_turn") this.transcript = addNotice(this.transcript, t(this.lang, "stopped", { reason: reason(this.lang, stop) }));
    } finally {
      this.busy = false;
      await this.render();
    }
  }

  private async ensureSession(): Promise<AgentSession> {
    const { key, renewed } = await this.creds.currentKey();
    if (this.session && !renewed) return this.session;
    if (this.session) this.transcript = addNotice(this.transcript, t(this.lang, "keyRenewed"));
    this.endSession();
    const folder = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!folder) throw new Said("openFolder");
    const model = this.model(key);
    const launch = launchFor(this.agent(key), {
      baseUrl: key.baseUrl, apiKey: key.apiKey, model, extensionPath: this.ctx.extensionPath,
    });
    launch.env.BULKHOURS_MODEL = model;
    launch.env.BULKHOURS_MODELS = key.models.join(",");
    // The first start on a machine can download the agent (minutes, measured
    // 2026-11-10): the panel says so instead of staying silent.
    this.starting = true;
    await this.render();
    try {
      this.session = await AgentSession.start(launch, folder, {
        readTextFile, writeTextFile,
        askPermission: (req) => this.ask(req),
        onUpdate: (u) => { this.transcript = applyUpdate(this.transcript, u); void this.render(); },
        log: (line) => this.log.append(line),
      }, this.ctx.extension.packageJSON.version);
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
    });
  }
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
const PANEL_WORDS: MessageKey[] = ["signIn", "emptyChat", "placeholder", "send", "stop", "model", "thinking", "output", "noChange", "startingAgent"];

function panelHtml(webview: vscode.Webview, media: vscode.Uri, school: School, lang: Lang): string {
  const css = webview.asWebviewUri(vscode.Uri.joinPath(media, "chat.css"));
  const js = webview.asWebviewUri(vscode.Uri.joinPath(media, "chat.js"));
  const nonce = Math.random().toString(36).slice(2) + Math.random().toString(36).slice(2);
  const words = Object.fromEntries(PANEL_WORDS.map((k) => [k, t(lang, k)]));
  words.signInPrompt = t(lang, "signInPrompt", { school: school.name });
  const data = JSON.stringify(words).replace(/</g, "\\u003c");
  return `<!doctype html><html lang="${lang}"><head><meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src ${webview.cspSource}; script-src 'nonce-${nonce}';">
<link rel="stylesheet" href="${css}"></head>
<body style="--accent:${school.accent}">
<div id="log" role="log" aria-live="polite"></div>
<script type="application/json" id="words">${data}</script>
<form id="ask"><textarea id="input" rows="3"></textarea>
<div class="bar"><select id="model"></select><span id="agent"></span>
<button type="button" id="stop" hidden></button><button type="submit" id="send"></button></div></form>
<script nonce="${nonce}" src="${js}"></script></body></html>`;
}
