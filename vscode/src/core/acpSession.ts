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

  private constructor(child: ChildProcess, conn: Connection, active: Active, host: Host, acceptsImages: boolean) {
    this.child = child;
    this.conn = conn;
    this.active = active;
    this.host = host;
    this.acceptsImages = acceptsImages;
  }

  get sessionId(): string { return this.active.sessionId; }

  static async start(launch: Launch, cwd: string, host: Host, clientVersion = "0.1.0"): Promise<AgentSession> {
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
      const { active, images } = await Promise.race([failed, open(conn, cwd, clientVersion)]);
      return new AgentSession(child, conn, active, host, images);
    } catch (e) {
      conn.close(e);
      child.kill();
      throw e;
    }
  }

  async prompt(text: string, context: { uri: string; name: string }[] = [],
               images: { mimeType: string; data: string }[] = []): Promise<StopReason> {
    const reply = this.active.prompt([
      { type: "text", text },
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

async function open(conn: Connection, cwd: string, version: string): Promise<{ active: Active; images: boolean }> {
  const init = await conn.agent.request(methods.agent.initialize, {
    protocolVersion: PROTOCOL_VERSION,
    clientCapabilities: { fs: { readTextFile: true, writeTextFile: true }, terminal: false },
    clientInfo: { name: "bulkhours", version },
  });
  const active = await conn.agent.buildSession({ cwd, mcpServers: [] }).start();
  return { active, images: init.agentCapabilities?.promptCapabilities?.image === true };
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
