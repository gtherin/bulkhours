// The link between the chat and the editor (owner, 2026-11-12: "a link
// between the maqi chat and the rest of vscode"): a path the agent writes
// as code (`topic_hormuz.py:42`) opens in the editor; a file or a selection
// sent from the editor arrives in the chat as a reference.
export type FileRef = { path: string; line?: number; endLine?: number };

// "src/a.py", "a.py:42", "a.py:42-50", "notebooks/x.ipynb": a relative or
// absolute path with an extension, optionally lines. Nothing else is a link.
const REF = /^(\/?[\w.@+-]+(?:\/[\w.@+-]+)*\.[A-Za-z0-9]{1,8})(?::(\d{1,7})(?:-(\d{1,7}))?)?$/;

export function parseFileRef(text: string): FileRef | undefined {
  const m = REF.exec(text.trim());
  if (!m || m[1].includes("..")) return undefined;
  return { path: m[1], ...(m[2] ? { line: Number(m[2]) } : {}), ...(m[3] ? { endLine: Number(m[3]) } : {}) };
}

// What goes into the chat box for a file or a selection from the editor.
export function referenceText(path: string, sel?: { start: number; end: number; text: string; language: string }): string {
  if (!sel || !sel.text.trim()) return `\`${path}\` `;
  const lines = sel.start === sel.end ? `${sel.start}` : `${sel.start}-${sel.end}`;
  const fence = sel.text.includes("```") ? "````" : "```";
  return `\`${path}:${lines}\`\n${fence}${sel.language}\n${sel.text.replace(/\n$/, "")}\n${fence}\n`;
}
