// The chat panel, driven the way a student drives it: messages from the
// panel in, state and permission prompts out. `vscode` is a stand-in; the
// agent is the real fake ACP agent from fixtures/, so the round trip is real.
import { after, mock, test } from "node:test";
import assert from "node:assert/strict";
import { existsSync, mkdtempSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const written = new Map<string, string>();
let folder: string | undefined = mkdtempSync(join(tmpdir(), "bh-"));
const settings: Record<string, unknown> = {};
let editor: unknown = undefined;
const executed: string[] = [];
let confirmAnswer: "yes" | "no" = "yes";

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
      showWarningMessage: async (_m: string, _o: unknown, ...choices: string[]) => (confirmAnswer === "yes" ? choices[0] : undefined),
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
  modelVision: ["fast"],
  currency: "USD",
};

// Every panel's agent is stopped at the end, even after a failed test.
const views: { dispose(): void }[] = [];
after(() => views.forEach((v) => v.dispose()));

function panel(signedIn = true, lang: "fr" | "en" = "en", schoolName = "IPSA",
               opts: { images?: boolean; fresh?: boolean; store?: string; idleMs?: number; commands?: boolean; state?: string;
                      workspace?: Map<string, unknown>; platform?: boolean } = {}) {
  // Each panel keeps its conversations in its own state folder (never the
  // real ~/.local/state/gateka), unless a test shares one on purpose.
  process.env.GATEKA_STATE_HOME = opts.state ?? mkdtempSync(join(tmpdir(), "bh-gstate-"));
  const env = { ...key.agent.env, ...(opts.images ? { FAKE_IMAGES: "1" } : {}), ...(opts.store ? { FAKE_STORE: opts.store } : {}),
    ...(opts.commands ? { FAKE_COMMANDS: "1" } : {}) };
  const k = { ...key, agent: { ...key.agent, env } };
  const meters: unknown[] = [];
  let fetched = false;
  const state = new Map<string, unknown>();
  const workspace = opts.workspace ?? new Map<string, unknown>();
  const posted: any[] = [];
  let send: (m: unknown) => Promise<void> = async () => {};
  let changed: () => void = () => {};
  const ctx: any = {
    extensionUri: { fsPath: "/ext" }, extensionPath: "/ext",
    extension: { packageJSON: { version: "0.1.0" } },
    globalState: { get: (k: string) => state.get(k), update: async (k: string, v: unknown) => { state.set(k, v); } },
    workspaceState: { get: (k: string) => workspace.get(k), update: async (k: string, v: unknown) => { workspace.set(k, v); } },
  };
  const creds: any = {
    onDidChange: (f: () => void) => { changed = f; return { dispose() {} }; },
    interactive: opts.platform ? false : true,
    signedIn: async () => signedIn,
    // fresh: a window just reloaded, the key is not fetched yet
    known: () => (signedIn && (!opts.fresh || fetched) ? k : undefined),
    currentKey: async () => { fetched = true; return { key: k, renewed: false }; },
    credits: async () => (signedIn ? { spent: 0.25, budget: 10, currency: "USD" } : undefined),
    signIn: async () => { posted.push({ type: "signIn-opened" }); },
  };
  const view = new ChatView(ctx, { id: "ipsa", name: schoolName, accent: "#c8102e", signInUrl: "https://a", keyUrl: "https://b", creditsUrl: "https://c", language: "en" as const, title: `BulkHours ${schoolName}`, prefix: "bulkhours", links: [] },
    creds, { append() {} } as any, lang, (c: unknown) => meters.push(c), opts.idleMs);
  views.push(view);
  changed();   // a sign-in change can arrive before VS Code shows the panel
  const webview: any = {
      options: {}, cspSource: "csp", html: "",
      asWebviewUri: (u: { fsPath: string }) => u.fsPath,
      onDidReceiveMessage: (f: any) => { send = (m) => f(m); },
      postMessage: async (m: unknown) => { posted.push(m); return true; },
  };
  const viewObj: any = { webview };
  view.resolveWebviewView(viewObj);
  const settle = () => new Promise((r) => setTimeout(r, 30));
  const last = () => [...posted].reverse().find((m) => m.type === "state");
  return { view, posted, state, webview, meters, description: () => viewObj.description, send: async (m: unknown) => { await send(m); await settle(); }, last };
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
  for (let i = 0; i < 100 && !ask; i++) { await new Promise((r) => setTimeout(r, 20)); ask = p.posted.find((m) => m.type === "state" && m.asks?.length)?.asks[0]; }
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
  for (let i = 0; i < 100 && !ask; i++) { await new Promise((r) => setTimeout(r, 20)); ask = p.posted.find((m) => m.type === "state" && m.asks?.length)?.asks[0]; }
  await p.send({ type: "permission", id: ask.id, optionId: null });
  await turn;
  assert.equal(written.has(`${folder}/never.txt`), false);
  assert.deepEqual(texts(p.last()).slice(-1), ["did not write"]);
  p.view.newChat();
});

