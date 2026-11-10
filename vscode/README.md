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

`401` means the sign-in expired (the extension signs out), `402` means no
credits left.

The panel's budget meter reads `GET <creditsUrl>?school=<id>` with the same
bearer, which answers `{"spent": 0.25, "budget": 10, "unit": "USD"}`; a meter
that cannot be read is simply not shown. `${baseUrl}`, `${apiKey}`, `${model}` and `${extensionPath}`
are filled in by the extension; any other placeholder is refused. The
extension renews the key ten minutes before `expires_at` and restarts the
agent, which reads its key only once.

Sign-in opens `signInUrl` with `redirect` (a `vscode://` link back to the
extension) and `state`; the page sends the student back to
`<redirect>?token=…&state=…`. The token is kept in VS Code's secret storage.

## Layout

| Path | What |
|---|---|
| `src/core/` | pure logic: transcript, agent launch, key reply, school file, the ACP session |
| `src/vscode/` | the VS Code layer: chat panel, sign-in, file access |
| `media/` | the panel's script and style, the harness overlay |
| `test/` | `node --test`, with a fake ACP agent for the session round trips |

## Releasing

Bump `version` in `package.json`, add its entry to `CHANGELOG.md`, then push
a tag `vscode-v<version>`. The workflow `.github/workflows/vscode.yml` tests,
packages every school in `schools/` and publishes them to the Marketplace
under the `gateka` publisher, by trusted publishing (no token is stored).
