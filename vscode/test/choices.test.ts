import { test } from "node:test";
import assert from "node:assert/strict";
import { chooseAgent, chooseModel, keyFailure, signInToken, sliceLines } from "../src/core/choices.ts";
import { t } from "../src/core/i18n.ts";
import type { Key } from "../src/core/keys.ts";

const school = { id: "gateka", label: "Gateka", command: "dsh", args: [], env: {} };
const mine = { id: "opencode", label: "OpenCode", command: "opencode", args: ["acp"], env: {} };
const key: Key = {
  apiKey: "sk", baseUrl: "https://x/v1", expiresAt: 0, models: ["fast", "code"], defaultModel: "fast", agent: school, modelLabels: {}, modelPrices: {}, modelVision: [], currency: "USD",
};

test("the student's model choice holds while the school still offers it", () => {
  assert.equal(chooseModel("code", key), "code");
  assert.equal(chooseModel("frontier", key), "fast");
  assert.equal(chooseModel(undefined, key), "fast");
  assert.equal(chooseModel("code", undefined), "code");
  assert.equal(chooseModel(undefined, undefined), "");
});

test("the school's agent unless the student picked one of their own", () => {
  assert.equal(chooseAgent(key, [mine], "").id, "gateka");
  assert.equal(chooseAgent(key, [mine], "opencode").id, "opencode");
  assert.equal(chooseAgent(key, [mine], "vanished").id, "gateka");
  assert.equal(chooseAgent(undefined, [mine], "").id, "opencode");
  assert.throws(() => chooseAgent(undefined, [], ""), /no agent configured/);
});

test("an agent may read part of a file, counted from line 1", () => {
  const text = "a\nb\nc\nd";
  assert.equal(sliceLines(text), text);
  assert.equal(sliceLines(text, 2), "b\nc\nd");
  assert.equal(sliceLines(text, 2, 2), "b\nc");
  assert.equal(sliceLines(text, null, 1), "a");
  assert.equal(sliceLines(text, 0, 1), "a");
});

test("each key server answer says what the student should do", () => {
  const said = (status: number) => { const e = keyFailure(status); return e && t("fr", e.key, e.vars); };
  assert.equal(keyFailure(200), null);
  assert.equal(keyFailure(204), null);
  assert.equal(said(300), "le serveur de clés a répondu 300");
  assert.equal(said(401), "votre session BulkHours a expiré : reconnectez-vous");
  assert.equal(said(402), "plus de crédits pour cette période");
  assert.equal(keyFailure(503)?.message, "the key server answered 503");
});

test("a sign-in link counts only if this window asked for it", () => {
  assert.deepEqual(signInToken("/signed-in", "state=s1&token=t1", "s1"), { token: "t1" });
  assert.deepEqual(signInToken("/signed-in", "state=other&token=t1", "s1"), { ignored: true });
  assert.deepEqual(signInToken("/signed-in", "state=s1&token=t1", undefined), { ignored: true });
  assert.deepEqual(signInToken("/elsewhere", "state=s1&token=t1", "s1"), { ignored: true });
  assert.throws(() => signInToken("/signed-in", "state=s1", "s1"), /the sign-in page sent no token/);
});
