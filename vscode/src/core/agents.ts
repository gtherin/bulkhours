// Which agent program to start, and how the student's credentials reach it.
// Pure: parsing and substitution only; spawning lives in acpSession.ts.

export type AgentSpec = {
  id: string;
  label: string;
  command: string;
  args: string[];
  env: Record<string, string>;
};

// What an agent's command, arguments and environment may refer to as ${name}.
export type LaunchVars = { baseUrl: string; apiKey: string; model: string; extensionPath: string };
export type Launch = { command: string; args: string[]; env: Record<string, string> };

const PLACEHOLDER = /\$\{([a-zA-Z]+)\}/g;

export function launchFor(spec: AgentSpec, vars: LaunchVars): Launch {
  const fill = (s: string) => s.replace(PLACEHOLDER, (_, name: string) => {
    if (name in vars) return vars[name as keyof LaunchVars];
    throw new Error(`unknown placeholder \${${name}} in agent ${spec.id}`);
  });
  return {
    command: fill(spec.command),
    args: spec.args.map(fill),
    env: Object.fromEntries(Object.entries(spec.env).map(([k, v]) => [k, fill(v)])),
  };
}

export function parseAgents(raw: unknown): AgentSpec[] {
  if (!Array.isArray(raw)) throw new Error("agents must be a list");
  return raw.map((item, i) => parseAgent(item, i + 1));
}

function parseAgent(raw: unknown, n: number): AgentSpec {
  const o = (raw ?? {}) as Record<string, unknown>;
  const where = `agent ${n}`;
  return {
    id: str(o.id, where, "id"),
    label: str(o.label, where, "label"),
    command: str(o.command, where, "command"),
    args: strings(o.args ?? [], where, "args"),
    env: stringMap(o.env ?? {}, where, "env"),
  };
}

function str(v: unknown, where: string, key: string): string {
  if (typeof v !== "string" || v === "") throw new Error(`${where}: "${key}" must be a non-empty string`);
  return v;
}

function strings(v: unknown, where: string, key: string): string[] {
  if (!Array.isArray(v) || v.some((x) => typeof x !== "string")) {
    throw new Error(`${where}: "${key}" must be a list of strings`);
  }
  return v as string[];
}

function stringMap(v: unknown, where: string, key: string): Record<string, string> {
  if (typeof v !== "object" || v === null || Array.isArray(v)
      || Object.values(v).some((x) => typeof x !== "string")) {
    throw new Error(`${where}: "${key}" must map names to strings`);
  }
  return v as Record<string, string>;
}

export function pickAgent(agents: AgentSpec[], wanted: string): AgentSpec {
  if (agents.length === 0) throw new Error("no agent configured");
  if (!wanted) return agents[0];
  const found = agents.find((a) => a.id === wanted);
  if (!found) throw new Error(`no agent "${wanted}"`);
  return found;
}
