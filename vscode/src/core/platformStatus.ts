// A platform's own status bar (MaQI: memory, CPU, data rights, idle, egress,
// as JupyterLab's MaQI bar shows them). The platform's command computes them
// with its own code and prints {"items": [{id, text, tooltip, level}]}; the
// extension only shows what it prints, after checking each item.
export type StatusItem = { id: string; text: string; tooltip: string; level: "ok" | "warn" | "error" };

const LEVELS = new Set(["ok", "warn", "error"]);
const TEXT_MAX = 80;
const TOOLTIP_MAX = 2000;

export function parseStatus(out: string): StatusItem[] {
  let raw: unknown;
  try { raw = JSON.parse(out); } catch { return []; }
  const items = (raw as { items?: unknown })?.items;
  if (!Array.isArray(items)) return [];
  return items.flatMap((i: Record<string, unknown>) => {
    if (typeof i?.id !== "string" || !/^[a-z0-9-]{1,32}$/.test(i.id) || typeof i.text !== "string") return [];
    return [{
      id: i.id,
      text: i.text.slice(0, TEXT_MAX),
      tooltip: typeof i.tooltip === "string" ? i.tooltip.slice(0, TOOLTIP_MAX) : "",
      level: (LEVELS.has(i.level as string) ? i.level : "ok") as StatusItem["level"],
    }];
  });
}
