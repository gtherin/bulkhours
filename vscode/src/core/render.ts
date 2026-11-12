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

// A session's own page (<run directory>/renders/*.html), shown in a tab: its
// files beside it resolve (base), scripts may come from the page and from the
// usual chart CDNs, pictures and data only from the page itself, and nothing
// can be sent anywhere - a picture address is a way out too.
const CDNS = "https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://cdn.plot.ly https://unpkg.com";
export function pageHtml(html: string, baseHref: string, source: string): string {
  const csp = `default-src 'none'; script-src ${source} 'unsafe-inline' 'unsafe-eval' ${CDNS}; `
    + `style-src ${source} 'unsafe-inline' ${CDNS}; font-src ${source} data: ${CDNS}; `
    + `img-src ${source} data: blob:; media-src ${source} data: blob:; worker-src blob:; connect-src 'none';`;
  const head = `<meta http-equiv="Content-Security-Policy" content="${csp}"><base href="${baseHref}">`;
  return /<head[^>]*>/i.test(html) ? html.replace(/<head[^>]*>/i, (h) => `${h}${head}`) : `${head}${html}`;
}

export function showable(html: string): string {
  const meta = `<meta http-equiv="Content-Security-Policy" content="${RENDER_CSP}">`;
  return /<head[^>]*>/i.test(html) ? html.replace(/<head[^>]*>/i, (h) => `${h}${meta}`) : `${meta}${html}`;
}