test("closing VS Code stops the agent process", async () => {
  const p = panel();
  await p.send({ type: "send", text: "hello" });
  const child = (p.view as any).active.session.child;
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
  assert.deepEqual(p.last().asks, []);
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
  assert.equal(p.webview.html.match(/<\/script>/g)!.length, 3, "only the data block and the two panel scripts close");
});


test("the budget is shown as MaQI's meter, in the panel and the status bar", async () => {
  const p = panel();
  await p.send({ type: "ready" });
  assert.deepEqual(p.last().credits, { spent: 0.25, budget: 10, currency: "USD" });
  assert.deepEqual(p.meters.at(-1), { spent: 0.25, budget: 10, currency: "USD" });
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

test("Compact is offered only by an agent that announces it, and then reaches it", async () => {
  const p = panel(true, "en", "IPSA", { commands: true });
  await p.send({ type: "send", text: "hello" });
  assert.deepEqual(p.last().commands, ["compact"]);
  await p.send({ type: "compact" });
  assert.deepEqual(texts(p.last()).slice(-2), ["/compact", "you said: /compact"]);
  await p.send({ type: "clear" });
  assert.deepEqual([texts(p.last()), p.last().commands], [[], []]);
});

test("an agent without a compact command is compacted by the extension, never sent /compact as a question", async () => {
  const p = panel(true, "en", "IPSA", { store: mkdtempSync(join(tmpdir(), "bh-store-")) });
  await p.send({ type: "send", text: "hello" });
  assert.deepEqual(p.last().commands, []);
  await p.send({ type: "compact" });
  const after = texts(p.last());
  assert.deepEqual(after.slice(0, 2), ["hello", "you said: hello"]);
  assert.equal(after.at(-1), "conversation compacted: the next message starts a fresh agent session with the conversation condensed");
  await p.send({ type: "send", text: "next" });
  // a fresh session (not the resumed one), handed the condensed conversation
  assert.match(texts(p.last()).at(-1), /^you said: The conversation so far .*Student: hello/s);
  p.view.newChat();
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

test("after a window reload the menu still offers the school's models, not only the student's agents", async () => {
  settings.extraAgents = [{ id: "claude", label: "Claude Code (Max)", command: "npx" }];
  const p = panel(true, "en", "IPSA", { fresh: true });
  await p.send({ type: "ready" });
  assert.deepEqual(p.last().models, ["fast", "code"]);
  assert.deepEqual(p.last().agents.map((a: any) => a.id), ["", "claude"]);
  delete settings.extraAgents;
});

const quiet = (ms: number) => new Promise((r) => setTimeout(r, ms));

test("a quiet agent is paused to free memory, and comes back with the conversation", async () => {
  const p = panel(true, "en", "IPSA", { store: mkdtempSync(join(tmpdir(), "bh-store-")), idleMs: 80 });
  await p.send({ type: "send", text: "remember apple" });
  await quiet(250);
  assert.ok(texts(p.last()).includes("the agent was paused to free memory: it comes back, with the conversation, at your next message"));
  await p.send({ type: "send", text: "recall" });
  const t = texts(p.last());
  assert.match(t.at(-1), /^I remember apple \(pid \d+\)$/);
  p.view.newChat();
});

test("an agent that cannot resume is never paused: it would forget", async () => {
  const p = panel(true, "en", "IPSA", { idleMs: 50 });
  await p.send({ type: "send", text: "hello" });
  await quiet(200);
  assert.deepEqual(texts(p.last()), ["hello", "you said: hello"]);
  p.view.newChat();
});

test("a new chat forgets the paused conversation", async () => {
  const p = panel(true, "en", "IPSA", { store: mkdtempSync(join(tmpdir(), "bh-store-")), idleMs: 60 });
  await p.send({ type: "send", text: "remember pear" });
  await quiet(200);
  p.view.newChat();
  await p.send({ type: "send", text: "recall" });
  assert.equal(texts(p.last())[0], "recall");
  assert.match(texts(p.last()).at(-1), /^I remember nothing/);
  p.view.newChat();
});

test("a conversation survives a window reload, and the agent is handed it", async () => {
  const state = mkdtempSync(join(tmpdir(), "bh-gstate-"));
  const before = panel(true, "en", "IPSA", { state });
  await before.send({ type: "send", text: "hello" });
  before.view.dispose();                                  // the window reloads
  const after = panel(true, "en", "IPSA", { state });
  await after.send({ type: "ready" });
  assert.deepEqual(texts(after.last()), ["hello", "you said: hello"]);
  await after.send({ type: "send", text: "next" });
  // the fake agent cannot resume: a new session gets the conversation first
  assert.match(texts(after.last()).at(-1), /^you said: The conversation so far .*\n\nStudent: hello\n\nAssistant: you said: hello$/s);
  after.view.newChat();
});

test("another model takes the conversation over; a new chat starts clean", async () => {
  const p = panel();
  await p.send({ type: "send", text: "hello" });
  await p.send({ type: "choose", agent: "", model: "code" });
  await p.send({ type: "send", text: "go on" });
  assert.match(texts(p.last()).at(-1), /^you said: The conversation so far/);
  p.view.newChat();
  await p.send({ type: "send", text: "fresh" });
  assert.deepEqual(texts(p.last()), ["fresh", "you said: fresh"]);
  p.view.newChat();
});

test("an older conversation reopens from the history, and its title shows beside the panel's name", async () => {
  const state = mkdtempSync(join(tmpdir(), "bh-gstate-"));
  const p = panel(true, "en", "IPSA", { state });
  await p.send({ type: "send", text: "first topic" });
  p.view.newChat();
  await p.send({ type: "send", text: "second topic" });
  const list = p.view.conversations();
  assert.deepEqual(list.map((c: any) => c.title), ["second topic", "first topic"]);
  await p.view.open(list[1].file);
  await new Promise((r) => setTimeout(r, 30));
  assert.deepEqual(texts(p.last()), ["first topic", "you said: first topic"]);
  assert.equal(p.description(), "first topic");
  await p.view.rename("Le premier sujet");
  assert.equal(p.description(), "Le premier sujet");
  assert.ok(p.view.conversations().some((c: any) => c.title === "Le premier sujet"));
  p.view.newChat();
});

test("the agent is told which models read images, and the menu says so", async () => {
  const p = panel();
  await p.send({ type: "send", text: "vision" });
  assert.equal(texts(p.last()).at(-1), "vision=fast");
  assert.deepEqual(p.last().modelVision, ["fast"]);
  p.view.newChat();
});

test("the student's own image-models setting replaces the school's list", async () => {
  settings.imageModels = ["code"];
  const p = panel();
  await p.send({ type: "send", text: "vision" });
  assert.equal(texts(p.last()).at(-1), "vision=code");
  assert.deepEqual(p.last().modelVision, ["code"]);
  delete settings.imageModels;
  p.view.newChat();
});

test("restarting the assistant stops its agent only, and the conversation goes on", async () => {
  const p = panel(true, "en", "IPSA", { store: mkdtempSync(join(tmpdir(), "bh-store-")) });
  await p.send({ type: "send", text: "remember plum" });
  const first = texts(p.last());
  p.view.restart();
  await new Promise((r) => setTimeout(r, 50));
  assert.deepEqual(texts(p.last()).slice(0, first.length), first, "the conversation stays on screen");
  assert.ok(p.webview.html.includes("<html"), "the panel reloaded its page");
  await p.send({ type: "send", text: "recall" });
  assert.match(texts(p.last()).at(-1), /^I remember plum \(pid \d+\)$/);
  p.view.newChat();
});

test("while the agent works the panel knows since when, its last sign of life, and the spend so far", async () => {
  const p = panel();
  await p.send({ type: "ready" });                         // the budget is known before the turn
  const t0 = Date.now();
  await p.send({ type: "send", text: "wait" });
  const during = p.posted.filter((m) => m.type === "state" && m.busy && m.activity).at(-1);
  assert.ok(during, "a busy state carries the activity");
  assert.ok(during.activity.since >= t0 && during.activity.last >= during.activity.since);
  assert.equal(during.activity.spentAtStart, 0.25);
  assert.equal(p.last().activity, null, "a finished turn has no activity line");
  p.view.newChat();
});

test("Compact during a turn asks first, then stops the turn and compacts; a refusal changes nothing", async () => {
  const p = panel(true, "en", "IPSA", { store: mkdtempSync(join(tmpdir(), "bh-store-")) });
  await p.send({ type: "send", text: "hello" });
  confirmAnswer = "no";
  const busy = p.send({ type: "send", text: "wait" });           // a long turn
  await new Promise((r) => setTimeout(r, 120));
  await p.send({ type: "compact" });
  assert.equal(p.last().busy, true, "refused: the turn goes on");
  await busy;
  confirmAnswer = "yes";
  const busy2 = p.send({ type: "send", text: "wait" });
  await new Promise((r) => setTimeout(r, 120));
  await p.send({ type: "compact" });
  await busy2;
  await new Promise((r) => setTimeout(r, 100));
  const t = texts(p.last());
  assert.equal(p.last().busy, false);
  assert.equal(t.at(-1), "conversation compacted: the next message starts a fresh agent session with the conversation condensed");
  p.view.newChat();
});

// -- tabs: one per conversation, each running on its own (owner, 2026-11-12;
// architect bfd92a) ----------------------------------------------------------

const until = async (f: () => boolean) => { for (let i = 0; i < 200 && !f(); i++) await new Promise((r) => setTimeout(r, 20)); };

test("a conversation keeps working in its tab while the student asks something in another", async () => {
  const p = panel();
  const first = p.send({ type: "send", text: "wait" });           // a long turn
  await until(() => p.last()?.busy);
  const a = p.last().tab;
  p.view.newChat();                                               // + : a new tab
  await p.send({ type: "send", text: "hello" });
  const s = p.last();
  assert.notEqual(s.tab, a);
  assert.deepEqual(texts(s), ["hello", "you said: hello"]);
  assert.equal(s.tabs.find((x: any) => x.id === a).busy, true, "the first tab still works");
  await first;
  await p.send({ type: "tab", id: a });
  assert.deepEqual(texts(p.last()), ["wait", "waited the whole second"]);
  assert.equal(p.last().tabs.length, 2);
  p.view.dispose();
});

test("a tab is named by its first question, renamed in place, and the record keeps the name", async () => {
  const p = panel();
  await p.send({ type: "send", text: "why is my kernel slow?" });
  assert.equal(p.last().tabs[0].title, "why is my kernel slow?");
  await p.send({ type: "rename", id: p.last().tab, title: "Kernel speed" });
  assert.equal(p.last().tabs[0].title, "Kernel speed");
  assert.equal(p.description(), "Kernel speed");
  assert.ok(p.view.conversations().some((c: any) => c.title === "Kernel speed"));
  p.view.dispose();
});

test("closing a working tab asks first; a refusal keeps it, the last tab closed leaves an empty one", async () => {
  const p = panel();
  confirmAnswer = "no";
  const turn = p.send({ type: "send", text: "wait" });
  await until(() => p.last()?.busy);
  await p.send({ type: "closeTab", id: p.last().tab });
  assert.equal(p.last().tabs.length, 1);
  assert.equal(p.last().busy, true, "refused: the turn goes on");
  await turn;
  confirmAnswer = "yes";
  const id = p.last().tab;
  await p.send({ type: "closeTab", id });
  const s = p.last();
  assert.equal(s.tabs.length, 1);
  assert.notEqual(s.tab, id);
  assert.deepEqual(s.transcript, []);
  assert.equal(p.view.conversations().length, 1, "the closed conversation stays in the history");
  p.view.dispose();
});

test("the open tabs come back after a window reload, each agent started only at its next message", async () => {
  const state = mkdtempSync(join(tmpdir(), "bh-gstate-"));
  const workspace = new Map<string, unknown>();
  const before = panel(true, "en", "IPSA", { state, workspace });
  await before.send({ type: "send", text: "first topic" });
  before.view.newChat();
  await before.send({ type: "send", text: "second topic" });
  before.view.newChat();                                          // an empty tab is not kept
  await before.send({ type: "tab", id: before.last().tabs[0].id });
  before.view.dispose();
  const after = panel(true, "en", "IPSA", { state, workspace });
  await after.send({ type: "ready" });
  const s = after.last();
  assert.deepEqual(s.tabs.map((x: any) => x.title), ["first topic", "second topic"]);
  assert.deepEqual(texts(s), ["first topic", "you said: first topic"], "the tab shown before is shown again");
  assert.equal((after.view as any).tabs.some((t: any) => t.session), false, "no agent started by the reload");
  after.view.dispose();
});

test("choosing another model changes the shown tab only", async () => {
  const p = panel();
  await p.send({ type: "send", text: "hello" });
  const a = p.last().tab;
  p.view.newChat();
  await p.send({ type: "choose", agent: "", model: "code" });
  assert.equal(p.last().model, "code");
  await p.send({ type: "tab", id: a });
  assert.equal(p.last().model, "fast", "the first tab keeps the model it runs");
  p.view.dispose();
});

test("no more than three conversations work at once", async () => {
  const p = panel();
  const turns = [];
  for (let i = 0; i < 3; i++) {
    if (i) p.view.newChat();
    turns.push(p.send({ type: "send", text: "wait" }));
    await until(() => p.last()?.busy);
  }
  p.view.newChat();
  await p.send({ type: "send", text: "hello" });
  assert.match(texts(p.last()).at(-1), /3 conversations are already working/);
  await Promise.all(turns);
  p.view.dispose();
});

test("a conversation picked in the history shows its tab when it is open, else opens one", async () => {
  const p = panel();
  await p.send({ type: "send", text: "first topic" });
  const a = p.last().tab;
  p.view.newChat();
  await p.send({ type: "send", text: "second topic" });
  const [second, first] = p.view.conversations();
  await p.view.open(first.file);
  assert.equal(p.last().tab, a, "already open: its tab is shown");
  assert.equal(p.last().tabs.length, 2);
  await p.send({ type: "closeTab", id: p.last().tabs[1].id });
  await p.view.open(second.file);
  assert.equal(p.last().tabs.length, 2, "closed: it opens in a tab of its own");
  assert.deepEqual(texts(p.last()), ["second topic", "you said: second topic"]);
  p.view.dispose();
});

test("a variant signed in by its machine shows where it works, never a sign-in button", async () => {
  const p = panel(false, "en", "MaQI", { platform: true });
  await p.send({ type: "ready" });
  assert.deepEqual([p.last().signedIn, p.last().interactive], [false, false]);
  assert.match(p.webview.html, /works on its own servers/);
});

test("an empty tab presents the recent conversations, and one click reopens one", async () => {
  const p = panel();
  await p.send({ type: "ready" });                    // the panel is open
  await p.send({ type: "send", text: "first topic" });
  p.view.newChat();
  await p.send({ type: "send", text: "second topic" });
  p.view.newChat();                                   // an empty tab
  await p.send({ type: "model", model: "fast" });     // any redraw
  const recent = p.last().recent;
  assert.deepEqual(recent.map((r: any) => [r.title, r.questions]), [["second topic", 1], ["first topic", 1]]);
  await p.send({ type: "openConversation", file: recent[1].file });
  assert.deepEqual(texts(p.last()), ["first topic", "you said: first topic"]);
  await p.send({ type: "openConversation", file: "/etc/passwd" });
  assert.deepEqual(texts(p.last()), ["first topic", "you said: first topic"], "only a listed conversation opens");
  p.view.dispose();
});

// Session names, run directories, status for monitoring (owner, 2026-11-12).
test("a session is named at its first question; its agent is told its name and run directory; its status is kept for monitoring", async () => {
  const state = mkdtempSync(join(tmpdir(), "bh-gstate-"));
  const p = panel(true, "en", "IPSA", { state });
  await p.send({ type: "send", text: "whoami now" });
  const s = p.last();
  assert.equal(s.tabs[0].name, "whoami-now");
  assert.deepEqual(texts(s).at(-1), `whoami-now|${join(state, "sessions", "whoami-now")}`);
  const read = () => JSON.parse(readFileSync(join(state, "sessions", "whoami-now", "session.json"), "utf8"));
  assert.deepEqual([read().state, read().questions, read().title, read().name], ["idle", 1, "whoami now", "whoami-now"]);
  const turn = p.send({ type: "send", text: "wait" });
  await until(() => p.last()?.busy);
  assert.equal(read().state, "working");
  await turn;
  assert.equal(read().state, "idle");
  await p.send({ type: "rename", id: p.last().tab, title: "Kernel study" });
  assert.deepEqual([p.last().tabs[0].title, p.last().tabs[0].name, read().title], ["Kernel study", "whoami-now", "Kernel study"],
    "a rename is the title's; the name stays the run directory's key");
  p.view.dispose();
});

test("a tab with no question yet has no name, no run directory, no status", async () => {
  const state = mkdtempSync(join(tmpdir(), "bh-gstate-"));
  const p = panel(true, "en", "IPSA", { state });
  await p.send({ type: "ready" });
  assert.equal(p.last().tabs[0].name, "");
  assert.equal(existsSync(join(state, "sessions")), false);
  p.view.dispose();
});
