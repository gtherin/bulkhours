// A tiny ACP agent for tests: it echoes, reads a file, or asks before writing
// one, so the client's whole round trip runs without a model or an API key.
import { Readable, Writable } from "node:stream";
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { agent, methods, ndJsonStream, PROTOCOL_VERSION } from "@agentclientprotocol/sdk";

// FAKE_STORE: a folder where sessions are saved, like dsh's ~/.dsh/sessions,
// so a NEW process can resume one (session/resume) with what it remembered.
const store = process.env.FAKE_STORE;
const memory = (id: string) => join(store!, `${id.replace(/\W/g, "_")}.txt`);
let nextId = 0;

const stream = ndJsonStream(
  Writable.toWeb(process.stdout) as WritableStream<Uint8Array>,
  Readable.toWeb(process.stdin) as ReadableStream<Uint8Array>,
);

const say = (client: any, sessionId: string, text: string) =>
  client.notify(methods.client.session.update, {
    sessionId, update: { sessionUpdate: "agent_message_chunk", content: { type: "text", text } },
  });

const cancelled = new Set<string>();

let caps: unknown = null;

agent({ name: "fake-agent" })
  .onNotification(methods.agent.session.cancel, ({ params }) => { cancelled.add(params.sessionId); })
  .onRequest(methods.agent.initialize, ({ params }) => {
    caps = params.clientCapabilities;
    return { protocolVersion: PROTOCOL_VERSION,
      agentCapabilities: {
        ...(process.env.FAKE_IMAGES ? { promptCapabilities: { image: true } } : {}),
        ...(store ? { sessionCapabilities: { resume: {} } } : {}),
      } };
  })
  .onRequest(methods.agent.session.new, ({ params }) => ({ sessionId: store ? `s-${process.pid}-${nextId++}` : `s-${params.cwd}` }))
  .onRequest(methods.agent.session.resume, ({ params }) => {
    if (!store || !existsSync(memory(params.sessionId))) throw new Error(`no saved session ${params.sessionId}`);
    return {};
  })
  .onRequest(methods.agent.session.prompt, async ({ params, client }) => {
    // FAKE_COMMANDS: announce slash commands, as Claude Code does; here at the
    // start of every turn, so a test never races the announcement.
    if (process.env.FAKE_COMMANDS) await client.notify(methods.client.session.update, {
      sessionId: params.sessionId, update: { sessionUpdate: "available_commands_update",
        availableCommands: [{ name: "compact", description: "Summarise and continue" }] },
    });
    const first = params.prompt[0];
    const text = first && first.type === "text" ? first.text : "";
    const [verb, path] = text.split(" ");
    if (verb === "caps") {
      await say(client, params.sessionId, JSON.stringify(caps));
    } else if (verb === "context") {
      const links = params.prompt.filter((b) => b.type === "resource_link").map((b: any) => b.name);
      await say(client, params.sessionId, `context=${links.join(",") || "none"}`);
    } else if (verb === "wait") {
      // Ends early only if the client's session/cancel actually arrives.
      for (let i = 0; i < 40 && !cancelled.has(params.sessionId); i++) await new Promise((r) => setTimeout(r, 25));
      const stopped = cancelled.delete(params.sessionId);
      await say(client, params.sessionId, stopped ? "stopping" : "waited the whole second");
      return { stopReason: stopped ? "cancelled" : "end_turn" };
    } else if (verb === "remember") {
      writeFileSync(memory(params.sessionId), path);
      await say(client, params.sessionId, `noted ${path}`);
    } else if (verb === "recall") {
      const m = store && existsSync(memory(params.sessionId)) ? readFileSync(memory(params.sessionId), "utf8") : "nothing";
      await say(client, params.sessionId, `I remember ${m} (pid ${process.pid})`);
    } else if (verb === "images") {
      const imgs = params.prompt.filter((b) => b.type === "image").map((b: any) => `${b.mimeType}:${b.data}`);
      await say(client, params.sessionId, `images=${imgs.join(",") || "none"}`);
    } else if (verb === "usage") {
      await client.notify(methods.client.session.update, {
        sessionId: params.sessionId, update: { sessionUpdate: "usage_update", used: 40_600, size: 64_000 },
      });
      await say(client, params.sessionId, "counted");
    } else if (verb === "model") {
      await say(client, params.sessionId, `model=${process.env.FAKE_MODEL}`);
    } else if (verb === "read") {
      const r = await client.request(methods.client.fs.readTextFile, { sessionId: params.sessionId, path });
      await say(client, params.sessionId, `read: ${r.content}`);
    } else if (verb === "write") {
      const r = await client.request(methods.client.session.requestPermission, {
        sessionId: params.sessionId,
        toolCall: { toolCallId: "w1", title: `Write ${path}`, kind: "edit" },
        options: [
          { optionId: "yes", name: "Allow", kind: "allow_once" },
          { optionId: "no", name: "Reject", kind: "reject_once" },
        ],
      });
      if (r.outcome.outcome === "selected" && r.outcome.optionId === "yes") {
        await client.request(methods.client.fs.writeTextFile, { sessionId: params.sessionId, path, content: "written" });
        await say(client, params.sessionId, "wrote it");
      } else {
        await say(client, params.sessionId, "did not write");
      }
    } else {
      await say(client, params.sessionId, `you said: ${text}`);
    }
    return { stopReason: "end_turn" };
  })
  .connect(stream);
