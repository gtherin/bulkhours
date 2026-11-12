// A marimo notebook's rendered page in a VS Code tab (owner, 2026-11-12:
// "please also add the html renderer... in visual"): the notebook stays a
// .py next to the code, its page is exported (marimo export html) and shown,
// again at each save. Pure parts here, tested; the VS Code glue in
// src/vscode/renderEditor.ts.

// A marimo notebook declares itself: `import marimo` and `marimo.App(`.
export function isMarimo(source: string): boolean {
  return /^\s*import marimo\b/m.test(source) && /\bmarimo\.App\(/.test(source);
}

// Which marimo to run, first that exists: the one set by the person, the one
// beside their default Python (it can import what the notebook imports), then
// whatever "marimo" the PATH gives.
export function marimoCandidates(setting: string | undefined, interpreter: string | undefined): string[] {
  const out: string[] = [];
  if (setting?.trim()) out.push(setting.trim());
  if (interpreter?.includes("/")) out.push(interpreter.replace(/\/[^/]+$/, "/marimo"));
  out.push("marimo");
  return [...new Set(out)];
}

// The exported page, made showable in a webview: marimo's static page loads
// its own code from jsdelivr and keeps the results inline; nothing else may
// load, nothing may be sent anywhere (connect-src none).
export const RENDER_CSP = "default-src 'none'; script-src https://cdn.jsdelivr.net 'unsafe-inline' 'unsafe-eval'; "
  + "style-src https://cdn.jsdelivr.net 'unsafe-inline'; font-src https://cdn.jsdelivr.net data:; "
  + "img-src data: blob: https://cdn.jsdelivr.net; worker-src blob:; connect-src 'none';";

export function showable(html: string): string {
  const meta = `<meta http-equiv="Content-Security-Policy" content="${RENDER_CSP}">`;
  return /<head[^>]*>/i.test(html) ? html.replace(/<head[^>]*>/i, (h) => `${h}${meta}`) : `${meta}${html}`;
}
