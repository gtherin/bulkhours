// Entry point. The school is compiled into each build (scripts/build.mjs
// defines __SCHOOL__), so one codebase yields one extension per school.
import * as vscode from "vscode";
import { parseAgents } from "../core/agents.ts";
import { pickLang, t, type Lang } from "../core/i18n.ts";
import { parseSchool } from "../core/school.ts";
import { ChatView } from "./chatView.ts";
import { Credentials } from "./credentials.ts";

declare const __SCHOOL__: unknown;

export function activate(ctx: vscode.ExtensionContext): void {
  const school = parseSchool(__SCHOOL__);
  const lang = pickLang(vscode.env.language, school.language);
  const log = vscode.window.createOutputChannel(`BulkHours ${school.name}`);
  const creds = new Credentials(ctx.secrets, school, ctx.extension.id, lang);
  const chat = new ChatView(ctx, school, creds, log, lang);
  ctx.subscriptions.push(
    log,
    chat,
    vscode.window.registerUriHandler(creds),
    vscode.window.registerWebviewViewProvider("bulkhours.chat", chat, { webviewOptions: { retainContextWhenHidden: true } }),
    vscode.commands.registerCommand("bulkhours.newChat", () => chat.newChat()),
    vscode.commands.registerCommand("bulkhours.signIn", () => creds.signIn()),
    vscode.commands.registerCommand("bulkhours.signOut", () => creds.signOut()),
    vscode.commands.registerCommand("bulkhours.pickAgent", () => pickAgent(creds, chat, lang)),
  );
}

// The school's agent, or one of the student's own `bulkhours.extraAgents`.
export async function pickAgent(creds: Pick<Credentials, "known">, chat: Pick<ChatView, "newChat">,
                                lang: Lang = "en"): Promise<void> {
  const cfg = vscode.workspace.getConfiguration("bulkhours");
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

export function deactivate(): void {}
