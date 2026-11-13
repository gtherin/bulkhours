# Changelog

## 0.1.46 — 2026-11-13

- MaQI: the frontier tier (Kimi K3) is gone from the menu, as from MaQI's proxy; reasoning (Kimi K3.1 Pro) scores far higher for less.

## 0.1.45 — 2026-11-13

- MaQI: reasoning is Kimi K3.1 Pro (2.00 / 10.00 per million tokens), the best-scored model Nebius publishes; it was GLM 5.2. The other variants read their menu from their key server, changed the same day.

## 0.1.44 — 2026-11-13

- MaQI: code is GLM 5.3 (1.40 / 4.40 per million tokens), as the MaQI proxy has mapped it since 13 November; 0.1.43 named DeepSeek V4 Pro, which the proxy does not run.

## 0.1.43 — 2026-11-13

- MaQI: the model menu names what the tiers run since Nebius withdrew two models on 13 November: fast is DeepSeek V4.1 Flash (0.30 / 1.20 per million tokens), code is DeepSeek V4 Pro (1.32 / 3.96). The other variants read their menu from their key server and needed no new build.
- A Claude Code session becomes a conversation of the panel with `scripts/import-claude.ts` (see the README).

## 0.1.42 — 2026-11-12

- A session's served pages: a file renders/<name>.url holding an address (a Streamlit or marimo dashboard, a monitoring page) is a link in the panel too. An address on the machine opens in a tab beside the code, through VS Code's way to a local port; another address opens in the browser.

## 0.1.41 — 2026-11-12

- A conversation another tool prepared for the folder (a record with its first request written and never run) opens as its own tab when the panel loads, with a Start button that runs that request as it is. Before, it was one more line in the list, and nothing ran it.

## 0.1.40 — 2026-11-12

- An empty tab lists every conversation recorded for the folder, not only the six most recent.

## 0.1.39 — 2026-11-12

- MaQI's status bar keeps its Wasabi check cache under ~/.local/state/maqi too; nothing of the extension is left in ~/.maqi, which is the platform's. (MaQI only.)

## 0.1.38 — 2026-11-12

