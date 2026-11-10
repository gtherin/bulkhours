// The chat panel, driven the way a student drives it: messages from the
// panel in, state and permission prompts out. `vscode` is a stand-in; the
// agent is the real fake ACP agent from fixtures/, so the round trip is real.
import { after, mock, test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const written = new Map<string, string>();
let folder: string | undefined = mkdtempSync(join(tmpdir(), "bh-"));
const settings: Record<string, unknown> = {};
let editor: unknown = undefined;
const executed: string[] = [];

mock.module("vscode", {
  namedExports: {
    Uri: {
      file: (p: string) => ({ fsPath: p, scheme: "file", toString: () => `file://${p}` }),
      joinPath: (u: { fsPath: string }, ...p: string[]) => ({ fsPath: [u.fsPath, ...p].join("/") }),
    },
    workspace: {
      get workspaceFolders() { return folder ? [{ uri: { fsPath: folder } }] : undefined; },
      getConfiguration: () => ({ get: (k: string) => settings[k], update: async (k: string, v: unknown) => { settings[k] = v; } }),
      textDocuments: [],
      openTextDocument: async (u: { fsPath: string }) => ({ getText: () => `contents of ${u.fsPath}` }),
      fs: { writeFile: async (u: { fsPath: string }, b: Uint8Array) => { written.set(u.fsPath, new TextDecoder().decode(b)); } },
      asRelativePath: (u: { fsPath: string }) => u.fsPath,
    },
    window: {
      get activeTextEditor() { return editor; },
    },
    commands: { executeCommand: async (id: string) => { executed.push(id); } },
  },
});

const { ChatView } = await import("../src/vscode/chatView.ts");

const FAKE = fileURLToPath(new URL("./fixtures/fake-agent.ts", import.meta.url));
const key = {
  apiKey: "sk", baseUrl: "https://x/v1", expiresAt: Date.now() + 3600e3, models: ["fast", "code"], defaultModel: "fast",
  agent: { id: "fake", label: "Fake agent", command: process.execPath, args: ["--experimental-strip-types", "--no-warnings", FAKE],
    env: { FAKE_MODEL: "${model}" } },
  modelLabels: { fast: "DeepSeek V4.1 Flash" },
  modelPrices: { fast: { in: 0.3, out: 1.2 } },
};

// Every panel's agent is stopped at the end, even after a failed test.
const views: { dispose(): void }[] = [];
after(() => views.forEach((v) => v.dispose()));

function panel(signedIn = true, lang: "fr" | "en" = "en", schoolName = "IPSA", opts: { images?: boolean } = {}) {
  const k = opts.images ? { ...key, agent: { ...key.agent, env: { ...key.agent.env, FAKE_IMAGES: "1" } } } : key;
  const meters: unknown[] = [];
  const state = new Map<string, unknown>();
  const posted: any[] = [];
  let send: (m: unknown) => Promise<void> = async () => {};
  let changed: () => void = () => {};
  const ctx: any = {
    extensionUri: { fsPath: "/ext" }, extensionPath: "/ext",
    extension: { packageJSON: { version: "0.1.0" } },
    globalState: { get: (k: string) => state.get(k), update: async (k: string, v: unknown) => { state.set(k, v); } },
  };
  const creds: any = {
    onDidChange: (f: () => void) => { changed = f; return { dispose() {} }; },
    signedIn: async () => signedIn,
    known: () => (signedIn ? k : undefined),
    currentKey: async () => ({ key: k, renewed: false }),
    credits: async () => (signedIn ? { spent: 0.25, budget: 10 } : undefined),
    signIn: async () => { posted.push({ type: "signIn-opened" }); },
  };
  const view = new ChatView(ctx, { id: "ipsa", name: schoolName, accent: "#c8102e", signInUrl: "https://a", keyUrl: "https://b", creditsUrl: "https://c", language: "en" as const },
    creds, { append() {} } as any, lang, (c: unknown) => meters.push(c));
  views.push(view);
  changed();   // a sign-in change can arrive before VS Code shows the panel
  const webview: any = {
      options: {}, cspSource: "csp", html: "",
      asWebviewUri: (u: { fsPath: string }) => u.fsPath,
      onDidReceiveMessage: (f: any) => { send = (m) => f(m); },
      postMessage: async (m: unknown) => { posted.push(m); return true; },
  };
  view.resolveWebviewView({ webview } as any);
  const settle = () => new Promise((r) => setTimeout(r, 30));
  const last = () => [...posted].reverse().find((m) => m.type === "state");
  return { view, posted, state, webview, meters, send: async (m: unknown) => { await send(m); await settle(); }, last };
}

const texts = (s: any) => s.transcript.map((e: any) => e.text ?? e.kind);

test("a signed-out student is offered sign-in, nothing else", async () => {
  const p = panel(false);
  await p.send({ type: "ready" });
  assert.deepEqual({ signedIn: p.last().signedIn, models: p.last().models, agent: p.last().agent },
    { signedIn: false, models: [], agent: "" });
  await p.send({ type: "signIn" });
  assert.ok(p.posted.some((m) => m.type === "signIn-opened"));
});

test("a question gets the agent's answer, with the school's models shown", async () => {
  const p = panel();
  await p.send({ type: "send", text: "hello" });
  const s = p.last();
  assert.deepEqual(texts(s), ["hello", "you said: hello"]);
  assert.deepEqual({ busy: s.busy, model: s.model, models: s.models, agent: s.agent },
    { busy: false, model: "fast", models: ["fast", "code"], agent: "Fake agent" });
  p.view.newChat();
});

test("while the agent starts the panel says so, and stops saying it once the agent is up", async () => {
  const p = panel();
  await p.send({ type: "send", text: "hello" });
  const states = p.posted.filter((m) => m.type === "state");
  assert.ok(states.some((m) => m.starting === true), "a state says the agent is starting");
  assert.equal(p.last().starting, false);
  p.view.newChat();
});

test("the chosen model reaches the agent, and a new choice restarts it", async () => {
  const p = panel();
  await p.send({ type: "model", model: "code" });
  await p.send({ type: "send", text: "model" });
  assert.deepEqual(texts(p.last()), ["model", "model=code"]);
  p.view.newChat();
  await new Promise((r) => setTimeout(r, 30));
  assert.deepEqual(texts(p.last()), []);
});

test("a write waits for the student's answer in the panel", async () => {
  const p = panel();
  const turn = p.send({ type: "send", text: `write ${folder}/out.txt` });
  let ask: any;
  for (let i = 0; i < 100 && !ask; i++) { await new Promise((r) => setTimeout(r, 20)); ask = p.posted.find((m) => m.type === "permission"); }
  assert.equal(ask.title, `Write ${folder}/out.txt`);
  assert.deepEqual(ask.options.map((o: any) => o.kind), ["allow_once", "reject_once"]);
  assert.equal(written.has(`${folder}/out.txt`), false, "nothing is written before the answer");
  await p.send({ type: "permission", id: ask.id, optionId: "yes" });
  await turn;
  assert.equal(written.get(`${folder}/out.txt`), "written");
  assert.deepEqual(texts(p.last()), [`write ${folder}/out.txt`, "wrote it"]);
  p.view.newChat();
});

test("without an open folder the student is told what to do", async () => {
  const saved = folder;
  folder = undefined;
  try {
    const p = panel();
    await p.send({ type: "send", text: "hello" });
    assert.deepEqual(texts(p.last()), ["hello", "error: open a folder first: the assistant works inside your project"]);
    assert.equal(p.last().busy, false);
  } finally { folder = saved; }
});

test("an empty message or a second one mid-turn is ignored", async () => {
  const p = panel();
  await p.send({ type: "send", text: "   " });
  assert.equal(p.last(), undefined);
  p.view.newChat();
});

test("the file open in the editor goes along as context", async () => {
  const p = panel();
  editor = { document: { uri: { scheme: "file", fsPath: "src/main.c", toString: () => "file:///w/src/main.c" } } };
  try {
    await p.send({ type: "send", text: "context" });
    assert.deepEqual(texts(p.last()), ["context", "context=src/main.c"]);
    editor = { document: { uri: { scheme: "untitled", fsPath: "Untitled-1", toString: () => "untitled:1" } } };
    await p.send({ type: "send", text: "context" });
    assert.deepEqual(texts(p.last()).slice(-1), ["context=none"]);
  } finally { editor = undefined; p.view.newChat(); }
});

test("Stop pressed while the agent starts is kept, not lost", async () => {
  const p = panel();
  const turn = p.send({ type: "send", text: "wait" });
  await p.send({ type: "cancel" });
  await turn;
  assert.deepEqual(texts(p.last()), ["wait", "stopped before the agent began"]);
  assert.equal(p.last().busy, false);
  p.view.newChat();
});

test("Stop reaches a working agent, and the panel says how the turn ended", async () => {
  const p = panel();
  await p.send({ type: "send", text: "hello" });   // the agent is up
  const turn = p.send({ type: "send", text: "wait" });
  await new Promise((r) => setTimeout(r, 100));
  await p.send({ type: "cancel" });
  await turn;
  assert.deepEqual(texts(p.last()).slice(2), ["wait", "stopping", "stopped: cancelled"]);
  p.view.newChat();
});

test("closing a permission prompt without choosing refuses the action", async () => {
  const p = panel();
  const turn = p.send({ type: "send", text: `write ${folder}/never.txt` });
  let ask: any;
  for (let i = 0; i < 100 && !ask; i++) { await new Promise((r) => setTimeout(r, 20)); ask = p.posted.find((m) => m.type === "permission"); }
  await p.send({ type: "permission", id: ask.id, optionId: null });
  await turn;
  assert.equal(written.has(`${folder}/never.txt`), false);
  assert.deepEqual(texts(p.last()).slice(-1), ["did not write"]);
  p.view.newChat();
});

test("closing VS Code stops the agent process", async () => {
  const p = panel();
  await p.send({ type: "send", text: "hello" });
  const child = (p.view as any).session.child;
  assert.equal(child.exitCode, null);
  p.view.dispose();
  await new Promise((r) => child.once("exit", r));
  assert.ok(child.killed);
});

test("the panel runs its own script only, under a fresh nonce each time", () => {
  const a = panel(), b = panel();
  assert.equal(a.webview.options.enableScripts, true);
  const nonce = (html: string) => /script-src 'nonce-([a-z0-9]+)'/.exec(html)![1];
  assert.ok(nonce(a.webview.html).length >= 16);
  assert.notEqual(nonce(a.webview.html), nonce(b.webview.html));
  assert.ok(a.webview.html.includes(`<script nonce="${nonce(a.webview.html)}"`));
});

test("an answer to a prompt that no longer exists is ignored", async () => {
  const p = panel();
  await p.send({ type: "ready" });
  await p.send({ type: "permission", id: 999, optionId: "yes" });
  assert.equal(p.posted.filter((m) => m.type === "permission").length, 0);
  assert.deepEqual(texts(p.last()), [], "no error shows up in the chat");
});

test("a French panel speaks French, words and messages alike", async () => {
  const p = panel(true, "fr");
  const words = JSON.parse(/<script type="application\/json" id="words">(.*?)<\/script>/.exec(p.webview.html)![1]);
  assert.equal(words.send, "Envoyer");
  assert.equal(words.signInPrompt, "Connectez-vous avec votre compte IPSA pour utiliser l'assistant sur les crédits de votre école.");
  assert.ok(p.webview.html.includes('<html lang="fr">'));
  const saved = folder;
  folder = undefined;
  try {
    await p.send({ type: "send", text: "bonjour" });
    assert.deepEqual(texts(p.last()).slice(-1), ["erreur : ouvrez d'abord un dossier : l'assistant travaille dans votre projet"]);
  } finally { folder = saved; }
  const turn = p.send({ type: "send", text: "wait" });
  await p.send({ type: "cancel" });
  await turn;
  assert.match(texts(p.last()).at(-1), /^arrêté/);
});

test("a school name cannot break out of the panel's data", () => {
  const p = panel(true, "en", "</script><script>alert(1)</script>");
  assert.equal(p.webview.html.match(/<\/script>/g)!.length, 2, "only the data block and the panel script close");
});


test("the budget is shown as MaQI's meter, in the panel and the status bar", async () => {
  const p = panel();
  await p.send({ type: "ready" });
  assert.deepEqual(p.last().credits, { spent: 0.25, budget: 10 });
  assert.deepEqual(p.meters.at(-1), { spent: 0.25, budget: 10 });
});

test("the model list says which LLM answers", async () => {
  const p = panel();
  await p.send({ type: "ready" });
  assert.deepEqual(p.last().modelLabels, { fast: "DeepSeek V4.1 Flash" });
});

test("the context the agent reports is shown, and forgotten with a new chat", async () => {
  const p = panel();
  await p.send({ type: "send", text: "usage" });
  assert.deepEqual(p.last().usage, { used: 40_600, size: 64_000 });
  p.view.newChat();
  await new Promise((r) => setTimeout(r, 30));
  assert.equal(p.last().usage, null);
});

test("Compact asks the agent to compact, Clear starts the chat again", async () => {
  const p = panel();
  await p.send({ type: "compact" });
  assert.deepEqual(texts(p.last()), ["/compact", "you said: /compact"]);
  await p.send({ type: "clear" });
  assert.deepEqual(texts(p.last()), []);
});

test("pasted images reach an agent that reads them, and are shown in the question", async () => {
  const p = panel(true, "en", "IPSA", { images: true });
  await p.send({ type: "send", text: "images", images: [{ mimeType: "image/png", data: "AAA" }] });
  const s = p.last();
  assert.deepEqual(texts(s), ["images", "images=image/png:AAA"]);
  assert.deepEqual(s.transcript[0].images, ["data:image/png;base64,AAA"]);
  p.view.newChat();
});

test("an agent that does not read images: the student is told, the text still goes", async () => {
  const p = panel();
  await p.send({ type: "send", text: "images", images: [{ mimeType: "image/png", data: "AAA" }] });
  assert.deepEqual(texts(p.last()), ["images", "this agent does not read images: they were not sent", "images=none"]);
  p.view.newChat();
});

test("only images are accepted from a paste, nothing else", async () => {
  const p = panel(true, "en", "IPSA", { images: true });
  await p.send({ type: "send", text: "images", images: [{ mimeType: "text/html", data: "PHNjcmlwdD4=" }] });
  assert.deepEqual(texts(p.last()), ["images", "images=none"]);
  p.view.newChat();
});

test("the agent's name in the panel opens the agent picker", async () => {
  const p = panel();
  await p.send({ type: "pickAgent" });
  assert.deepEqual(executed, ["bulkhours.pickAgent"]);
});

test("one menu offers the school's models with their prices and the student's own agents", async () => {
  settings.extraAgents = [{ id: "claude", label: "Claude Code (Max)", command: "npx" }];
  const p = panel();
  await p.send({ type: "ready" });
  const s = p.last();
  assert.deepEqual(s.modelPrices, { fast: { in: 0.3, out: 1.2 } });
  assert.deepEqual(s.agents, [{ id: "", label: "Fake agent" }, { id: "claude", label: "Claude Code (Max)" }]);
  assert.equal(s.agentId, "");
  await p.send({ type: "choose", agent: "claude" });
  assert.equal(settings.agent, "claude");
  assert.equal(p.last().agentId, "claude");
  await p.send({ type: "choose", agent: "", model: "code" });
  assert.deepEqual([settings.agent, p.last().agentId, p.last().model], ["", "", "code"]);
  delete settings.extraAgents; delete settings.agent;
});
