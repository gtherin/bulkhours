// The decisions the VS Code layer makes, kept pure so they are tested:
// which model, which agent, which lines, what a key server answer means,
// and whether a sign-in link is one this window asked for.
import { pickAgent, type AgentSpec } from "./agents.ts";
import { Said, type MessageKey } from "./i18n.ts";
import type { Key } from "./keys.ts";

export function chooseModel(stored: string | undefined, key: Key | undefined): string {
  if (!key) return stored ?? "";
  return stored && key.models.includes(stored) ? stored : key.defaultModel;
}

export function chooseAgent(key: Key | undefined, extra: AgentSpec[], wanted: string): AgentSpec {
  const offered = key ? [key.agent, ...extra] : extra;
  return pickAgent(offered, offered.some((a) => a.id === wanted) ? wanted : "");
}

export function sliceLines(text: string, line?: number | null, limit?: number | null): string {
  if (!line && !limit) return text;
  const start = Math.max((line ?? 1) - 1, 0);
  return text.split("\n").slice(start, limit ? start + limit : undefined).join("\n");
}

// The way back to the editor, written out for the sign-in page. VS Code adds
// ?windowId=N when several windows are open - and hands it back INSIDE the
// path, where every toString() encodes the "?" as %3F: the page then refused
// the link (owner, 2026-11-12, twice). Rebuilt from the parts instead.
export function wayBack(u: { scheme: string; authority: string; path: string; query?: string }): string {
  const [path, inPath] = u.path.split(/\?|%3F/i);
  const query = [inPath, u.query].filter(Boolean).join("&");
  return `${u.scheme}://${u.authority}${path}${query ? `?${query}` : ""}`;
}

const FAILURES: Record<number, MessageKey> = { 401: "sessionExpired", 402: "noCredits" };

export function keyFailure(status: number): Said | null {
  if (status >= 200 && status < 300) return null;
  const known = FAILURES[status];
  return known ? new Said(known) : new Said("keyServerAnswered", { status });
}

export function signInToken(path: string, query: string, pending: string | undefined):
    { token: string } | { ignored: true } {
  const q = new URLSearchParams(query);
  if (path !== "/signed-in" || !pending || q.get("state") !== pending) return { ignored: true };
  const token = q.get("token");
  if (!token) throw new Said("noToken");
  return { token };
}
