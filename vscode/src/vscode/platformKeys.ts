// The platform's own connection (MaQI, owner 2026-11-12: "use the maqi
// connection, not bulkhours"; architect a39340). On a MaQI machine the
// platform writes each person's LiteLLM key to /run/maqi/keys/<account>/
// llm.env (0600, theirs) and renews it every 12 h: being on the machine is
// the sign-in. The key goes to the agent's environment only - never to
// SecretStorage, settings, logs or the conversation record.
import { readFileSync } from "node:fs";
import { userInfo } from "node:os";
import * as vscode from "vscode";
import { Said, t, type Lang } from "../core/i18n.ts";
import { keyFromFile, type Key } from "../core/keys.ts";
import type { Connection } from "../core/school.ts";
import type { KeySource } from "./credentials.ts";

export class PlatformKeys implements KeySource {
  readonly interactive = false;
  private key: Key | undefined;
  private readonly changed = new vscode.EventEmitter<void>();
  readonly onDidChange = this.changed.event;
  private readonly connection: Connection;
  private readonly lang: Lang;

  constructor(connection: Connection, lang: Lang = "en") {
    this.connection = connection;
    this.lang = lang;
  }

  known(): Key | undefined { return this.key; }

  // ${user} is the account, the only substitution.
  get file(): string { return this.connection.keyFile.replace(/\$\{user\}/g, userInfo().username); }

  async signedIn(): Promise<boolean> { return this.text() !== undefined; }

  // Nothing to open: the person is told where the key is expected.
  async signIn(): Promise<void> {
    void vscode.window.showWarningMessage(t(this.lang, "noKeyFile", { path: this.file }));
  }

  async signOut(): Promise<void> {}

  async handleUri(): Promise<void> {}

  // Read at the start of each turn: a key the platform renewed restarts the
  // agent, which resumes the conversation (ADR-0223).
  async currentKey(): Promise<{ key: Key; renewed: boolean }> {
    const text = this.text();
    if (text === undefined) throw new Said("noKeyFile", { path: this.file });
    const before = this.key;
    this.key = keyFromFile(text, this.connection.offer);
    return { key: this.key, renewed: before?.apiKey !== this.key.apiKey };
  }

  // MaQI's spend reader answers inside its own network only: no meter yet.
  async credits(): Promise<undefined> { return undefined; }

  private text(): string | undefined {
    try { return readFileSync(this.file, "utf8"); } catch { return undefined; }
  }
}
