// How the panel writes its two meters, after MaQI's status bar: the budget
// ("$0.12 / $10", amber from 80 %, red when spent) and the agent's context
// ("40.6K / 64K"). Pure, so the thresholds are tested, not eyeballed.

export type Level = "ok" | "warn" | "over";

export function tokens(n: number): string {
  if (n < 1000) return String(n);
  const [v, unit] = n < 1_000_000 ? [n / 1000, "K"] : [n / 1_048_576, "M"];
  return `${Number(v.toFixed(1))}${unit}`;
}

export type Currency = "USD" | "EUR";

// Amounts are LiteLLM's (Nebius dollars); a school may show them as euros at
// par (its tenant file says `currency: EUR`): the symbol changes, not the value.
export function money(v: number, currency: Currency = "USD", lang = "en"): string {
  const fmt = (x: number) => new Intl.NumberFormat(lang === "fr" ? "fr-FR" : "en-US", {
    style: "currency", currency, minimumFractionDigits: Number.isInteger(x) ? 0 : 2, maximumFractionDigits: 2,
  }).format(x);
  if (v > 0 && v < 0.01) return `<${fmt(0.01)}`;
  return fmt(v);
}

export function level(spent: number, budget: number): Level {
  if (budget <= 0 || spent >= budget) return "over";
  return spent >= 0.8 * budget ? "warn" : "ok";
}

export function budgetText(c: { spent: number; budget: number; currency?: Currency }, lang = "en"): string {
  return `${money(c.spent, c.currency, lang)} / ${money(c.budget, c.currency, lang)}`;
}
