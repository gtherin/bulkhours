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
