import { test } from "node:test";
import assert from "node:assert/strict";
import { needsRenewal, parseKeyReply } from "../src/core/keys.ts";

const reply = {
  key: "sk-1",
  base_url: "https://llm.bulkhours.fr/v1",
  expires_at: "2026-11-09T22:00:00Z",
  models: ["fast", "code"],
  default_model: "fast",
  agent: {
    id: "gateka", label: "Gateka (DeepSeek)", command: "npx",
    args: ["-y", "@deepseek-ai/dsh", "--profile", "acp"],
    env: { OPENAI_BASE_URL: "${baseUrl}", OPENAI_API_KEY: "${apiKey}" },
  },
};

test("a key reply is read once, where it enters, agent and models included", () => {
  assert.deepEqual(parseKeyReply(reply), {
    apiKey: "sk-1", baseUrl: "https://llm.bulkhours.fr/v1", expiresAt: Date.parse("2026-11-09T22:00:00Z"),
    models: ["fast", "code"], defaultModel: "fast",
    agent: { ...reply.agent }, modelLabels: {}, modelPrices: {}, modelVision: [], currency: "USD",
  });
});

test("model names are kept for offered models only, and are optional", () => {
  const k = parseKeyReply({ ...reply, model_labels: { fast: "DeepSeek V4.1 Flash", other: "x", code: 3 } });
  assert.deepEqual(k.modelLabels, { fast: "DeepSeek V4.1 Flash" });
});

test("a reply without a key or with a bad date is refused", () => {
  assert.throws(() => parseKeyReply({ ...reply, key: undefined }), /key server: "key" missing/);
  assert.throws(() => parseKeyReply({ ...reply, expires_at: "soon" }), /key server: "expires_at" is not a date/);
  assert.throws(() => parseKeyReply({ ...reply, base_url: "http://x" }), /key server: "base_url" must be https/);
});

test("the server decides the agent: a reply without one is refused", () => {
  assert.throws(() => parseKeyReply({ ...reply, agent: undefined }), /key server: agent 1: "id" must be a non-empty string/);
});

test("the default model must be one of the offered models", () => {
  assert.throws(() => parseKeyReply({ ...reply, default_model: "frontier" }), /key server: default model "frontier" is not offered/);
  assert.throws(() => parseKeyReply({ ...reply, models: [] }), /key server: "models" must be a non-empty list/);
});

test("a key is renewed ten minutes before it expires, not after", () => {
  const exp = Date.parse("2026-11-09T22:00:00Z");
  assert.equal(needsRenewal(exp, Date.parse("2026-11-09T21:49:00Z")), false);
  assert.equal(needsRenewal(exp, Date.parse("2026-11-09T21:51:00Z")), true);
  assert.equal(needsRenewal(exp, Date.parse("2026-11-09T23:00:00Z")), true);
});

test("a reply without a default model takes the first offered", () => {
  assert.equal(parseKeyReply({ ...reply, default_model: undefined }).defaultModel, "fast");
});

test("nothing at all is refused, not crashed on", () => {
  assert.throws(() => parseKeyReply(null), /key server: "key" missing/);
  assert.throws(() => parseKeyReply({ ...reply, models: ["fast", 3] }), /"models" must be a non-empty list/);
});

test("a key that is not text is refused", () => {
  assert.throws(() => parseKeyReply({ ...reply, key: 12345 }), /key server: "key" missing/);
});

test("renewal starts exactly ten minutes before expiry", () => {
  const exp = Date.parse("2026-11-09T22:00:00Z");
  assert.equal(needsRenewal(exp, exp - 10 * 60 * 1000), true);
  assert.equal(needsRenewal(exp, exp - 10 * 60 * 1000 - 1), false);
});

test("model prices are kept for offered models only, as two numbers", () => {
  const k = parseKeyReply({ ...reply, model_prices: { fast: { in: 0.3, out: 1.2 }, code: { in: "x" }, other: { in: 1, out: 2 } } });
  assert.deepEqual(k.modelPrices, { fast: { in: 0.3, out: 1.2 } });
});

test("the school's currency comes with the key, dollars unless it says euros", () => {
  assert.equal(parseKeyReply({ ...reply, currency: "EUR" }).currency, "EUR");
  assert.equal(parseKeyReply({ ...reply, currency: "GBP" }).currency, "USD");
});

test("the models that read images are kept, offered ones only", () => {
  assert.deepEqual(parseKeyReply({ ...reply, model_vision: ["fast", "other", 3] }).modelVision, ["fast"]);
});
