// The school's key server hands out three things together: the student's
// short-lived LiteLLM key, the models it may use, and the agent to run
// (architect 2026-11-09, f4e084: the extension never hard-codes an argv).
// The key expires on purpose: the extension renews it ten minutes ahead and
// restarts the agent, which reads its key only once, at start.
import { parseAgents, type AgentSpec } from "./agents.ts";
import { date, failer, https, names, type Fail } from "./fields.ts";

export type Key = {
  apiKey: string;
  baseUrl: string;
  expiresAt: number;
  models: string[];
  defaultModel: string;
  agent: AgentSpec;
  // The underlying LLM of each alias ("fast" -> "DeepSeek V4.1 Flash"):
  // students should know which model answers them. Optional.
  modelLabels: Record<string, string>;
  // Dollars per million tokens, in / out, as the school's LiteLLM charges.
  modelPrices: Record<string, { in: number; out: number }>;
};

const RENEW_BEFORE_MS = 10 * 60 * 1000;

export function parseKeyReply(raw: unknown): Key {
  const o = (raw ?? {}) as Record<string, unknown>;
  const fail = failer("key server");
  // Checked in this order: the key first, it is the error a student can act on.
  const apiKey = typeof o.key === "string" && o.key ? o.key : fail(`"key" missing`);
  const baseUrl = https(o, "base_url", fail, "https");
  const expiresAt = date(o, "expires_at", fail);
  const models = names(o, "models", fail);
  return {
    apiKey, baseUrl, expiresAt, models,
    defaultModel: offered(o.default_model, models, fail),
    agent: theAgent(o.agent, fail),
    modelLabels: labels(o.model_labels, models),
    modelPrices: prices(o.model_prices, models),
  };
}

function prices(raw: unknown, models: string[]): Record<string, { in: number; out: number }> {
  const o = (raw && typeof raw === "object" ? raw : {}) as Record<string, { in?: unknown; out?: unknown } | undefined>;
  return Object.fromEntries(models.filter((m) => typeof o[m]?.in === "number" && typeof o[m]?.out === "number")
    .map((m) => [m, { in: o[m]!.in as number, out: o[m]!.out as number }]));
}

function labels(raw: unknown, models: string[]): Record<string, string> {
  const o = (raw && typeof raw === "object" ? raw : {}) as Record<string, unknown>;
  return Object.fromEntries(models.filter((m) => typeof o[m] === "string").map((m) => [m, o[m] as string]));
}

function offered(wanted: unknown, models: string[], fail: Fail): string {
  const m = typeof wanted === "string" ? wanted : models[0];
  return models.includes(m) ? m : fail(`default model "${m}" is not offered`);
}

function theAgent(raw: unknown, fail: Fail): AgentSpec {
  try { return parseAgents([raw])[0]; } catch (e) { return fail((e as Error).message); }
}

export function needsRenewal(expiresAt: number, now: number): boolean {
  return now >= expiresAt - RENEW_BEFORE_MS;
}
