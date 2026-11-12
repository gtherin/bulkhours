// The chat panel. Everything the agent sends is escaped before it is shown;
// formatting is a small, safe subset (code blocks, inline code, bold, links).
// The meters, the "is thinking" line and the motion follow MaQI's lab
// extension (maqi-instance jupyterhub/maqi-lab).
(function () {
  const vscode = acquireVsCodeApi();
  const $ = (id) => document.getElementById(id);
  const log = $("log"), input = $("input"), form = $("ask"), go = $("go"), line = $("budgetline");
  const model = $("model"), thumbs = $("thumbs"), mic = $("mic");
  const budget = $("budget"), context = $("context"), compact = $("compact"), clear = $("clear"), strip = $("tabs");
  const W = JSON.parse($("words").textContent);
  // The school's colour, set here: the page's CSP forbids style attributes.
  if (/^#[0-9a-f]{6}$/i.test(W.accent || "")) document.body.style.setProperty("--accent", W.accent);
  input.placeholder = W.placeholder;
  model.title = W.model;
  const ARROW = '<svg viewBox="0 0 16 16"><path d="M8 2.5 3 7.5l1.1 1.1L7.2 5.5V13.5h1.6V5.5l3.1 3.1L13 7.5z"/></svg>';
  const SQUARE = '<svg viewBox="0 0 16 16"><rect x="4" y="4" width="8" height="8" rx="1.5"/></svg>';
  let busy = false;
  compact.textContent = W.compact; compact.title = W.compactHint;
  clear.textContent = W.clear; clear.title = W.clearHint;
  budget.title = W.budgetTitle;
  context.title = W.contextTitle;

  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  // The agent's Markdown: media/markdown.js (headings, lists, tables, quotes,
  // code), escaped first, tested on its own (test/markdown.test.ts).
  const { markdown, inline, toolOutput } = globalThis.bhMarkdown;

  const STATUS = { pending: "…", in_progress: "⟳", completed: "✓", failed: "✗" };

  function tool(e) {
    const diffs = e.diffs.map((d) =>
      `<details><summary>${esc(d.path)}</summary><pre class="diff">${diffLines(d.oldText, d.newText)}</pre></details>`).join("");
    const out = e.output ? toolOutput(e.output, W.output) : "";
    return `<div class="tool ${e.status}"><span class="st">${STATUS[e.status] || ""}</span> ${esc(e.title)}${diffs}${out}</div>`;
  }

  function diffLines(oldText, newText) {
    const before = (oldText || "").split("\n");
    const after = newText.split("\n");
    const gone = before.filter((l) => !after.includes(l)).map((l) => `<span class="del">- ${esc(l)}</span>`);
    const added = after.filter((l) => !before.includes(l)).map((l) => `<span class="add">+ ${esc(l)}</span>`);
    return [...gone, ...added].join("\n") || esc(W.noChange);
  }

  // Only data:image URLs the extension built itself are ever drawn.
  const picture = (src) => /^data:image\/(png|jpeg|gif|webp);base64,[A-Za-z0-9+/=]+$/.test(src) ? `<img src="${src}" alt="">` : "";

  function entry(e) {
    switch (e.kind) {
      case "user": return `<div class="msg user">${(e.images || []).length ? `<div class="imgs">${e.images.map(picture).join("")}</div>` : ""}${inline(e.text)}</div>`;
      case "agent": return `<div class="msg agent">${markdown(e.text)}</div>`;
      case "thought": return `<details class="thought"><summary>${esc(W.thinking)}</summary>${markdown(e.text)}</details>`;
      case "plan": return `<ol class="plan">${e.entries.map((p) => `<li class="${p.status}">${esc(p.content)}</li>`).join("")}</ol>`;
      case "notice": return `<div class="notice">${esc(e.text)}</div>`;
      case "tool": return tool(e);
      default: return "";
    }
  }

  // -- the meters ------------------------------------------------------------
  // As src/core/meter.ts money(): the school's currency, the panel's language.
  const lang = document.documentElement.lang === "fr" ? "fr-FR" : "en-US";
  const fmt = (v, cur, digits) => new Intl.NumberFormat(lang, { style: "currency", currency: cur || "USD",
    minimumFractionDigits: digits ?? (Number.isInteger(v) ? 0 : 2), maximumFractionDigits: 2 }).format(v);
  const money = (v, cur) => v > 0 && v < 0.01 ? `<${fmt(0.01, cur)}` : fmt(v, cur);
  const tokens = (n) => n < 1000 ? String(n) : `${Number((n < 1e6 ? n / 1000 : n / 1048576).toFixed(1))}${n < 1e6 ? "K" : "M"}`;
  const level = (s, b) => (b <= 0 || s >= b) ? "over" : s >= 0.8 * b ? "warn" : "ok";

  function meters(s) {
    budget.hidden = line.hidden = !s.credits;
    if (s.credits) {
      const pct = s.credits.budget > 0 ? Math.min(100, 100 * s.credits.spent / s.credits.budget) : 100;
      budget.dataset.level = line.dataset.level = level(s.credits.spent, s.credits.budget);
      line.querySelector(".fill").style.width = `${pct}%`;
      budget.textContent = `${money(s.credits.spent, s.credits.currency)} / ${money(s.credits.budget, s.credits.currency)}`;
    }
    const u = s.usage;
    context.querySelector(".txt").textContent = u ? `${tokens(u.used)} / ${tokens(u.size)}` : "";
    const ring = context.querySelector(".ring .used");
    const frac = u && u.size ? Math.min(1, u.used / u.size) : 0;
    ring.setAttribute("stroke-dasharray", `${(frac * 37.7).toFixed(1)} 37.7`);
    context.dataset.level = frac >= 0.75 ? "warn" : "ok";
    context.querySelector(".ring").toggleAttribute("hidden", !u);   // SVG has no .hidden property
    // Always clickable: during a turn the extension asks before stopping it.
    compact.disabled = clear.disabled = false;
    // Compact: the agent's own /compact when it has one, else the extension's
    // (a fresh session handed the condensed conversation).
    compact.hidden = !s.transcript.length;
  }

  // -- one menu: the school's models (with prices), then the student's agents --
  let priceCurrency = "USD";
  const price = (v) => fmt(v, priceCurrency, 2);
  function menu(s) {
    priceCurrency = s.currency || "USD";
    const school = s.models.map((m) => {
      const name = s.modelLabels[m] ? `${m} — ${s.modelLabels[m]}` : m;
      const p = s.modelPrices[m];
      const selected = !s.agentId && m === s.model ? "selected" : "";
      const eyes = (s.modelVision || []).includes(m) ? ` · ${W.seesImages}` : "";
      return `<option value="m:${esc(m)}" ${selected}>${esc((p ? `${name} · ${price(p.in)} / ${price(p.out)}` : name) + eyes)}</option>`;
    }).join("");
    const own = s.agents.filter((a) => a.id).map((a) =>
      `<option value="a:${esc(a.id)}" ${a.id === s.agentId ? "selected" : ""}>${esc(a.label)}</option>`).join("");
    const unit = priceCurrency === "EUR" ? "€" : "$";
    return (school ? `<optgroup label="${esc(W.schoolModels.replace("$", unit))}">${school}</optgroup>` : "")
      + (own ? `<optgroup label="${esc(W.yourAgents)}">${own}</optgroup>` : "");
  }

  // -- dictation: the panel may not use the microphone (VS Code's webview
  // frame does not allow it); the system's dictation types into the box -----
  const os = /Windows/.test(navigator.userAgent) ? "micWindows" : /Macintosh/.test(navigator.userAgent) ? "micMac" : "";
  mic.hidden = !os;
  mic.title = W.mic;
  mic.innerHTML = '<svg viewBox="0 0 16 16"><path d="M8 10a2.5 2.5 0 0 0 2.5-2.5v-4a2.5 2.5 0 0 0-5 0v4A2.5 2.5 0 0 0 8 10zm4-2.5a.75.75 0 0 0-1.5 0 2.5 2.5 0 0 1-5 0 .75.75 0 0 0-1.5 0 4 4 0 0 0 3.25 3.93V13H5.5v1.5h5V13H8.75v-1.57A4 4 0 0 0 12 7.5z"/></svg>';
  let hintTimer = 0;
  // The hint goes where the student looks: in the box, at its full width.
  mic.onclick = () => {
    input.focus();
    input.placeholder = W[os];
    clearTimeout(hintTimer);
    hintTimer = setTimeout(() => { input.placeholder = W.placeholder; }, 8000);
  };

  // -- what the agent is doing: since when, its last sign of life, the tool
  // it runs, what the turn has cost so far. Redrawn every second while busy.
  let lastState = null;
  const ago = (ms) => { const s = Math.max(0, Math.round(ms / 1000)); return s < 60 ? `${s} s` : s < 3600 ? `${Math.floor(s / 60)} min` : `${Math.floor(s / 3600)} h ${String(Math.floor(s / 60) % 60).padStart(2, "0")}`; };
  function drawActivity() {
    const el = log.querySelector(".writing .activity");
    const a = lastState && lastState.activity;
    if (!el || !a) return;
    const now = Date.now();
    const parts = [ago(now - a.since)];
    if (now - a.last > 15_000) parts.push(W.lastActivity.replace("{ago}", ago(now - a.last)));
    if (a.tool) parts.push(a.tool.length > 60 ? `${a.tool.slice(0, 60)}…` : a.tool);
    const c = lastState.credits;
    if (c && a.spentAtStart !== null && c.spent - a.spentAtStart >= 0.01)
      parts.push(W.thisTurn.replace("{cost}", money(c.spent - a.spentAtStart, c.currency)));
    el.textContent = " · " + parts.join(" · ");
  }
  setInterval(drawActivity, 1000);

  // A new tab is the view's own + (the panel's title bar), not a second one here.
  const PENCIL = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M11.1 1.9a1.5 1.5 0 0 1 2.1 0l.9.9a1.5 1.5 0 0 1 0 2.1L6.3 12.7l-3.6.9.9-3.6zM10 4.1 4.9 9.2l-.4 1.5 1.5-.4L11.1 5.2z"/></svg>';

  // -- the tabs: one per conversation, each running on its own. A dot marks a
  // tab whose agent works, a ! one that waits for the student's answer.
  let editing = 0;        // the tab being renamed: the strip is not redrawn under it

  function tabs(s) {
    strip.hidden = !s.signedIn;
    if (editing) return;
    strip.innerHTML = s.tabs.map((x) =>
      `<span class="tab${x.id === s.tab ? " on" : ""}${x.busy ? " busy" : ""}${x.asking ? " asking" : ""}" role="tab" aria-selected="${x.id === s.tab}" data-id="${x.id}">`
      + `<span class="name" title="${esc(x.title ? `${x.title} — ${W.renameHint}` : W.renameHint)}">${esc(x.title || W.newTab)}</span>`
      + (x.id === s.tab && x.named ? `<button type="button" class="ren" title="${esc(W.renameTab)}" aria-label="${esc(W.renameTab)}">${PENCIL}</button>` : "")
      + `<button type="button" class="x" title="${esc(W.closeTab)}" aria-label="${esc(W.closeTab)}">×</button></span>`).join("")
      // The person, at the end of the strip: their picture opens the platform's links.
      + (s.avatar ? `<button type="button" class="me" title="${esc(W.linksTitle)}" aria-label="${esc(W.linksTitle)}">${picture(s.avatar)}</button>` : "");
    strip.querySelectorAll(".tab").forEach((el) => {
      const id = Number(el.dataset.id);
      el.onclick = (ev) => { if (!ev.target.closest(".x") && id !== s.tab) vscode.postMessage({ type: "tab", id }); };
      el.querySelector(".x").onclick = () => vscode.postMessage({ type: "closeTab", id });
      // A conversation is named once it has a question (its record).
      if (s.tabs.find((x) => x.id === id).named) el.querySelector(".name").ondblclick = () => renameTab(el, id);
      const ren = el.querySelector(".ren");
      if (ren) ren.onclick = () => renameTab(el, id);
    });
    const me = strip.querySelector(".me");
    if (me) me.onclick = () => vscode.postMessage({ type: "links" });
    strip.querySelector(".on")?.scrollIntoView({ block: "nearest", inline: "nearest" });
  }

  // Renamed in place: Enter keeps the name, Escape or an empty name drops it.
  function renameTab(el, id) {
    const name = el.querySelector(".name");
    const box = document.createElement("input");
    box.className = "rename";
    box.value = name.textContent === W.newTab ? "" : name.textContent;
    editing = id;
    name.replaceWith(box);
    box.focus();
    box.select();
    let done = false;
    const finish = (keep) => {
      if (done) return;
      done = true;
      editing = 0;
      if (keep && box.value.trim()) vscode.postMessage({ type: "rename", id, title: box.value.trim() });
      if (lastState) tabs(lastState);
    };
    box.onkeydown = (ev) => { if (ev.key === "Enter") finish(true); if (ev.key === "Escape") finish(false); };
    box.onblur = () => finish(true);
  }

  // -- the conversation --------------------------------------------------------
  let shown = 0;          // entries already drawn: only new ones fade in
  let shownTab = 0;       // another tab shown: its entries do not fade in

  function render(s) {
    tabs(s);
    if (!s.signedIn) {
      // Signed in by the machine (MaQI's key file): nothing to click here.
      log.innerHTML = s.interactive === false ? `<div class="welcome"><p>${esc(W.platformOnly)}</p></div>`
        : `<div class="welcome"><p>${esc(W.signInPrompt)}</p><button id="signin">${esc(W.signIn)}</button></div>`;
      if (s.interactive !== false) $("signin").onclick = () => vscode.postMessage({ type: "signIn" });
      form.hidden = true;
      $("meters").hidden = true;
      return;
    }
    form.hidden = false;
    $("meters").hidden = false;
    const atBottom = log.scrollHeight - log.scrollTop - log.clientHeight < 40;
    const switched = s.tab !== shownTab;
    if (switched) { shownTab = s.tab; shown = s.transcript.length; }
    if (s.transcript.length < shown) shown = 0;
    log.innerHTML = s.transcript.length
      ? s.transcript.map((e, i) => entry(e).replace(/^<(\w+) class="/, (m) => i >= shown ? `${m}enter ` : m)).join("")
      : `<div class="welcome"><h2>${esc(W.title)}</h2><p>${esc(W.emptyChat)}</p><div class="suggest">`
        + ["suggestExplain", "suggestBuild", "suggestFaster"].map((k) => `<button type="button">${esc(W[k])}</button>`).join("")
        + `</div></div>`;
    log.querySelectorAll(".suggest button").forEach((b) => b.onclick = () => { input.value = b.textContent; grow(); input.focus(); });
    shown = s.transcript.length;
    const label = s.agentId ? s.agent : (s.modelLabels[s.model] || s.model);
    if (s.starting) log.innerHTML += `<div class="notice">${esc(W.startingAgent)}</div>`;
    else if (s.busy) log.innerHTML += `<div class="writing"><span class="dots" aria-hidden="true"><i></i><i></i><i></i></span>`
      + `<span class="name">${esc(label)}</span> <span class="verb">${esc(W.thinkingVerb)}</span><span class="activity"></span></div>`;
    lastState = s;
    drawActivity();
    drawAsks(s.asks || []);
    if (atBottom || (s.asks || []).length || switched) log.scrollTop = log.scrollHeight;
    busy = s.busy;
    go.classList.toggle("stop", busy);
    go.innerHTML = busy ? SQUARE : ARROW;
    go.title = busy ? W.stop : W.send;
    go.setAttribute("aria-label", go.title);
    linkFiles();
    model.innerHTML = menu(s);
    model.title = s.agentId ? s.agent : W.model;
    meters(s);
  }

  // A path the agent writes as code opens in the editor (src/core/fileLinks.ts
  // parseFileRef holds the same pattern, tested there).
  const REF = /^(\/?[\w.@+-]+(?:\/[\w.@+-]+)*\.[A-Za-z0-9]{1,8})(?::(\d{1,7})(?:-(\d{1,7}))?)?$/;
  function linkFiles() {
    log.querySelectorAll(".msg.agent :not(pre) > code").forEach((c) => {
      const m = REF.exec(c.textContent.trim());
      if (!m || m[1].includes("..")) return;
      c.classList.add("ref");
      c.title = W.openInEditor;
      c.onclick = () => vscode.postMessage({ type: "openFile", path: m[1], ...(m[2] ? { line: +m[2] } : {}), ...(m[3] ? { endLine: +m[3] } : {}) });
    });
  }

  // Permission prompts waiting for the student: part of the shown tab's
  // state, drawn again after every render - a prompt that vanished left the
  // agent waiting forever (owner, 2026-11-10: "why is that freeze?" -
  // Claude Code asking to run `ls`).
  function drawAsks(asks) {
    for (const p of asks) {
      const box = document.createElement("div");
      box.className = "ask";
      box.innerHTML = `<p>${esc(p.title)}</p>` + p.options.map((o) =>
        `<button data-id="${esc(o.id)}" class="${o.kind.startsWith("allow") ? "allow" : "reject"}">${esc(o.name)}</button>`).join("");
      box.querySelectorAll("button").forEach((b) => b.onclick = () => {
        vscode.postMessage({ type: "permission", id: p.id, optionId: b.dataset.id });
        box.remove();
      });
      log.appendChild(box);
    }
  }

  // -- pasted pictures ---------------------------------------------------------
  const MAX_IMAGES = 4, MAX_BYTES = 5 * 1024 * 1024;
  let pasted = [];

  function drawThumbs() {
    thumbs.hidden = !pasted.length;
    thumbs.innerHTML = pasted.map((p, i) =>
      `<span class="thumb">${picture(`data:${p.mimeType};base64,${p.data}`)}<button type="button" data-i="${i}" title="${esc(W.removeImage)}">×</button></span>`).join("");
    thumbs.querySelectorAll("button").forEach((b) => b.onclick = () => { pasted.splice(Number(b.dataset.i), 1); drawThumbs(); });
  }

  input.addEventListener("paste", (ev) => {
    const files = [...(ev.clipboardData?.items || [])].filter((i) => i.kind === "file" && /^image\/(png|jpeg|gif|webp)$/.test(i.type));
    if (!files.length) return;
    ev.preventDefault();
    for (const item of files) {
      const f = item.getAsFile();
      if (!f || f.size > MAX_BYTES || pasted.length >= MAX_IMAGES) continue;
      const r = new FileReader();
      r.onload = () => {
        const [, mimeType, data] = String(r.result).match(/^data:([^;]+);base64,(.*)$/) || [];
        if (mimeType && pasted.length < MAX_IMAGES) { pasted.push({ mimeType, data }); drawThumbs(); }
      };
      r.readAsDataURL(f);
    }
  });

  window.addEventListener("message", (ev) => {
    if (ev.data.type === "state") render(ev.data);
    // From the editor (Ask MaQI): a file or selection, added to what is typed.
    if (ev.data.type === "insert") {
      input.value = (input.value && !/\s$/.test(input.value) ? input.value + "\n" : input.value) + ev.data.text;
      grow();
      input.focus();
    }
  });
  // The text box grows with what is typed, up to its max-height.
  function grow() { input.style.height = "auto"; input.style.height = `${input.scrollHeight}px`; }
  input.addEventListener("input", grow);
  form.addEventListener("submit", (ev) => {
    ev.preventDefault();
    if (busy || !input.value.trim()) return;     // Enter mid-turn keeps the text
    vscode.postMessage({ type: "send", text: input.value, images: pasted });
    input.value = "";
    grow();
    pasted = [];
    drawThumbs();
  });
  input.addEventListener("keydown", (ev) => {
    if (ev.key === "Enter" && !ev.shiftKey) { ev.preventDefault(); form.requestSubmit(); }
  });
  // One round button: send, or stop while the agent works.
  go.addEventListener("click", (ev) => { if (busy) { ev.preventDefault(); vscode.postMessage({ type: "cancel" }); } });
  model.onchange = () => {
    const [kind, id] = [model.value.slice(0, 1), model.value.slice(2)];
    vscode.postMessage(kind === "a" ? { type: "choose", agent: id } : { type: "choose", agent: "", model: id });
  };
  compact.onclick = () => vscode.postMessage({ type: "compact" });
  clear.onclick = () => vscode.postMessage({ type: "clear" });
  vscode.postMessage({ type: "ready" });
})();
