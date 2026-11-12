// MaQI's own connection (owner 2026-11-12; architect a39340): the key file
// the platform writes and renews is the sign-in.
import { mock, test } from "node:test";
import assert from "node:assert/strict";

const warnings: string[] = [];
class EventEmitter { event = () => ({ dispose() {} }); fire() {} }
mock.module("vscode", { namedExports: { EventEmitter, window: { showWarningMessage: async (m: string) => { warnings.push(m); } } } });
const { PlatformKeys } = await import("../src/vscode/platformKeys.ts");
const { setBrand } = await import("../src/core/i18n.ts");
setBrand("MaQI");

test("on its platform a variant reads the key file: no sign-in, a rotated key restarts the agent", async () => {
  const { mkdtempSync, writeFileSync, rmSync } = await import("node:fs");
  const { join } = await import("node:path");
  const { tmpdir, userInfo } = await import("node:os");
  const dir = mkdtempSync(join(tmpdir(), "bh-keys-"));
  const file = join(dir, `${userInfo().username}.env`);
  const maqi: any = { id: "maqi", name: "MaQI", accent: "#61b45c", language: "en", title: "MaQI", prefix: "maqi",
    connection: { keyFile: join(dir, "${user}.env"), offer: { models: ["fast"], agent: { id: "maqi", label: "MaQI", command: "dsh" } } } };
  const c = new PlatformKeys(maqi.connection);
  assert.equal(await c.signedIn(), false, "no key file yet");
  await assert.rejects(c.currentKey(), (e: any) => e.key === "noKeyFile");
  writeFileSync(file, "OPENAI_API_KEY=sk-1\nOPENAI_BASE_URL=http://10.4.0.44:4000\n");
  assert.equal(await c.signedIn(), true);
  assert.deepEqual([(await c.currentKey()).key.apiKey, (await c.currentKey()).renewed], ["sk-1", false]);
  writeFileSync(file, "OPENAI_API_KEY=sk-2\nOPENAI_BASE_URL=http://10.4.0.44:4000\n");
  const next = await c.currentKey();
  assert.deepEqual([next.key.apiKey, next.renewed], ["sk-2", true]);
  assert.equal(await c.credits(), undefined);
  await c.signIn();
  assert.match(warnings.at(-1)!, /No MaQI key on this machine/);
  assert.equal(c.interactive, false);
  rmSync(dir, { recursive: true });
});

test("the meter reads the person's spend and cap from the platform's LiteLLM, with their key", async () => {
  const { mkdtempSync, writeFileSync } = await import("node:fs");
  const { join } = await import("node:path");
  const { tmpdir, userInfo } = await import("node:os");
  const dir = mkdtempSync(join(tmpdir(), "bh-keys-"));
  writeFileSync(join(dir, `${userInfo().username}.env`), "OPENAI_API_KEY=sk-9\nOPENAI_BASE_URL=http://10.4.0.44:4000\n");
  const calls: { url: string; auth: string }[] = [];
  globalThis.fetch = (async (url: string, init: any) => {
    calls.push({ url, auth: init.headers.authorization });
    const body = url.endsWith("/key/info") ? { info: { user_id: "u", team_id: "research" } }
      : { teams: [{ team_id: "research", team_memberships: [{ user_id: "u", spend: 3.2, litellm_budget_table: { max_budget: 200 } }] }] };
    return { status: 200, json: async () => body };
  }) as any;
  const c = new PlatformKeys({ keyFile: join(dir, "${user}.env"), offer: { models: ["fast"], currency: "EUR", agent: { id: "maqi", label: "MaQI", command: "dsh" } } });
  assert.deepEqual(await c.credits(), { spent: 3.2, budget: 200, currency: "EUR" });
  assert.equal((await c.currentKey()).renewed, true, "the meter never takes the turn's notice of a new key");
  assert.deepEqual(calls.map((x) => [x.url, x.auth]), [["http://10.4.0.44:4000/key/info", "Bearer sk-9"], ["http://10.4.0.44:4000/user/info", "Bearer sk-9"]]);
  globalThis.fetch = (async () => { throw new Error("down"); }) as any;
  assert.equal(await c.credits(), undefined, "a platform that cannot be read shows no meter, never an error");
});
