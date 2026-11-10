// How the panel writes its two meters, after MaQI's status bar: the budget
// ("$0.12 / $10", amber from 80 %, red when spent) and the agent's context
// ("40.6K / 64K"). Pure, so the thresholds are tested, not eyeballed.

export type Level = "ok" | "warn" | "over";

export function tokens(n: number): string {
  if (n < 1000) return String(n);
  const [v, unit] = n < 1_000_000 ? [n / 1000, "K"] : [n / 1_048_576, "M"];
  return `${Number(v.toFixed(1))}${unit}`;
}

export function money(usd: number): string {
  if (usd === 0) return "$0";
  if (usd < 0.01) return "<$0.01";
  return Number.isInteger(usd) ? `$${usd}` : `$${usd.toFixed(2)}`;
}

export function level(spent: number, budget: number): Level {
  if (budget <= 0 || spent >= budget) return "over";
  return spent >= 0.8 * budget ? "warn" : "ok";
}

export function budgetText(c: { spent: number; budget: number }): string {
  return `${money(c.spent)} / ${money(c.budget)}`;
}
