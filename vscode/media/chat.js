// The chat panel. Everything the agent sends is escaped before it is shown;
// formatting is a small, safe subset (code blocks, inline code, bold, links).
// The meters, the "is thinking" line and the motion follow MaQI's lab
// extension (maqi-instance jupyterhub/maqi-lab).
(function () {
  const vscode = acquireVsCodeApi();
  const $ = (id) => document.getElementById(id);
  const log = $("log"), input = $("input"), form = $("ask"), stop = $("stop"), send = $("send");
  const model = $("model"), agent = $("agent"), thumbs = $("thumbs");
  const budget = $("budget"), context = $("context"), compact = $("compact"), clear = $("clear");
  const W = JSON.parse($("words").textContent);
  // The school's colour, set here: the page's CSP forbids style attributes.
  if (/^#[0-9a-f]{6}$/i.test(W.accent || "")) document.body.style.setProperty("--accent", W.accent);
  input.placeholder = W.placeholder;
  send.textContent = W.send;
  stop.textContent = W.stop;
  model.title = W.model;
  compact.textContent = W.compact; compact.title = W.compactHint;
  clear.textContent = W.clear; clear.title = W.clearHint;
  budget.title = W.budgetTitle;
  context.title = W.contextTitle;

  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  function inline(s) {
    return esc(s)
      .replace(/`([^`]+)`/g, "<code>$1</code>")
      .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
      .replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (_, t, u) => /^(https?|file):/.test(u) ? `<a href="${u}">${t}</a>` : t);
  }

  function markdown(s) {
    return s.split(/```/).map((part, i) => {
      if (i % 2 === 1) {
        const body = part.replace(/^[\w+-]*\n/, "");
        return `<pre><code>${esc(body)}</code></pre>`;
      }
      return part.split(/\n{2,}/).filter((p) => p.trim()).map((p) => `<p>${inline(p).replace(/\n/g, "<br>")}</p>`).join("");
    }).join("");
  }

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
    budget.hidden = !s.credits;
    if (s.credits) {
      const pct = s.credits.budget > 0 ? Math.min(100, 100 * s.credits.spent / s.credits.budget) : 100;
      budget.dataset.level = level(s.credits.spent, s.credits.budget);
      budget.querySelector(".fill").style.width = `${pct}%`;
      budget.querySelector(".txt").textContent = `${money(s.credits.spent)} / ${money(s.credits.budget)}`;
    }
    const u = s.usage;
    context.querySelector(".txt").textContent = u ? `${tokens(u.used)} / ${tokens(u.size)}` : "";
    const ring = context.querySelector(".ring .used");
    const frac = u && u.size ? Math.min(1, u.used / u.size) : 0;
    ring.setAttribute("stroke-dasharray", `${(frac * 37.7).toFixed(1)} 37.7`);
    context.dataset.level = frac >= 0.75 ? "warn" : "ok";
    context.querySelector(".ring").toggleAttribute("hidden", !u);   // SVG has no .hidden property
    compact.disabled = clear.disabled = s.busy;
  }

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
      : `<div class="welcome"><p>${esc(W.emptyChat)}</p></div>`;
    shown = s.transcript.length;
    const label = s.modelLabels[s.model] || s.model;
    if (s.starting) log.innerHTML += `<div class="notice">${esc(W.startingAgent)}</div>`;
    else if (s.busy) log.innerHTML += `<div class="writing"><span class="dots" aria-hidden="true"><i></i><i></i><i></i></span>`
      + `<span class="name">${esc(label)}</span> <span class="verb">${esc(W.thinkingVerb)}</span></div>`;
    if (atBottom) log.scrollTop = log.scrollHeight;
    stop.hidden = !s.busy;
    send.disabled = s.busy;
    model.innerHTML = s.models.map((m) =>
      `<option value="${esc(m)}" ${m === s.model ? "selected" : ""}>${esc(s.modelLabels[m] ? `${m} — ${s.modelLabels[m]}` : m)}</option>`).join("");
    agent.textContent = s.agent;
    agent.title = s.agent;
    meters(s);
  }

  function permission(p) {
    const box = document.createElement("div");
    box.className = "ask enter";
    box.innerHTML = `<p>${esc(p.title)}</p>` + p.options.map((o) =>
      `<button data-id="${esc(o.id)}" class="${o.kind.startsWith("allow") ? "allow" : "reject"}">${esc(o.name)}</button>`).join("");
    box.querySelectorAll("button").forEach((b) => b.onclick = () => {
      vscode.postMessage({ type: "permission", id: p.id, optionId: b.dataset.id });
      box.remove();
    });
    log.appendChild(box);
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
  form.addEventListener("submit", (ev) => {
    ev.preventDefault();
    vscode.postMessage({ type: "send", text: input.value, images: pasted });
    input.value = "";
    pasted = [];
    drawThumbs();
  });
  input.addEventListener("keydown", (ev) => {
    if (ev.key === "Enter" && !ev.shiftKey) { ev.preventDefault(); form.requestSubmit(); }
  });
  stop.onclick = () => vscode.postMessage({ type: "cancel" });
  model.onchange = () => vscode.postMessage({ type: "model", model: model.value });
  agent.onclick = () => vscode.postMessage({ type: "pickAgent" });
  compact.onclick = () => vscode.postMessage({ type: "compact" });
  clear.onclick = () => vscode.postMessage({ type: "clear" });
  vscode.postMessage({ type: "ready" });
})();
