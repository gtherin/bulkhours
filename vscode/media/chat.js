// The chat panel. Everything the agent sends is escaped before it is shown;
// formatting is a small, safe subset (code blocks, inline code, bold, links).
(function () {
  const vscode = acquireVsCodeApi();
  const log = document.getElementById("log");
  const input = document.getElementById("input");
  const form = document.getElementById("ask");
  const stop = document.getElementById("stop");
  const send = document.getElementById("send");
  const model = document.getElementById("model");
  const agent = document.getElementById("agent");
  const W = JSON.parse(document.getElementById("words").textContent);
  input.placeholder = W.placeholder;
  send.textContent = W.send;
  stop.textContent = W.stop;
  model.title = W.model;

  const esc = (s) => s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

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

  function entry(e) {
    switch (e.kind) {
      case "user": return `<div class="msg user">${inline(e.text)}</div>`;
      case "agent": return `<div class="msg agent">${markdown(e.text)}</div>`;
      case "thought": return `<details class="thought"><summary>${esc(W.thinking)}</summary>${markdown(e.text)}</details>`;
      case "plan": return `<ol class="plan">${e.entries.map((p) => `<li class="${p.status}">${esc(p.content)}</li>`).join("")}</ol>`;
      case "notice": return `<div class="notice">${esc(e.text)}</div>`;
      case "tool": return tool(e);
      default: return "";
    }
  }

  function render(s) {
    if (!s.signedIn) {
      log.innerHTML = `<div class="welcome"><p>${esc(W.signInPrompt)}</p>
        <button id="signin">${esc(W.signIn)}</button></div>`;
      document.getElementById("signin").onclick = () => vscode.postMessage({ type: "signIn" });
      form.hidden = true;
      return;
    }
    form.hidden = false;
    const atBottom = log.scrollHeight - log.scrollTop - log.clientHeight < 40;
    log.innerHTML = s.transcript.length ? s.transcript.map(entry).join("")
      : `<div class="welcome"><p>${esc(W.emptyChat)}</p></div>`;
    if (s.starting) log.innerHTML += `<div class="notice">${esc(W.startingAgent)}</div>`;
    if (atBottom) log.scrollTop = log.scrollHeight;
    stop.hidden = !s.busy;
    send.disabled = s.busy;
    model.innerHTML = s.models.map((m) => `<option ${m === s.model ? "selected" : ""}>${esc(m)}</option>`).join("");
    agent.textContent = s.agent;
  }

  function permission(p) {
    const box = document.createElement("div");
    box.className = "ask";
    box.innerHTML = `<p>${esc(p.title)}</p>` + p.options.map((o) =>
      `<button data-id="${esc(o.id)}" class="${o.kind.startsWith("allow") ? "allow" : "reject"}">${esc(o.name)}</button>`).join("");
    box.querySelectorAll("button").forEach((b) => b.onclick = () => {
      vscode.postMessage({ type: "permission", id: p.id, optionId: b.dataset.id });
      box.remove();
    });
    log.appendChild(box);
    log.scrollTop = log.scrollHeight;
  }

  window.addEventListener("message", (ev) => {
    if (ev.data.type === "state") render(ev.data);
    if (ev.data.type === "permission") permission(ev.data);
  });
  form.addEventListener("submit", (ev) => {
    ev.preventDefault();
    vscode.postMessage({ type: "send", text: input.value });
    input.value = "";
  });
  input.addEventListener("keydown", (ev) => {
    if (ev.key === "Enter" && !ev.shiftKey) { ev.preventDefault(); form.requestSubmit(); }
  });
  stop.onclick = () => vscode.postMessage({ type: "cancel" });
  model.onchange = () => vscode.postMessage({ type: "model", model: model.value });
  vscode.postMessage({ type: "ready" });
})();
