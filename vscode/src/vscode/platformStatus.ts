// The platform's status bar items (MaQI: RAM, CPU, Wasabi rights, idle,
// egress), refreshed every minute while the window is open. The command is
// the variant's (connection.status); a failure hides the items, never an error.
import { execFile } from "node:child_process";
import * as vscode from "vscode";
import { parseStatus, type StatusItem } from "../core/platformStatus.ts";

const EVERY_MS = 60_000;
const TIMEOUT_MS = 30_000;
const COLOURS = { warn: "statusBarItem.warningBackground", error: "statusBarItem.errorBackground" } as const;

export class PlatformStatus implements vscode.Disposable {
  private readonly items = new Map<string, vscode.StatusBarItem>();
  private readonly timer: ReturnType<typeof setInterval>;
  private readonly command: string;
  private readonly args: string[];
  private running = false;

  constructor(status: { command: string; args: string[] }, vars: Record<string, string>) {
    this.command = status.command;
    this.args = status.args.map((a) => a.replace(/\$\{(\w+)\}/g, (m, k: string) => vars[k] ?? m));
    void this.refresh();
    this.timer = setInterval(() => void this.refresh(), EVERY_MS);
  }

  async refresh(): Promise<void> {
    if (this.running) return;
    this.running = true;
    try { this.show(parseStatus(await this.run())); } finally { this.running = false; }
  }

  private run(): Promise<string> {
    return new Promise((resolve) => execFile(this.command, this.args, { timeout: TIMEOUT_MS },
      (err, out) => resolve(err ? "" : String(out))));
  }

  private show(list: StatusItem[]): void {
    const seen = new Set(list.map((i) => i.id));
    for (const [id, item] of this.items) if (!seen.has(id)) { item.dispose(); this.items.delete(id); }
    list.forEach((i, n) => {
      let item = this.items.get(i.id);
      // Left side, in the platform's order: JupyterLab's bar reads left to right.
      if (!item) { item = vscode.window.createStatusBarItem(`platform.${i.id}`, vscode.StatusBarAlignment.Left, 100 - n); this.items.set(i.id, item); }
      item.text = i.text;
      item.tooltip = i.tooltip;
      item.backgroundColor = i.level === "ok" ? undefined : new vscode.ThemeColor(COLOURS[i.level]);
      item.show();
    });
  }

  dispose(): void {
    clearInterval(this.timer);
    for (const item of this.items.values()) item.dispose();
    this.items.clear();
  }
}
