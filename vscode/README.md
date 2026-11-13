# BulkHours for VS Code

A coding assistant for students, in the style of Claude Code: a chat panel in
VS Code, an agent that reads the student's project and edits it after asking,
and models paid from the school's credits.

The extension is an [Agent Client Protocol](https://agentclientprotocol.com)
(ACP) client. The agent is a separate program the extension starts on the
student's machine; by default the DeepSeek harness (`dsh --profile acp`), with
models reached only through the school's LiteLLM proxy.

## One codebase, one extension per school

A school is a small file in `schools/<id>.json`: its name, colour, sign-in
page and key server. Everything else (models, which agent to run) comes from
the key server after sign-in, so changing models needs no new release.

```bash
npm install
npm test                                  # core tests, no VS Code needed
npm run check                             # type check
node scripts/package-school.mjs ipsa      # dist/bulkhours-ipsa-<version>.vsix
```

Each school build has its own extension id (`gateka.bulkhours-<id>`). VSIX
files are build output: they are published to the download area, never
committed.

## The key server contract

After sign-in, the extension calls the school's `keyUrl`:

```
POST <keyUrl>
Authorization: Bearer <BulkHours sign-in token>
{"school": "<id>"}
```

and expects:

```json
{
  "key": "sk-…",                       // LiteLLM virtual key, short-lived
  "base_url": "https://…/v1",          // the school's LiteLLM proxy (https)
  "expires_at": "2026-11-10T04:00:00Z",
  "models": ["fast", "code", "reasoning"],
  "default_model": "fast",
  "agent": {
    "id": "gateka", "label": "Gateka (DeepSeek)",
    "command": "npx",
    "args": ["-y", "@deepseek-ai/dsh", "--profile", "acp",
             "--patch", "${extensionPath}/media/agents/dsh-bulkhours.yml"],
    "env": {"OPENAI_BASE_URL": "${baseUrl}", "OPENAI_API_KEY": "${apiKey}"}
  }
}
```

The reply may also carry `"model_labels": {"fast": "DeepSeek V4.1 Flash"}`,
the underlying model of each alias, shown in the model list.

The agent's command, arguments and environment may use `${baseUrl}`,
`${apiKey}`, `${model}`, `${extensionPath}` and `${state}` (Gateka's state
folder, `$XDG_STATE_HOME/gateka`: a school's own agent keeps its files there,
e.g. `DSH_HOME: "${state}/agents/dsh"`). The extension fills them in; any
other placeholder is refused.

`401` means the sign-in expired (the extension signs out), `402` means no
credits left.

The panel's budget meter reads `GET <creditsUrl>?school=<id>` with the same
bearer, which answers `{"spent": 0.25, "budget": 10, "unit": "USD"}`; a meter
that cannot be read is simply not shown. The extension renews the key ten
minutes before `expires_at` and restarts the agent, which reads its key only once.

Sign-in opens `signInUrl` with `redirect` (a `vscode://` link back to the
extension) and `state`; the page sends the student back to
`<redirect>?token=…&state=…`. The token is kept in VS Code's secret storage.

## Where state lives: one rule

Everything the extension and its agents keep is under XDG, never in a
dot-folder of the home:

    $XDG_STATE_HOME/<name>/          ~/.local/state/<name>/   (<name>: the variant's
      conversations/                 `stateName`, gateka by default)
      sessions/<session name>/       a session's run directory
        session.json                 its status, for monitoring pages
        tools/                       code that only displays or renders results
        renders/*.html               its pages: each one is a link in the panel
        renders/*.url                a SERVED page (dashboard, monitor): its address
      agents/<agent id>/             an agent's own files: ${agentHome}

`GATEKA_STATE_HOME`, then the person's setting `<prefix>.stateDirectory`, move
the whole folder. **Any agent that speaks ACP fits** (dsh, OpenCode, Gemini
CLI, Claude Code...): its spec - from the key server, or the person's
`<prefix>.extraAgents` - gives the command, and points the agent's own
storage variable at `${agentHome}`:

    { "id": "dsh", "label": "dsh", "command": "dsh", "args": ["--profile", "acp"],
      "env": { "DSH_HOME": "${agentHome}" } }

Every agent also receives `GATEKA_STATE_HOME`, `GATEKA_AGENT_HOME`,
`GATEKA_SESSION_NAME` and `GATEKA_SESSION_DIR`. An agent that holds the
person's own login (Claude Code, Codex) is left where it is: moving it would
sign them out (ADR-0223).

## Conversations

Each conversation is recorded by the extension, whatever agent answered, in
ACP's shape under `$XDG_STATE_HOME/gateka/conversations/` (files readable by
their owner only, never in the project, pruned after 90 days; ADR-0223). The
panel shows the project's last conversation again after a reload; the same
agent resumes its own session when it can, another agent is handed the
conversation so far.

A Claude Code session becomes a conversation of the panel with
`scripts/import-claude.ts` (run where the session lives; nothing leaves the
machine):

    node --experimental-strip-types scripts/import-claude.ts \
      ~/.claude/projects/<folder>/<session id>.jsonl \
      --state ~/.local/state/<variant> --cwd <folder opened in VS Code> --school <variant>

What was typed, what was answered and each tool (its result cut short) are
kept; the session is named after the Claude Code title and gets its run
directory. Run again after the session went on in Claude Code: its one record
is replaced, unless an agent of the panel has since taken it over.

## Layout

| Path | What |
|---|---|
| `src/core/` | pure logic: transcript, agent launch, key reply, school file, the ACP session |
| `src/vscode/` | the VS Code layer: chat panel, sign-in, file access |
| `media/` | the panel's script and style, the harness overlay |
| `test/` | `node --test`, with a fake ACP agent for the session round trips |

## Releasing

Until the Marketplace listing is live, builds are published in the school's
`downloadUrl` (bulkhours.fr/bkfpage/vscode/) beside a `latest.json`
(`{"ipsa": "0.1.9", ...}`); the extension offers a newer build once a day, and
« Mettre à jour l'extension » installs it in place.

Bump `version` in `package.json`, add its entry to `CHANGELOG.md`, then push
a tag `vscode-v<version>`. The workflow `.github/workflows/vscode.yml` tests,
packages every school in `schools/` and publishes them to the Marketplace
under the `gateka` publisher, by trusted publishing (no token is stored).
