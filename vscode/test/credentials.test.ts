// Sign-in and keys, against a stand-in `vscode` and a fake key server.
import { mock, test } from "node:test";
import assert from "node:assert/strict";

const opened: string[] = [];
const warnings: string[] = [];
class EventEmitter { private l: (() => void)[] = []; event = (f: () => void) => { this.l.push(f); return { dispose() {} }; }; fire() { this.l.forEach((f) => f()); } }
mock.module("vscode", {
  namedExports: {
    EventEmitter,
    Uri: { parse: (s: string) => ({ toString: () => s }) },
    env: {
      uriScheme: "vscode",
      asExternalUri: async (u: unknown) => u,
      openExternal: async (u: { toString(): string }) => { opened.push(u.toString()); return true; },
    },
    window: { showWarningMessage: async (m: string) => { warnings.push(m); } },
  },
});
const { Credentials } = await import("../src/vscode/credentials.ts");

const school = { id: "ipsa", name: "IPSA", accent: "#c8102e", signInUrl: "https://bh.fr/sign-in?school=ipsa", keyUrl: "https://bh.fr/api/workbench/key", language: "en" as const };
const reply = (minutes: number) => ({
  key: `sk-${minutes}`, base_url: "https://llm.bh.fr/v1", expires_at: new Date(Date.now() + minutes * 60e3).toISOString(),
  models: ["fast"], agent: { id: "gateka", label: "Gateka", command: "dsh" },
});

function setup(answer: { status: number; body?: unknown }) {
  const store = new Map<string, string>();
  const secrets: any = { get: async (k: string) => store.get(k), store: async (k: string, v: string) => { store.set(k, v); }, delete: async (k: string) => { store.delete(k); } };
  const calls: { auth: string | null; body: string }[] = [];
  globalThis.fetch = (async (_url: string, init: any) => {
    calls.push({ auth: init.headers.authorization, body: init.body });
    return { status: answer.status, json: async () => answer.body };
  }) as any;
  const c = new Credentials(secrets, school, "bulkhours.bulkhours-ipsa");
  let changes = 0;
  c.onDidChange(() => changes++);
  return { c, store, calls, changes: () => changes };
}

async function signIn(c: InstanceType<typeof Credentials>, token = "tok") {
  opened.length = 0;
  await c.signIn();
  const url = new URL(opened[0]);
  await c.handleUri({ path: "/signed-in", query: `state=${url.searchParams.get("state")}&token=${token}` } as any);
  return url;
}

test("sign-in opens the school's page with a way back, then fetches a key", async () => {
  const s = setup({ status: 200, body: reply(720) });
  const url = await signIn(s.c);
  assert.equal(url.origin + url.pathname, "https://bh.fr/sign-in");
  assert.equal(url.searchParams.get("school"), "ipsa");
  assert.equal(url.searchParams.get("redirect"), "vscode://bulkhours.bulkhours-ipsa/signed-in");
  assert.equal(await s.c.signedIn(), true);
  assert.deepEqual(s.calls, [{ auth: "Bearer tok", body: JSON.stringify({ school: "ipsa" }) }]);
  assert.equal(s.c.known()?.apiKey, "sk-720");
  assert.equal(s.changes(), 1);
});

test("a sign-in link this window did not ask for is ignored", async () => {
  const s = setup({ status: 200, body: reply(720) });
  warnings.length = 0;
  await s.c.handleUri({ path: "/signed-in", query: "state=forged&token=evil" } as any);
  assert.equal(await s.c.signedIn(), false);
  assert.equal(warnings.length, 1);
});

test("a fresh key is reused; one near expiry is renewed and says so", async () => {
  const s = setup({ status: 200, body: reply(720) });
  await signIn(s.c);
  assert.deepEqual((await s.c.currentKey()).renewed, false);
  const t = setup({ status: 200, body: reply(5) });
  await signIn(t.c);
  const again = await t.c.currentKey();
  assert.equal(again.renewed, true);
  assert.equal(t.calls.length, 2);
});

test("an expired session signs the student out", async () => {
  const s = setup({ status: 200, body: reply(5) });
  await signIn(s.c);
  globalThis.fetch = (async () => ({ status: 401, json: async () => ({}) })) as any;
  await assert.rejects(s.c.currentKey(), /your BulkHours session expired: sign in again/);
  assert.equal(await s.c.signedIn(), false);
  assert.equal(s.c.known(), undefined);
});

test("no credits left is said plainly, and the student stays signed in", async () => {
  const s = setup({ status: 402 });
  await assert.rejects(signIn(s.c), /no credits left for this period/);
  assert.equal(await s.c.signedIn(), true);
});

test("asking for a key before sign-in is refused", async () => {
  const s = setup({ status: 200, body: reply(720) });
  await assert.rejects(s.c.currentKey(), /not signed in/);
  assert.equal(s.calls.length, 0);
});

test("signing out forgets the token and the key", async () => {
  const s = setup({ status: 200, body: reply(720) });
  await signIn(s.c);
  await s.c.signOut();
  assert.equal(await s.c.signedIn(), false);
  assert.equal(s.c.known(), undefined);
});
