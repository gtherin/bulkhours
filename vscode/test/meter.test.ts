import { test } from "node:test";
import assert from "node:assert/strict";
import { budgetText, level, money, tokens } from "../src/core/meter.ts";

test("token counts read like MaQI's context wheel: 40.6K / 64K", () => {
  assert.deepEqual([950, 40_600, 64_000, 1_048_576].map(tokens), ["950", "40.6K", "64K", "1M"]);
});

test("money is in dollars, cents kept, tiny spends not shown as zero", () => {
  assert.deepEqual([0, 0.004, 0.1234, 10, 2.5].map((v) => money(v)), ["$0", "<$0.01", "$0.12", "$10", "$2.50"]);
});

test("the meter warns from 80% and is over at 100%", () => {
  assert.deepEqual([[0, 5], [3.99, 5], [4, 5], [5, 5], [1, 0]].map(([s, b]) => level(s, b)),
    ["ok", "ok", "warn", "over", "over"]);
});

test("the status bar reads spent / budget", () => {
  assert.equal(budgetText({ spent: 0.25, budget: 10 }), "$0.25 / $10");
});

test("a school that shows euros gets them, written the French way in French", () => {
  // The space before € is a no-break one, narrow or not depending on ICU.
  const sp = (s: string) => s.replace(/[\u00a0\u202f]/g, " ");
  const nb = " ";
  assert.equal(sp(money(4.96, "EUR", "fr")), `4,96${nb}€`);
  assert.equal(sp(money(50, "EUR", "fr")), `50${nb}€`);
  assert.equal(sp(money(0.004, "EUR", "fr")), `<0,01${nb}€`);
  assert.equal(money(4.96, "EUR", "en"), "€4.96");
  assert.equal(sp(budgetText({ spent: 4.96, budget: 50, currency: "EUR" }, "fr")), `4,96${nb}€ / 50${nb}€`);
});
