// A dashboard in an editor tab (owner, 2026-11-12: "we need to be able to
// display a dashboard in a tab"): the app runs on the machine (Streamlit on
// 8501 by default, marimo, Panel...), VS Code turns its local port into an
// address the browser reaches (code-server: <its address>/proxy/<port>/,
// behind the same sign-in) and shows it beside the code.
export const DEFAULT_PORT = 8501;

export function parsePort(text: string | undefined): number | undefined {
  const t = (text ?? "").trim();
  if (!/^\d{2,5}$/.test(t)) return undefined;
  const n = Number(t);
  return n >= 1024 && n <= 65535 ? n : undefined;
}
