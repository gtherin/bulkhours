// Updating the extension from the school's download area, until it is on the
// Marketplace (which updates by itself). The area holds latest.json,
// {"<school>": "<version>"}, beside the VSIX files it names.

export function newer(candidate: string, current: string): boolean {
  const parse = (v: string) => /^\d+(\.\d+)*$/.test(v) ? v.split(".").map(Number) : undefined;
  const a = parse(candidate), b = parse(current);
  if (!a || !b) return false;
  for (let i = 0; i < Math.max(a.length, b.length); i++) {
    const d = (a[i] ?? 0) - (b[i] ?? 0);
    if (d) return d > 0;
  }
  return false;
}

export function offeredUpdate(latest: Record<string, unknown>, school: string, current: string,
                              area: string): { version: string; url: string } | undefined {
  const v = latest[school];
  if (typeof v !== "string" || !newer(v, current) || !/^https:\/\//.test(area)) return undefined;
  return { version: v, url: new URL(`bulkhours-${school}-${v}.vsix`, area.endsWith("/") ? area : `${area}/`).toString() };
}
