// Activation and the agent picker, against a stand-in `vscode`.
import { mock, test } from "node:test";
import assert from "node:assert/strict";

const registered = { commands: [] as string[], views: [] as string[], uri: 0 };
const info: string[] = [];
const settings: Record<string, unknown> = {};
const updates: [string, unknown, boolean][] = [];
let quickPick: (items: any[]) => any = () => undefined;
const offered: any[][] = [];
class EventEmitter { event = () => ({ dispose() {} }); fire() {} }
const disposable = { dispose() {} };
let viewOptions: any;
mock.module("vscode", {
  namedExports: {
    EventEmitter,
    window: {
      createOutputChannel: () => ({ append() {}, dispose() {} }),
      registerUriHandler: () => { registered.uri++; return disposable; },
      registerWebviewViewProvider: (id: string, _p: unknown, o: any) => { registered.views.push(id); viewOptions = o; return disposable; },
      showInformationMessage: async (m: string) => { info.push(m); },
      showQuickPick: async (items: any[]) => { offered.push(items); return quickPick(items); },
    },
    env: { language: "en" },
    commands: { registerCommand: (id: string) => { registered.commands.push(id); return disposable; } },
    workspace: {
      getConfiguration: () => ({ get: (k: string) => settings[k], update: async (k: string, v: unknown, global: boolean) => { updates.push([k, v, global]); } }),
    },
  },
});
(globalThis as any).__SCHOOL__ = { id: "ipsa", name: "IPSA", accent: "#c8102e", signInUrl: "https://a", keyUrl: "https://b" };
const { activate, pickAgent, deactivate } = await import("../src/vscode/extension.ts");

test("activation registers the panel, the sign-in link and four commands", () => {
  const ctx: any = { subscriptions: [], secrets: {}, extension: { id: "bulkhours.bulkhours-ipsa" } };
  activate(ctx);
  deactivate();
  assert.deepEqual(registered, {
    commands: ["bulkhours.newChat", "bulkhours.signIn", "bulkhours.signOut", "bulkhours.pickAgent"],
    views: ["bulkhours.chat"], uri: 1,
  });
  assert.equal(ctx.subscriptions.length, 8);
  assert.equal(viewOptions.webviewOptions.retainContextWhenHidden, true, "a hidden panel keeps its conversation");
});

const school = { id: "gateka", label: "Gateka", command: "dsh", args: [], env: {} };
let cleared = 0;
const chat = { newChat: () => { cleared++; } };

test("the picker offers the school's agent and the student's own", async () => {
  settings.extraAgents = [{ id: "opencode", label: "OpenCode", command: "opencode" }];
  quickPick = (items) => items[1];
  await pickAgent({ known: () => ({ agent: school }) as any }, chat);
  assert.deepEqual(offered.at(-1)!.map((i: any) => [i.label, i.id]), [["Gateka", ""], ["OpenCode", "opencode"]]);
  assert.deepEqual(updates.at(-1), ["agent", "opencode", true]);
  assert.equal(cleared, 1);
});

test("closing the picker changes nothing", async () => {
  quickPick = () => undefined;
  const before = updates.length;
  await pickAgent({ known: () => ({ agent: school }) as any }, chat);
  assert.equal(updates.length, before);
  assert.equal(cleared, 1);
});

test("with nothing to offer, the student is told how to get an agent", async () => {
  settings.extraAgents = [];
  await pickAgent({ known: () => undefined }, chat);
  assert.deepEqual(info, ["Sign in first, or add agents in bulkhours.extraAgents."]);
});
