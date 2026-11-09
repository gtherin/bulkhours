// Sign-in and the student's short-lived LiteLLM key.
// The BulkHours token lives in VS Code's SecretStorage, never in settings;
// the LiteLLM key lives in memory only and is renewed before it expires.
import { randomUUID } from "node:crypto";
import * as vscode from "vscode";
import { keyFailure, signInToken } from "../core/choices.ts";
import { Said, t, type Lang } from "../core/i18n.ts";
import { needsRenewal, parseKeyReply, type Key } from "../core/keys.ts";
import type { School } from "../core/school.ts";

const TOKEN = "bulkhours.token";

export class Credentials implements vscode.UriHandler {
  private key: Key | undefined;
  private pendingState: string | undefined;
  private readonly changed = new vscode.EventEmitter<void>();
  readonly onDidChange = this.changed.event;
  private readonly secrets: vscode.SecretStorage;
  private readonly school: School;
  private readonly extensionId: string;
  private readonly lang: Lang;

  constructor(secrets: vscode.SecretStorage, school: School, extensionId: string, lang: Lang = "en") {
    this.secrets = secrets;
    this.school = school;
    this.extensionId = extensionId;
    this.lang = lang;
  }

  // The last key the server gave, for what the panel shows (models, agent).
  known(): Key | undefined { return this.key; }

  async signedIn(): Promise<boolean> {
    return Boolean(await this.secrets.get(TOKEN));
  }

  // Opens the school's sign-in page; it comes back through handleUri.
  async signIn(): Promise<void> {
    this.pendingState = randomUUID();
    const back = await vscode.env.asExternalUri(
      vscode.Uri.parse(`${vscode.env.uriScheme}://${this.extensionId}/signed-in`));
    const url = new URL(this.school.signInUrl);
    url.searchParams.set("redirect", back.toString());
    url.searchParams.set("state", this.pendingState);
    await vscode.env.openExternal(vscode.Uri.parse(url.toString()));
  }

  async handleUri(uri: vscode.Uri): Promise<void> {
    const link = signInToken(uri.path, uri.query, this.pendingState);
    if ("ignored" in link) {
      void vscode.window.showWarningMessage(t(this.lang, "ignoredLink"));
      return;
    }
    this.pendingState = undefined;
    await this.secrets.store(TOKEN, link.token);
    this.key = undefined;
    // Fetch a key now: it proves the sign-in worked and fills the model list.
    try { await this.currentKey(); } finally { this.changed.fire(); }
  }

  async signOut(): Promise<void> {
    await this.secrets.delete(TOKEN);
    this.key = undefined;
    this.changed.fire();
  }

  // A valid key, renewed when it is ten minutes from expiry. `renewed` tells
  // the caller to restart the agent, which only reads its key at start.
  async currentKey(): Promise<{ key: Key; renewed: boolean }> {
    if (this.key && !needsRenewal(this.key.expiresAt, Date.now())) return { key: this.key, renewed: false };
    this.key = await this.fetchKey();
    return { key: this.key, renewed: true };
  }

  private async fetchKey(): Promise<Key> {
    const token = await this.secrets.get(TOKEN);
    if (!token) throw new Said("notSignedIn");
    const r = await fetch(this.school.keyUrl, {
      method: "POST",
      headers: { authorization: `Bearer ${token}`, "content-type": "application/json" },
      body: JSON.stringify({ school: this.school.id }),
    });
    const failure = keyFailure(r.status);
    if (r.status === 401) await this.signOut();
    if (failure) throw failure;
    return parseKeyReply(await r.json());
  }
}
