// Entry point. The school is compiled into each build (scripts/build.mjs
// defines __SCHOOL__), so one codebase yields one extension per school.
import * as vscode from "vscode";
import { parseAgents } from "../core/agents.ts";
import { pickLang, setBrand, t, type Lang } from "../core/i18n.ts";
import { budgetText, level } from "../core/meter.ts";
import { packageName, parseSchool, type School } from "../core/school.ts";
import { offeredUpdate } from "../core/update.ts";
import { writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { ChatView } from "./chatView.ts";
import { Credentials, type KeySource } from "./credentials.ts";
import { PlatformKeys } from "./platformKeys.ts";
import { PlatformStatus } from "./platformStatus.ts";

declare const __SCHOOL__: unknown;

export function activate(ctx: vscode.ExtensionContext): void {
  const school = parseSchool(__SCHOOL__);
  const lang = pickLang(vscode.env.language, school.language);
  setBrand(school.title);
  // Commands, view and settings under the variant's own prefix.
  const id = (name: string) => `${school.prefix}.${name}`;
  const log = vscode.window.createOutputChannel(school.title);
  // The school's Moodle sign-in, or the platform's own key file (MaQI).
  const creds: KeySource = school.connection ? new PlatformKeys(school.connection, lang)
    : new Credentials(ctx.secrets, school, ctx.extension.id, lang);
  // The budget in the status bar, as MaQI's; a click opens the panel.
  const bar = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
  bar.command = id("chat.focus");
  const chat = new ChatView(ctx, school, creds, log, lang, (c) => showMeter(bar, c, lang));
  // The platform's own status bar (MaQI: RAM, CPU, data rights...).
  if (school.connection?.status) {
    ctx.subscriptions.push(new PlatformStatus(school.connection.status, { extensionPath: ctx.extensionPath, lang }));
  }
  ctx.subscriptions.push(
    log,
    bar,
    chat,
    vscode.window.registerUriHandler(creds),
    vscode.window.registerWebviewViewProvider(id("chat"), chat, { webviewOptions: { retainContextWhenHidden: true } }),
    vscode.commands.registerCommand(id("newChat"), () => chat.newChat()),
    vscode.commands.registerCommand(id("signIn"), () => creds.signIn()),
    vscode.commands.registerCommand(id("signOut"), () => creds.signOut()),
    vscode.commands.registerCommand(id("pickAgent"), () => pickAgent(creds, chat, lang, school.prefix)),
    vscode.commands.registerCommand(id("history"), () => history(chat, lang)),
    vscode.commands.registerCommand(id("rename"), () => rename(chat, lang)),
    // Restarts the variant's own agent and panel, nothing else in the window.
    vscode.commands.registerCommand(id("restart"), () => chat.restart()),
    vscode.commands.registerCommand(id("update"), () => update(ctx, school, lang, true)),
  );
  // Once a day at most, a quiet look for a newer build in the download area.
  const DAY = 86_400_000;
  if (Date.now() - (ctx.globalState.get<number>("bulkhours.updateChecked") ?? 0) > DAY) {
    void ctx.globalState.update("bulkhours.updateChecked", Date.now());
    void update(ctx, school, lang, false);
  }
}

// The project's conversations, newest first; picking one reopens it.
export async function history(chat: Pick<ChatView, "conversations" | "open">, lang: Lang = "en"): Promise<void> {
  const list = chat.conversations();
  if (!list.length) { void vscode.window.showInformationMessage(t(lang, "historyEmpty")); return; }
  const when = new Intl.DateTimeFormat(lang === "fr" ? "fr-FR" : "en-GB", { dateStyle: "medium", timeStyle: "short" });
  const pick = await vscode.window.showQuickPick(list.map((c) => ({
    label: c.title, description: `${c.agent} · ${c.model}`,
    detail: t(lang, "historyDetail", { date: when.format(c.updated), n: c.questions }), file: c.file,
  })), { placeHolder: t(lang, "historyPlaceholder"), matchOnDescription: true });
  if (pick) await chat.open(pick.file);
}

export async function rename(chat: Pick<ChatView, "rename" | "title">, lang: Lang = "en"): Promise<void> {
  const title = await vscode.window.showInputBox({ prompt: t(lang, "renamePrompt"), value: chat.title });
  if (title) await chat.rename(title);
}

// A newer build from the school's download area, installed in place.
async function update(ctx: vscode.ExtensionContext, school: School, lang: Lang, asked: boolean): Promise<void> {
  const current = String(ctx.extension.packageJSON.version);
  if (!school.downloadUrl) { if (asked) void vscode.window.showInformationMessage(t(lang, "updateUnavailable")); return; }
  try {
    const r = await fetch(new URL("latest.json", school.downloadUrl).toString(), { cache: "no-store" });
    const offer = r.ok ? offeredUpdate(await r.json() as Record<string, unknown>, school.id, current, school.downloadUrl, packageName(school)) : undefined;
    if (!offer) { if (asked) void vscode.window.showInformationMessage(t(lang, "upToDate", { version: current })); return; }
    if (!asked) {
      const go = await vscode.window.showInformationMessage(t(lang, "updateAvailable", { version: offer.version }), t(lang, "updateNow"));
      if (!go) return;
    }
    const vsix = await fetch(offer.url);
    if (!vsix.ok) throw new Error(`${offer.url} answered ${vsix.status}`);
    const file = join(tmpdir(), `${packageName(school)}-${offer.version}.vsix`);
    writeFileSync(file, Buffer.from(await vsix.arrayBuffer()));
    await vscode.commands.executeCommand("workbench.extensions.installExtension", vscode.Uri.file(file));
    const reload = await vscode.window.showInformationMessage(t(lang, "updated", { version: offer.version }), t(lang, "reloadNow"));
    if (reload) await vscode.commands.executeCommand("workbench.action.reloadWindow");
  } catch (e) {
    if (asked) void vscode.window.showWarningMessage(t(lang, "updateFailed", { message: (e as Error).message }));
  }
}

// The school's agent, or one of the student's own `<prefix>.extraAgents`.
export async function pickAgent(creds: Pick<KeySource, "known">, chat: Pick<ChatView, "newChat">,
                                lang: Lang = "en", prefix = "bulkhours"): Promise<void> {
  const cfg = vscode.workspace.getConfiguration(prefix);
  const school = creds.known()?.agent;
  const extra = parseAgents(cfg.get<unknown[]>("extraAgents") ?? []);
  const items = [
    ...(school ? [{ label: school.label, description: t(lang, "schoolAgent"), id: "" }] : []),
    ...extra.map((a) => ({ label: a.label, description: a.command, id: a.id })),
  ];
  if (!items.length) {
    void vscode.window.showInformationMessage(t(lang, "pickAgentNone"));
    return;
  }
  const pick = await vscode.window.showQuickPick(items, { placeHolder: t(lang, "pickAgentPlaceholder") });
  if (!pick) return;
  await cfg.update("agent", pick.id, true);
  chat.newChat();
}

type Bar = Pick<vscode.StatusBarItem, "show" | "hide"> & { text?: string; tooltip?: unknown; backgroundColor?: unknown };

export function showMeter(bar: Bar, c: { spent: number; budget: number; currency?: "USD" | "EUR" } | undefined, lang: Lang): void {
  if (!c) { bar.hide(); return; }
  const l = level(c.spent, c.budget);
  bar.text = `$(credit-card) ${budgetText(c, lang)}`;
  bar.tooltip = t(lang, "budgetTitle");
  bar.backgroundColor = l === "ok" ? undefined
    : new vscode.ThemeColor(l === "warn" ? "statusBarItem.warningBackground" : "statusBarItem.errorBackground");
  bar.show();
}

export function deactivate(): void {}
