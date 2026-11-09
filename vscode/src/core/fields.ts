// Field readers for data that enters from outside (school files, key server
// replies). Each throws `<where>: <what is wrong>`; callers stay flat.

type Obj = Record<string, unknown>;
export type Fail = (msg: string) => never;

export function failer(where: string): Fail {
  return (msg) => { throw new Error(`${where}: ${msg}`); };
}

export function text(o: Obj, k: string, fail: Fail): string {
  const v = o[k];
  return typeof v === "string" && v !== "" ? v : fail(`"${k}" must be a non-empty string`);
}

export function https(o: Obj, k: string, fail: Fail, label = "an https address"): string {
  const v = o[k];
  return typeof v === "string" && v.startsWith("https://") ? v : fail(`"${k}" must be ${label}`);
}

export function colour(o: Obj, k: string, fail: Fail): string {
  const v = o[k];
  return typeof v === "string" && /^#[0-9a-fA-F]{6}$/.test(v) ? v : fail(`"${k}" must be a #rrggbb colour`);
}

export function date(o: Obj, k: string, fail: Fail): number {
  const v = typeof o[k] === "string" ? Date.parse(o[k] as string) : NaN;
  return Number.isNaN(v) ? fail(`"${k}" is not a date`) : v;
}

export function names(o: Obj, k: string, fail: Fail): string[] {
  const v = o[k];
  return Array.isArray(v) && v.length > 0 && v.every((x) => typeof x === "string")
    ? (v as string[]) : fail(`"${k}" must be a non-empty list`);
}
