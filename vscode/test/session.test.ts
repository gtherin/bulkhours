import { test } from "node:test";
import assert from "node:assert/strict";
import { tmpdir } from "node:os";
import { fileURLToPath } from "node:url";
import { AgentSession, type Host } from "../src/core/acpSession.ts";
import { applyUpdate, type Transcript } from "../src/core/transcript.ts";

const CWD = tmpdir();
const FAKE = fileURLToPath(new URL("./fixtures/fake-agent.ts", import.meta.url));
const launch = {
  command: process.execPath, args: ["--experimental-strip-types", "--no-warnings", FAKE],
  env: { FAKE_MODEL: "fast" },
};

function recordingHost(answer: "yes" | "no" | "cancel" = "yes") {
  const files = new Map<string, string>([["/w/main.c", "int main() {}"]]);
  let transcript: Transcript = [];
  const asked: string[] = [];
  const host: Host = {
    readTextFile: async (path) => {
      const f = files.get(path);
      if (f === undefined) throw new Error(`no such file ${path}`);
      return f;
    },
    writeTextFile: async (path, content) => { files.set(path, content); },
    askPermission: async (req) => {
      asked.push(req.toolCall.title ?? "");
      return answer === "cancel" ? { outcome: "cancelled" } : { outcome: "selected", optionId: answer };
    },
    onUpdate: (u) => { transcript = applyUpdate(transcript, u); },
  };
  return { host, files, asked, text: () => transcript.map((e) => ("text" in e ? e.text : e.kind)).join("|") };
}

test("a prompt streams the agent's answer back", async () => {
  const r = recordingHost();
  const s = await AgentSession.start(launch, CWD, r.host);
  try {
    assert.equal(await s.prompt("hello"), "end_turn");
    assert.equal(r.text(), "you said: hello");
  } finally { s.dispose(); }
});

test("the agent's environment carries the launch settings", async () => {
  const r = recordingHost();
  const s = await AgentSession.start(launch, CWD, r.host);
  try {
    await s.prompt("model");
    assert.equal(r.text(), "model=fast");
  } finally { s.dispose(); }
});

test("the agent reads files through the editor", async () => {
  const r = recordingHost();
  const s = await AgentSession.start(launch, CWD, r.host);
  try {
    await s.prompt("read /w/main.c");
    assert.equal(r.text(), "read: int main() {}");
  } finally { s.dispose(); }
});

test("a write happens only after the student allows it", async () => {
  const yes = recordingHost("yes");
  const s1 = await AgentSession.start(launch, CWD, yes.host);
  try {
    await s1.prompt("write /w/out.txt");
    assert.deepEqual(yes.asked, ["Write /w/out.txt"]);
    assert.equal(yes.files.get("/w/out.txt"), "written");
  } finally { s1.dispose(); }

  const no = recordingHost("no");
  const s2 = await AgentSession.start(launch, CWD, no.host);
  try {
    await s2.prompt("write /w/out.txt");
    assert.equal(no.files.has("/w/out.txt"), false);
    assert.equal(no.text(), "did not write");
  } finally { s2.dispose(); }
});

test("a missing agent program fails loudly with its name", async () => {
  const r = recordingHost();
  await assert.rejects(
    AgentSession.start({ command: "no-such-agent-xyz", args: [], env: {} }, CWD, r.host),
    /could not start "no-such-agent-xyz"/,
  );
});

test("a missing workspace folder is named, not reported as a missing program", async () => {
  const r = recordingHost();
  await assert.rejects(AgentSession.start(launch, "/no/such/folder", r.host), /workspace folder "\/no\/such\/folder" does not exist/);
});

test("the agent is told it may read and write through the editor, and has no terminal", async () => {
  const r = recordingHost();
  const s = await AgentSession.start(launch, CWD, r.host);
  try {
    await s.prompt("caps");
    const caps = JSON.parse(r.text());
    assert.deepEqual({ fs: caps.fs, terminal: caps.terminal }, { fs: { readTextFile: true, writeTextFile: true }, terminal: false });
  } finally { s.dispose(); }
});

test("pasted images reach an agent that reads them, and it says it does", async () => {
  const r = recordingHost();
  const s = await AgentSession.start({ ...launch, env: { ...launch.env, FAKE_IMAGES: "1" } }, CWD, r.host);
  try {
    assert.equal(s.acceptsImages, true);
    await s.prompt("images", [], [{ mimeType: "image/png", data: "AAA" }]);
    assert.equal(r.text(), "images=image/png:AAA");
  } finally { s.dispose(); }
});

test("an agent that does not read images says so, and is never sent one", async () => {
  const r = recordingHost();
  const s = await AgentSession.start(launch, CWD, r.host);
  try {
    assert.equal(s.acceptsImages, false);
    await s.prompt("images", [], [{ mimeType: "image/png", data: "AAA" }]);
    assert.equal(r.text(), "images=none");
  } finally { s.dispose(); }
});