- One rule for where state lives: XDG, ~/.local/state/<name> (the variant's `stateName`, gateka by default) - no dot-folder in the home. MaQI moves from ~/.maqi to ~/.local/state/maqi; a variant file still naming `stateDir` is refused at build.
- One rule for every agent's own files: <state>/agents/<agent id>/, which a spec names with ${agentHome} (dsh: DSH_HOME, OpenCode: its XDG folders, another agent: its own variable). Every agent is told GATEKA_STATE_HOME and GATEKA_AGENT_HOME.
- A session's pages: each session has a renders folder (<run directory>/renders/); every .html file there is a link under the panel's tabs, opened in a tab beside the code and shown again when the file changes. The page may use its own files and the usual chart CDNs, and can send nothing anywhere.
- The agent is told the session's rules once: code that only displays or renders results goes in <run directory>/tools/, pages in <run directory>/renders/, product code stays in the project (GATEKA_SESSION_RENDERS names the folder).

## 0.1.37 — 2026-11-12

- Each conversation is a named session. Its name (a slug of its first question, or the one a tool wrote in the record's header) is claimed once with its run directory, <state>/sessions/<name>/, and never changes; renaming a tab changes its title only. The agent is told GATEKA_SESSION_NAME and GATEKA_SESSION_DIR.
- For monitoring pages, each session keeps <state>/sessions/<name>/session.json (name, title, folder, agent, model, state working / waiting / idle, since, last sign of life, tool, questions, updated, record), written whole at turn start, turn end and each minute while it works. No key in it.
- The history lists a project's records by the folder named in their header, wherever they sit: sessions seeded by another tool appear.

## 0.1.36 — 2026-11-12

- Sign-in, the real cause: the link is handed to the browser as written. VS Code's own Uri round trip re-encoded the link inside the link (…signed-in%253FwindowId=5) and the sign-in page refused it; 0.1.34 and 0.1.35 looked in the wrong place. The page now also reads such a link back.
- « Paste a code instead » (and the command « Sign in with a code »): the sign-in page shows a code, you paste it into VS Code - as Claude Code does. No way back to the editor is needed, so it works from any editor or browser.

## 0.1.35 — 2026-11-12

- Sign-in with several VS Code windows open, for good: VS Code hands the way back with ?windowId=N inside its path, which every way of writing it out encoded as %3F; the link is now rebuilt from its parts. (0.1.34 only fixed the "=".)

## 0.1.34 — 2026-11-12

- Sign-in works with several VS Code windows open: the way back to the window (…?windowId=N) is sent as written; percent-encoded, the sign-in page refused it (« Lien de connexion invalide »).

## 0.1.33 — 2026-11-12

- BulkHours and IPSA are two extensions. IPSA (gateka.ipsa): named IPSA, its logo in the extension list and in the activity bar, its blue in the panel, its own commands and settings (ipsa.*). BulkHours (gateka.bulkhours): the B on the logo's teal, commands and settings bulkhours.*. Polytechnique has its own prefix too. The earlier build « bulkhours-ipsa » is replaced by « ipsa ».
- Gateka carries the BulkHours favicon: the white B on its square teal ground, in the extension list and the activity bar (in place of the dotted G).

## 0.1.32 — 2026-11-12

- The IPSA build carries IPSA's logo as its icon in the extension list (schools/ipsa-tile.svg, redrawn as vectors from the school's image). The activity bar keeps the BulkHours mark. (IPSA only.)
- New variant Gateka (gateka.gateka), the reference one: built as the BulkHours variants (same sign-in and key server), with the G of Gateka's dot-matrix wordmark as its mark.

## 0.1.31 — 2026-11-12

- An empty tab presents your recent conversations (the last six: title, when, how many questions); one click reopens one in its tab.
- The IPSA build is named « BulkHours » (panel, menus, extension list), not « BulkHours IPSA ».

## 0.1.30 — 2026-11-12

- A marimo notebook's rendered page in VS Code: on a .py, « Reopen Editor With… › Rendered page (HTML) » shows its page (marimo export html, results only), rendered again at each save - yours or the agent's. The marimo used is the setting « marimo », else the one beside your default Python, else the PATH's. The page may load marimo's own code (jsdelivr) and send nothing anywhere.

## 0.1.29 — 2026-11-12

- A tool's output is folded only when it is long: two short lines or fewer show as they are (an error is read at once), wrapped instead of scrolling sideways; longer ones fold behind their first line and their line count.

## 0.1.28 — 2026-11-12

- You, always in view: your name in the status bar (far left) and your avatar at the end of the panel's tab strip (MaQI: the picture Git and the portal show) both open the platform's links. Variants without links show neither.

## 0.1.27 — 2026-11-12

- The platform's pages one button away: a links icon in the panel header opens the variant's list (MaQI: MaQI, Docs, Directory, Slack, Git, Moodle - the portal menu's entries open to every member). Variants without links show no button.

## 0.1.26 — 2026-11-12

- A dashboard in a tab: « Open a dashboard » (panel menu or command palette) asks the port of the app running on the machine (Streamlit 8501, marimo 2718) and opens it in an editor tab beside the code, behind the same sign-in.
- The chat and the editor are linked: right-click a file in the explorer, or a selection in the editor, « Ask the assistant about this » puts it in the chat box with its lines; a file path the agent writes (`topic_hormuz.py:42`) opens in the editor at that line.

## 0.1.25 — 2026-11-12

- MaQI's status bar in VS Code, as JupyterLab's MaQI bar: your session's RAM and CPU, your Wasabi data rights (buckets readable, datasets, credentials renewal), whether the machine stays on, and the data sent out. Computed by MaQI's own code on the machine (media/platform/maqi-status.py), refreshed every minute; hover an item for the detail. (MaQI only.)

## 0.1.24 — 2026-11-12

- MaQI shows its budget as JupyterHub does: the spend and cap of the project your key belongs to (e.g. res-enterprise, €0 / €200), as MaQI's LiteLLM enforces them, read with your own key.
- In a folder VS Code does not trust yet (Restricted Mode), the extension says it needs a trusted folder instead of disappearing silently.

## 0.1.23 — 2026-11-12

- MaQI runs MaQI's own agent launcher on its servers (/opt/maqi-agent/bin/dsh-acp: its Node, its pinned dsh, its profile and platform rules), with the model chosen in the menu on top. 0.1.22 tried npx, which MaQI hubs do not have. (MaQI only.)

## 0.1.22 — 2026-11-12

- MaQI uses MaQI's own connection, not BulkHours': on a MaQI server the key the platform writes for each person (/run/maqi/keys/<account>/llm.env, renewed every 12 h) is the sign-in; its models (fast, code, reasoning, frontier) and prices are in schools/maqi.json. A renewed key restarts the agent at the next turn, which resumes the conversation. Elsewhere, MaQI says where it works instead of offering a sign-in.
- The agent introduces itself with the variant's name.

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
