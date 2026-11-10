// The chat panel. Everything the agent sends is escaped before it is shown;
// formatting is a small, safe subset (code blocks, inline code, bold, links).
// The meters, the "is thinking" line and the motion follow MaQI's lab
// extension (maqi-instance jupyterhub/maqi-lab).
(function () {
  const vscode = acquireVsCodeApi();
  const $ = (id) => document.getElementById(id);
  const log = $("log"), input = $("input"), form = $("ask"), go = $("go"), line = $("budgetline");
  const model = $("model"), thumbs = $("thumbs"), mic = $("mic");
  const budget = $("budget"), context = $("context"), compact = $("compact"), clear = $("clear");
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
  const { markdown, inline } = globalThis.bhMarkdown;

  const STATUS = { pending: "…", in_progress: "⟳", completed: "✓", failed: "✗" };

  function tool(e) {
    const diffs = e.diffs.map((d) =>
      `<details><summary>${esc(d.path)}</summary><pre class="diff">${diffLines(d.oldText, d.newText)}</pre></details>`).join("");
    const out = e.output ? `<details><summary>${esc(W.output)}</summary><pre>${esc(e.output.slice(0, 4000))}</pre></details>` : "";
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
  const money = (v) => v === 0 ? "$0" : v < 0.01 ? "<$0.01" : Number.isInteger(v) ? `$${v}` : `$${v.toFixed(2)}`;
  const tokens = (n) => n < 1000 ? String(n) : `${Number((n < 1e6 ? n / 1000 : n / 1048576).toFixed(1))}${n < 1e6 ? "K" : "M"}`;
  const level = (s, b) => (b <= 0 || s >= b) ? "over" : s >= 0.8 * b ? "warn" : "ok";

  function meters(s) {
    budget.hidden = line.hidden = !s.credits;
    if (s.credits) {
      const pct = s.credits.budget > 0 ? Math.min(100, 100 * s.credits.spent / s.credits.budget) : 100;
      budget.dataset.level = line.dataset.level = level(s.credits.spent, s.credits.budget);
      line.querySelector(".fill").style.width = `${pct}%`;
      budget.textContent = `${money(s.credits.spent)} / ${money(s.credits.budget)}`;
    }
    const u = s.usage;
    context.querySelector(".txt").textContent = u ? `${tokens(u.used)} / ${tokens(u.size)}` : "";
    const ring = context.querySelector(".ring .used");
    const frac = u && u.size ? Math.min(1, u.used / u.size) : 0;
    ring.setAttribute("stroke-dasharray", `${(frac * 37.7).toFixed(1)} 37.7`);
    context.dataset.level = frac >= 0.75 ? "warn" : "ok";
    context.querySelector(".ring").toggleAttribute("hidden", !u);   // SVG has no .hidden property
    compact.disabled = clear.disabled = s.busy;
    compact.hidden = !(s.commands || []).includes("compact");   // only an agent that offers it
  }

  // -- one menu: the school's models (with prices), then the student's agents --
  const price = (v) => `$${v.toFixed(2)}`;
  function menu(s) {
    const school = s.models.map((m) => {
      const name = s.modelLabels[m] ? `${m} — ${s.modelLabels[m]}` : m;
      const p = s.modelPrices[m];
      const selected = !s.agentId && m === s.model ? "selected" : "";
      return `<option value="m:${esc(m)}" ${selected}>${esc(p ? `${name} · ${price(p.in)} / ${price(p.out)}` : name)}</option>`;
    }).join("");
    const own = s.agents.filter((a) => a.id).map((a) =>
      `<option value="a:${esc(a.id)}" ${a.id === s.agentId ? "selected" : ""}>${esc(a.label)}</option>`).join("");
    return (school ? `<optgroup label="${esc(W.schoolModels)}">${school}</optgroup>` : "")
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

  // -- the conversation --------------------------------------------------------
  let shown = 0;          // entries already drawn: only new ones fade in

  function render(s) {
    if (!s.signedIn) {
      log.innerHTML = `<div class="welcome"><p>${esc(W.signInPrompt)}</p>
        <button id="signin">${esc(W.signIn)}</button></div>`;
      $("signin").onclick = () => vscode.postMessage({ type: "signIn" });
      form.hidden = true;
      $("meters").hidden = true;
      return;
    }
    form.hidden = false;
    $("meters").hidden = false;
    const atBottom = log.scrollHeight - log.scrollTop - log.clientHeight < 40;
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
      + `<span class="name">${esc(label)}</span> <span class="verb">${esc(W.thinkingVerb)}</span></div>`;
    if (!s.busy) asks.clear();            // a finished turn leaves no question open
    drawAsks();
    if (atBottom || asks.size) log.scrollTop = log.scrollHeight;
    busy = s.busy;
    go.classList.toggle("stop", busy);
    go.innerHTML = busy ? SQUARE : ARROW;
    go.title = busy ? W.stop : W.send;
    go.setAttribute("aria-label", go.title);
    model.innerHTML = menu(s);
    model.title = s.agentId ? s.agent : W.model;
    meters(s);
  }

  // Permission prompts waiting for the student. Kept HERE and drawn again
  // after every render: the log is rebuilt at each update, and a prompt that
  // vanished left the agent waiting forever (owner, 2026-11-10: "why is
  // that freeze?" - Claude Code asking to run `ls`).
  const asks = new Map();

  function drawAsks() {
    for (const p of asks.values()) {
      const box = document.createElement("div");
      box.className = "ask";
      box.innerHTML = `<p>${esc(p.title)}</p>` + p.options.map((o) =>
        `<button data-id="${esc(o.id)}" class="${o.kind.startsWith("allow") ? "allow" : "reject"}">${esc(o.name)}</button>`).join("");
      box.querySelectorAll("button").forEach((b) => b.onclick = () => {
        asks.delete(p.id);
        vscode.postMessage({ type: "permission", id: p.id, optionId: b.dataset.id });
        box.remove();
      });
      log.appendChild(box);
    }
  }

  function permission(p) {
    asks.set(p.id, p);
    log.querySelectorAll(".ask").forEach((b) => b.remove());
    drawAsks();
    log.scrollTop = log.scrollHeight;
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
    if (ev.data.type === "permission") permission(ev.data);
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
