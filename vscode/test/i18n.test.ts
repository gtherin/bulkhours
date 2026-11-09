import { test } from "node:test";
import assert from "node:assert/strict";
import { MESSAGES, pickLang, t } from "../src/core/i18n.ts";

test("VS Code's display language wins when we speak it, else the school's", () => {
  assert.equal(pickLang("fr", "en"), "fr");
  assert.equal(pickLang("fr-CA", "en"), "fr");
  assert.equal(pickLang("en-US", "fr"), "en");
  assert.equal(pickLang("de", "fr"), "fr");
  assert.equal(pickLang("", "fr"), "fr");
});

test("every message exists in every language, with the same placeholders", () => {
  const holes = (s: string) => [...s.matchAll(/\{(\w+)\}/g)].map((m) => m[1]).sort().join(",");
  const keys = Object.keys(MESSAGES.en).sort();
  assert.deepEqual(Object.keys(MESSAGES.fr).sort(), keys);
  for (const k of keys) {
    const en = MESSAGES.en[k as keyof typeof MESSAGES.en];
    const fr = MESSAGES.fr[k as keyof typeof MESSAGES.fr];
    assert.ok(fr.trim() && fr !== en || /^[A-Z]/.test(en), `${k} looks untranslated`);
    assert.equal(holes(fr), holes(en), `${k}: placeholders differ`);
  }
});

test("placeholders are filled, and a missing value is refused", () => {
  assert.equal(t("fr", "keyServerAnswered", { status: 503 }), "le serveur de clés a répondu 503");
  assert.equal(t("en", "keyServerAnswered", { status: 503 }), "the key server answered 503");
  assert.throws(() => t("fr", "keyServerAnswered"), /missing value "status" for message keyServerAnswered/);
});

test("how a turn ended reads in the student's language", () => {
  assert.equal(t("fr", "stopped", { reason: t("fr", "reason_cancelled") }), "arrêté : annulé");
  assert.equal(t("en", "stopped", { reason: t("en", "reason_max_tokens") }), "stopped: the answer reached its length limit");
});
