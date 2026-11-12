# Changelog

## 0.1.21 — 2026-11-12

- Where conversations and the agents' files live is a choice: the variant's config file names its folder (MaQI: ~/.maqi), and the setting "State directory" moves it (absolute or under ~; after a window reload). Without either: ~/.local/state/gateka, as before.

## 0.1.20 — 2026-11-12

- MaQI carries MaQI's own mark, the candlesticks of its portal (maqi.ai.msct.fr): as is on its tile, in one colour in the activity bar. A variant's full-colour logo goes in schools/<id>-tile.svg. (MaQI only; the other variants are unchanged.)

## 0.1.19 — 2026-11-12

- One code, a config file per variant (schools/<id>.json): its title, its command and settings prefix, its mark (schools/<id>.svg) and tile colours. Two variants install side by side without colliding. First new variant: MaQI (gateka.maqi), on trial.

## 0.1.18 — 2026-11-12

- One + only, the panel's own: the tab strip no longer repeats it.
- The tab shown has a pencil to rename its conversation (double-click on the name still works).

## 0.1.17 — 2026-11-12

- Conversations open as tabs at the top of the panel, each with its own agent: a long job keeps working in one tab while you ask something in another. A dot marks a tab that works, a yellow dot one waiting for your answer. Double-click a tab to rename it, × closes it (asking first if it works), + opens a new one. The open tabs come back after a window reload; their agents start only at their next message.
- The model menu changes the tab shown; the other tabs keep the agent and model they run. At most three conversations work at once.

## 0.1.16 — 2026-11-12

- A long conversation reads back again: pictures a tool showed the agent (screenshots it read) are no longer stored in the record — the panel shows them as [image] anyway — and a record is read a piece at a time, so even a very large one opens. A job that read hundreds of screenshots had made a 584 MB record that left the panel empty.

## 0.1.15 — 2026-11-10

- Compacter and Effacer stay clickable during a turn: VS Code asks first, then the turn is stopped cleanly before compacting or clearing.

## 0.1.14 — 2026-11-10

- Compacter works with every agent: the agent's own /compact when it has one (Claude Code), otherwise the extension lets the session go and the next message starts a fresh one handed the conversation condensed.

## 0.1.13 — 2026-11-10

- dsh works with a 128K context window (was 64K): an orchestrating turn no longer runs out of room and stops every reply on « length limit ».

## 0.1.12 — 2026-11-10

- While the agent works, the panel says for how long, its last sign of life, the tool it runs and what the turn has cost so far; the budget is read again every minute during a long turn.

## 0.1.11 — 2026-11-10

- « Redémarrer l'assistant » restarts only BulkHours (its agent and its panel); it used to restart every extension of the window. The conversation goes on at the next message.

## 0.1.10 — 2026-11-10

- Pasted images reach the models that read them: the key server says which (LiteLLM supports_vision; today `fast`, DeepSeek V4.1 Flash), dsh is told, and the menu says « lit les images ».
- Setting `bulkhours.imageModels` replaces the school's list.

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
