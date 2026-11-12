// "Rendered page (HTML)" in Reopen Editor With, for .py files: a marimo
// notebook's page (marimo export html, results only) in a tab, rendered
// again at each save of the file - by the person or by the agent.
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { basename, dirname, join } from "node:path";
import * as vscode from "vscode";
import { t, type Lang } from "../core/i18n.ts";
import { isMarimo, marimoCandidates, showable } from "../core/render.ts";

const EXPORT_TIMEOUT_MS = 15 * 60_000;

type Result = { ok: true } | { ok: false; why: string };

function run(cmd: string, args: string[], cwd: string): Promise<Result & { missing?: boolean }> {
  return new Promise((resolve) => execFile(cmd, args, { cwd, timeout: EXPORT_TIMEOUT_MS, maxBuffer: 8 << 20 }, (err, _out, errOut) => {
    if (!err) return resolve({ ok: true });
    const missing = (err as NodeJS.ErrnoException).code === "ENOENT";
    resolve({ ok: false, missing, why: (String(errOut).trim().split("\n").slice(-12).join("\n") || err.message).slice(0, 3000) });
  }));
}

export class RenderEditor implements vscode.CustomReadonlyEditorProvider {
  private readonly prefix: string;
  private readonly lang: Lang;

  constructor(prefix: string, lang: Lang) {
    this.prefix = prefix;
    this.lang = lang;
  }

  openCustomDocument(uri: vscode.Uri): vscode.CustomDocument {
    return { uri, dispose: () => {} };
  }

  resolveCustomEditor(doc: vscode.CustomDocument, panel: vscode.WebviewPanel): void {
    panel.webview.options = { enableScripts: true };
    const file = doc.uri.fsPath;
    let running = false, again = false;
    const render = async (): Promise<void> => {
      if (running) { again = true; return; }
      running = true;
      try { panel.webview.html = await this.page(file); } finally { running = false; }
      if (again) { again = false; void render(); }
    };
    // Saved by the person (an editor) or written by the agent (the disk).
    const watcher = vscode.workspace.createFileSystemWatcher(new vscode.RelativePattern(vscode.Uri.file(dirname(file)), basename(file)));
    watcher.onDidChange(() => void render());
    panel.onDidDispose(() => watcher.dispose());
    void render();
  }

  private async page(file: string): Promise<string> {
    let source = "";
    try { source = readFileSync(file, "utf8"); } catch (e) { return this.note(t(this.lang, "renderUnreadable", { message: (e as Error).message })); }
    if (!isMarimo(source)) return this.note(t(this.lang, "renderNotMarimo"));
    const out = join(tmpdir(), `${this.prefix}-render-${createHash("sha1").update(file).digest("hex").slice(0, 12)}.html`);
    const folder = vscode.workspace.getWorkspaceFolder(vscode.Uri.file(file))?.uri.fsPath ?? dirname(file);
    const setting = vscode.workspace.getConfiguration(this.prefix).get<string>("marimo");
    const interpreter = vscode.workspace.getConfiguration("python").get<string>("defaultInterpreterPath");
    let last = "";
    for (const marimo of marimoCandidates(setting, interpreter)) {
      const r = await run(marimo, ["export", "html", file, "-o", out, "--no-include-code"], folder);
      if (r.ok) return showable(readFileSync(out, "utf8"));
      last = r.why;
      if (!r.missing) break;           // marimo ran and failed: say why, do not try another
    }
    return this.note(t(this.lang, "renderFailed", { message: last }));
  }

  private note(text: string): string {
    const esc = text.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]!));
    return `<!doctype html><meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'">`
      + `<body style="font:13px var(--vscode-font-family);color:var(--vscode-foreground);padding:16px"><pre style="white-space:pre-wrap">${esc}</pre>`;
  }
}
