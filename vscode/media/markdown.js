// The agent's Markdown, as HTML the panel can show safely. Everything is
// escaped FIRST; only the tags written here come out, and a link keeps its
// href only for https/http/file. A plain script (no import/export): the panel
// loads it before chat.js, and the tests import it the same way.
(function () {
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  // Inline: code spans first, so nothing inside them is formatted.
  function inline(s) {
    return String(s).split(/(`[^`\n]+`)/).map((part, i) => {
      if (i % 2 === 1) return `<code>${esc(part.slice(1, -1))}</code>`;
      return esc(part)
        .replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (_, t, u) => /^(https?|file):/.test(u) ? `<a href="${u}">${t}</a>` : t)
        .replace(/\*\*(?=\S)(.+?)\*\*/g, "<strong>$1</strong>")
        .replace(/__(?=\S)(.+?)__/g, "<strong>$1</strong>")
        .replace(/(^|[^*\w])\*(?=\S)([^*]+?)\*(?!\*)/g, "$1<em>$2</em>")
        .replace(/(^|[^_\w])_(?=\S)([^_]+?)_(?!\w)/g, "$1<em>$2</em>")
        .replace(/~~(?=\S)(.+?)~~/g, "<del>$1</del>");
    }).join("");
  }

  const HEADING = /^(#{1,6})\s+(.*?)\s*#*\s*$/;
  const RULE = /^\s*([-*_])(\s*\1){2,}\s*$/;
  const ITEM = /^(\s*)([-*+]|\d+[.)])\s+(.*)$/;
  const QUOTE = /^\s*>\s?(.*)$/;
  const isTable = (a, b) => /\|/.test(a) && /^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$/.test(b || "");
  const startsBlock = (l, next) => HEADING.test(l) || RULE.test(l) || ITEM.test(l) || QUOTE.test(l) || isTable(l, next);

  function cells(row) {
    return row.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((c) => c.trim());
  }

  function table(lines) {
    const [head, , ...rows] = lines;
    const th = cells(head).map((c) => `<th>${inline(c)}</th>`).join("");
    const tb = rows.map((r) => `<tr>${cells(r).map((c) => `<td>${inline(c)}</td>`).join("")}</tr>`).join("");
    return `<div class="table"><table><thead><tr>${th}</tr></thead><tbody>${tb}</tbody></table></div>`;
  }

  // A list from consecutive item lines (and their indented continuations);
  // deeper indentation nests.
  function list(lines) {
    const items = [];
    for (const l of lines) {
      const m = l.match(ITEM);
      if (m) items.push({ indent: m[1].replace(/\t/g, "    ").length, ordered: /\d/.test(m[2]), text: m[3], start: parseInt(m[2], 10) });
      else if (items.length) items[items.length - 1].text += " " + l.trim();
    }
    let i = 0;
    function level(indent) {
      const first = items[i];
      const tag = first.ordered ? "ol" : "ul";
      const start = first.ordered && first.start > 1 ? ` start="${first.start}"` : "";
      let html = `<${tag}${start}>`;
      while (i < items.length && items[i].indent >= indent) {
        const it = items[i++];
        html += `<li>${inline(it.text)}`;
        if (i < items.length && items[i].indent > it.indent) html += level(items[i].indent);
        html += "</li>";
      }
      return html + `</${tag}>`;
    }
    let out = "";
    while (i < items.length) out += level(items[i].indent);
    return out;
  }

  function blocks(text) {
    const lines = text.split("\n");
    const out = [];
    let i = 0;
    while (i < lines.length) {
      const l = lines[i];
      if (!l.trim()) { i++; continue; }
      let m;
      if ((m = l.match(HEADING))) {
        const n = Math.min(6, m[1].length + 2);           // # -> h3: the panel is narrow
        out.push(`<h${n}>${inline(m[2])}</h${n}>`); i++;
      } else if (RULE.test(l)) {
        out.push("<hr>"); i++;
      } else if (isTable(l, lines[i + 1])) {
        const t = [l, lines[i + 1]]; i += 2;
        while (i < lines.length && /\|/.test(lines[i]) && lines[i].trim()) t.push(lines[i++]);
        out.push(table(t));
      } else if (QUOTE.test(l)) {
        const q = [];
        while (i < lines.length && QUOTE.test(lines[i])) q.push(lines[i++].match(QUOTE)[1]);
        out.push(`<blockquote>${blocks(q.join("\n"))}</blockquote>`);
      } else if (ITEM.test(l)) {
        const items = [];
        while (i < lines.length && lines[i].trim() && (ITEM.test(lines[i]) || /^\s{2,}\S/.test(lines[i]))) items.push(lines[i++]);
        out.push(list(items));
      } else {
        const p = [];
        while (i < lines.length && lines[i].trim() && !(p.length && startsBlock(lines[i], lines[i + 1]))) p.push(lines[i++]);
        out.push(`<p>${p.map(inline).join("<br>")}</p>`);
      }
    }
    return out.join("");
  }

  function markdown(s) {
    return String(s).split(/```/).map((part, i) => {
      if (i % 2 === 1) return `<pre><code>${esc(part.replace(/^[\w+-]*\n/, ""))}</code></pre>`;
      return blocks(part);
    }).join("");
  }

  globalThis.bhMarkdown = { markdown, inline, esc };
})();
