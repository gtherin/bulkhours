# Changelog

## 0.1.9 — 2026-11-10

- Conversation history (🕘 in the panel title): every conversation of the project, titled by its first question, reopens with its memory; « Renommer » names it, and the title shows beside the panel's name.
- « Redémarrer l'extension » and « Mettre à jour l'extension » in the panel's menu; a newer build in the download area is offered once a day.

## 0.1.8 — 2026-11-10

- Conversations are recorded by the extension, whatever agent answered (ACP shape, under `$XDG_STATE_HOME/gateka`, owner-only, pruned after 90 days; ADR-0223): the panel shows the last one again after a window reload.
- The same agent resumes its own session; another agent or model is handed the conversation so far.
- New `${state}` placeholder for agent launches (dsh keeps its files under it).

## 0.1.7 — 2026-11-10

- Money is shown in the school's currency, written the way the student's language writes it: IPSA shows euros (at par with the dollars Nebius bills), others dollars.

## 0.1.6 — 2026-11-10

- The agent's Markdown is rendered: headings, bullet and numbered lists (nested), tables, quotes, rules, italics, strikethrough; still escaped first.

## 0.1.5 — 2026-11-10

- dsh compacts its context earlier, leaving room for the answer: a long turn no longer ends every following reply on « length limit ».
- Compacter appears only for an agent that announces a compact command; dsh does not, and received « /compact » as a plain question.

## 0.1.4 — 2026-11-10

- An agent idle for 15 minutes is paused to free its memory, then resumed with the whole conversation at the next message (ACP session/resume). Only agents that save their sessions are paused (dsh does).
- A key renewal (every 12 h) no longer makes the agent forget the conversation.

## 0.1.3 — 2026-11-10

- The activity bar shows the BulkHours logo (the B with the code chevrons).

## 0.1.2 — 2026-11-10

- A permission request (an agent asking to run a command or edit a file) no longer vanishes when the conversation redraws: the agent waited forever.
- « réfléchit » names the agent in use (Claude Code), not the school model.

## 0.1.1 — 2026-11-10

- MaQI-style panel: budget and context meters, Compact / Clear, « réfléchit », pasted images, one menu for models (with prices) and your own agents, a dictation button.
- The menu shows the school models right after a window reload.

## 0.1.0 — 2026-11-09

First release, for IPSA and Polytechnique.

- Chat panel that runs an agent through the Agent Client Protocol (the
  DeepSeek harness by default) inside the student's workspace.
- Sign-in with BulkHours; models paid from the school's credits through a
  short-lived LiteLLM key, renewed automatically.
- The agent asks before writing a file; edits to open files can be undone.
- Model choice in the panel; English and French.
