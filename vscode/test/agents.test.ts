import { test } from "node:test";
import assert from "node:assert/strict";
import { launchFor, parseAgents, pickAgent, type AgentSpec } from "../src/core/agents.ts";

const creds = { baseUrl: "https://llm.bulkhours.fr/v1", apiKey: "sk-student", model: "fast", extensionPath: "/ext", state: "/st" };
const dsh: AgentSpec = {
  id: "gateka", label: "Gateka (DeepSeek)", command: "dsh", args: ["--profile", "acp"],
  env: { OPENAI_BASE_URL: "${baseUrl}", OPENAI_API_KEY: "${apiKey}", DSH_MODEL: "${model}" },
};

test("the student's credentials reach the agent through its environment", () => {
  assert.deepEqual(launchFor(dsh, creds), {
    command: "dsh", args: ["--profile", "acp"],
    env: { OPENAI_BASE_URL: "https://llm.bulkhours.fr/v1", OPENAI_API_KEY: "sk-student", DSH_MODEL: "fast" },
  });
});

test("placeholders in arguments are filled too", () => {
  const spec = { ...dsh, args: ["--model", "${model}"], env: {} };
  assert.deepEqual(launchFor(spec, creds).args, ["--model", "fast"]);
});

test("an agent can name a file shipped with the extension", () => {
  const spec = { ...dsh, args: ["--patch", "${extensionPath}/agents/dsh.yml"], env: {} };
  assert.deepEqual(launchFor(spec, creds).args, ["--patch", "/ext/agents/dsh.yml"]);
});

test("an unknown placeholder is refused, not sent to the agent as text", () => {
  const spec = { ...dsh, env: { TOKEN: "${secret}" } };
  assert.throws(() => launchFor(spec, creds), /unknown placeholder \$\{secret\} in agent gateka/);
});

test("agent lists from settings are checked where they enter", () => {
  assert.deepEqual(parseAgents([{ id: "a", label: "A", command: "x" }]), [
    { id: "a", label: "A", command: "x", args: [], env: {} },
  ]);
  assert.throws(() => parseAgents([{ id: "a", label: "A" }]), /agent 1: "command" must be a non-empty string/);
  assert.throws(() => parseAgents([{ id: "a", label: "A", command: "x", args: [1] }]), /agent 1: "args" must be a list of strings/);
  assert.throws(() => parseAgents("nope"), /agents must be a list/);
});

test("the chosen agent wins, else the first one", () => {
  const other = { ...dsh, id: "opencode" };
  assert.equal(pickAgent([dsh, other], "opencode").id, "opencode");
  assert.equal(pickAgent([dsh, other], "").id, "gateka");
  assert.throws(() => pickAgent([dsh], "ghost"), /no agent "ghost"/);
  assert.throws(() => pickAgent([], ""), /no agent configured/);
});

test("an agent's environment must map names to strings", () => {
  for (const env of [["A=1"], { A: 1 }, "A=1"]) {
    assert.throws(() => parseAgents([{ id: "a", label: "A", command: "x", env }]), /agent 1: "env" must map names to strings/);
  }
  assert.deepEqual(parseAgents([{ id: "a", label: "A", command: "x", env: { A: "1" } }])[0].env, { A: "1" });
  assert.deepEqual(parseAgents([{ id: "a", label: "A", command: "x", env: null }])[0].env, {}, "null reads as no environment");
});

// One rule for every agent's own files (owner, 2026-11-12: "a generic way...
// dsh, opencode, gemini or others"): <state>/agents/<agent id>/, which a spec
// points its agent's own variable at with ${agentHome}.
test("every agent has a home under the state folder, which its spec can name", async () => {
  const { agentHome } = await import("../src/core/agents.ts");
  assert.equal(agentHome("/st", "dsh"), "/st/agents/dsh");
  assert.equal(agentHome("/st", "Open Code/../x"), "/st/agents/open-code-x", "an id is never a path");
  const opencode: AgentSpec = { id: "opencode", label: "OpenCode", command: "opencode", args: ["acp"],
    env: { XDG_DATA_HOME: "${agentHome}/data", OPENCODE_CONFIG: "${agentHome}/opencode.json" } };
  assert.deepEqual(launchFor(opencode, creds).env, { XDG_DATA_HOME: "/st/agents/opencode/data", OPENCODE_CONFIG: "/st/agents/opencode/opencode.json" });
  assert.deepEqual(launchFor({ ...dsh, id: "dsh", env: { DSH_HOME: "${agentHome}" } }, creds).env, { DSH_HOME: "/st/agents/dsh" });
});
