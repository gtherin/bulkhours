// One agent process, one ACP session. The editor side of every request the
// agent can make (read, write, ask permission) goes through `Host`, so this
// file knows nothing about VS Code and runs as-is under the tests.
import { spawn, type ChildProcess } from "node:child_process";
import { existsSync } from "node:fs";
import { Readable, Writable } from "node:stream";
import {
  client, methods, ndJsonStream, PROTOCOL_VERSION,
  type RequestPermissionOutcome, type RequestPermissionRequest, type SessionUpdate, type StopReason,
} from "@agentclientprotocol/sdk";

// The SDK's `ActiveSession`: it queues updates and the end of a turn in ONE
// ordered stream. A plain notification handler raced the prompt's reply, so a
// turn could read as finished before its last words arrived.
type Active = Awaited<ReturnType<ReturnType<Connection["agent"]["buildSession"]>["start"]>>;
import type { Launch } from "./agents.ts";

export interface Host {
  readTextFile(path: string, line?: number | null, limit?: number | null): Promise<string>;
  writeTextFile(path: string, content: string): Promise<void>;
  askPermission(req: RequestPermissionRequest): Promise<RequestPermissionOutcome>;
  onUpdate(update: SessionUpdate): void;
  log?(line: string): void;
}

type Connection = ReturnType<ReturnType<typeof client>["connect"]>;

export class AgentSession {
  private readonly child: ChildProcess;
  private readonly conn: Connection;
  private readonly active: Active;
  private readonly host: Host;
  // Whether the agent said, at initialize, that it reads images. Never sent
  // one otherwise: an agent that does not expect them may fail the turn.
  readonly acceptsImages: boolean;
  // Whether the agent saves its sessions and can resume one in a new process
  // (ACP sessionCapabilities.resume; dsh keeps them in ~/.dsh/sessions), and
  // whether this one was resumed rather than started fresh.
  readonly canResume: boolean;
  readonly resumed: boolean;

  private constructor(child: ChildProcess, conn: Connection, opened: Opened, host: Host) {
    this.child = child;
    this.conn = conn;
    this.active = opened.active;
    this.host = host;
    this.acceptsImages = opened.images;
    this.canResume = opened.canResume;
    this.resumed = opened.resumed;
  }

  get sessionId(): string { return this.active.sessionId; }

  // `resume`: the id of a session this agent saved earlier; when it can
  // resume it, the conversation continues with its memory, otherwise a fresh
  // session starts (a resume that fails is never an error for the student).
  static async start(launch: Launch, cwd: string, host: Host, clientVersion = "0.1.0",
                     resume?: string): Promise<AgentSession> {
    if (!existsSync(cwd)) throw new Error(`workspace folder "${cwd}" does not exist`);
    const child = spawn(launch.command, launch.args, {
      cwd, env: { ...process.env, ...launch.env }, stdio: ["pipe", "pipe", "pipe"],
    });
    const failed = new Promise<never>((_, reject) => {
      child.once("error", (e) => reject(new Error(`could not start "${launch.command}": ${e.message}`)));
      child.once("exit", (code) => reject(new Error(`"${launch.command}" exited (${code}) before the session opened`)));
    });
    child.stderr?.on("data", (b: Buffer) => host.log?.(b.toString()));

    const conn = editorSide(host).connect(ndJsonStream(
      Writable.toWeb(child.stdin!) as WritableStream<Uint8Array>,
      Readable.toWeb(child.stdout!) as ReadableStream<Uint8Array>,
    ));
    try {
      const opened = await Promise.race([failed, open(conn, cwd, clientVersion, resume)]);
      return new AgentSession(child, conn, opened, host);
    } catch (e) {
      conn.close(e);
      child.kill();
      throw e;
    }
  }

  // `preface`: text the agent reads before the question (the conversation so
  // far, when this agent was not part of it).
  async prompt(text: string, context: { uri: string; name: string }[] = [],
               images: { mimeType: string; data: string }[] = [], preface = "", note = ""): Promise<StopReason> {
    const reply = this.active.prompt([
      ...(preface ? [{ type: "text" as const, text: preface }] : []),
      { type: "text", text },
      // What the agent should know beside the question (its session's rules).
      ...(note ? [{ type: "text" as const, text: note }] : []),
      ...context.map((c) => ({ type: "resource_link" as const, uri: c.uri, name: c.name })),
      ...(this.acceptsImages ? images.map((i) => ({ type: "image" as const, mimeType: i.mimeType, data: i.data })) : []),
    ]);
    // A rejected prompt never queues a stop: surface it instead of waiting forever.
    const failed = reply.then(() => new Promise<never>(() => {}));
    for (;;) {
      const m = await Promise.race([this.active.nextUpdate(), failed]);
      if (m.kind === "stop") return m.stopReason;
      this.host.onUpdate(m.update);
    }
  }

  async cancel(): Promise<void> {
    await this.conn.agent.notify(methods.agent.session.cancel, { sessionId: this.sessionId });
  }

  dispose(): void {
    this.active.dispose();
    this.conn.close();
    this.child.kill();
  }
}

type Opened = { active: Active; images: boolean; canResume: boolean; resumed: boolean };

async function open(conn: Connection, cwd: string, version: string, resume?: string): Promise<Opened> {
  const init = await conn.agent.request(methods.agent.initialize, {
    protocolVersion: PROTOCOL_VERSION,
    clientCapabilities: { fs: { readTextFile: true, writeTextFile: true }, terminal: false },
    clientInfo: { name: "bulkhours", version },
  });
  const images = init.agentCapabilities?.promptCapabilities?.image === true;
  const canResume = Boolean(init.agentCapabilities?.sessionCapabilities?.resume);
  if (resume && canResume) {
    try {
      const reply = await conn.agent.request(methods.agent.session.resume, { sessionId: resume, cwd, mcpServers: [] });
      // The SDK builds its ordered update queue only around a session/new
      // reply (attachSession, private in @agentclientprotocol/sdk 2.4.0,
      // pinned); a resumed session gets the same queue the same way.
      const active = (conn.agent as unknown as { attachSession(r: object): Active })
        .attachSession({ ...reply, sessionId: resume });
      return { active, images, canResume, resumed: true };
    } catch {
      // gone, or refused: a fresh session below
    }
  }
  const active = await conn.agent.buildSession({ cwd, mcpServers: [] }).start();
  return { active, images, canResume, resumed: false };
}

function editorSide(host: Host) {
  return client({ name: "bulkhours" })
    .onRequest(methods.client.session.requestPermission, async ({ params }) => ({
      outcome: await host.askPermission(params),
    }))
    .onRequest(methods.client.fs.readTextFile, async ({ params }) => ({
      content: await host.readTextFile(params.path, params.line, params.limit),
    }))
    .onRequest(methods.client.fs.writeTextFile, async ({ params }) => {
      await host.writeTextFile(params.path, params.content);
      return {};
    });
}
