// One school = one build file = one extension. The file holds what must be
// known before sign-in (identity and addresses); models and the agent come
// from the school's key server after it. Checked once, at build time.
import { colour, failer, https, text } from "./fields.ts";
import type { Lang } from "./i18n.ts";

export type School = {
  id: string;
  name: string;
  accent: string;
  signInUrl: string;
  keyUrl: string;
  // What this student spent of their budget, for the panel's meter.
  creditsUrl: string;
  // Where this school's builds and latest.json are published (updates until
  // the extension is on the Marketplace). Optional.
  downloadUrl?: string;
  // The interface language when VS Code's own is one we do not speak.
  language: Lang;
  // gateka, maqi, ipsa, bulkhours: one code, a config file each (owner,
  // 2026-11-12). The title names the variant everywhere (panel, menus,
  // messages); the prefix names its commands, view and settings, so two
  // variants installed side by side never collide.
  title: string;
  prefix: string;
  // The extension tile's background, its mark drawn in the accent; without
  // it the mark is white on the accent. Optional.
  tile?: string;
};

export function parseSchool(raw: unknown): School {
  const o = (raw ?? {}) as Record<string, unknown>;
  if (typeof o.id !== "string" || !/^[a-z0-9-]+$/.test(o.id)) {
    throw new Error("school id must be lowercase letters, digits or dashes");
  }
  const fail = failer(`school ${o.id}`);
  return {
    id: o.id,
    name: text(o, "name", fail),
    accent: colour(o, "accent", fail),
    signInUrl: https(o, "signInUrl", fail),
    keyUrl: https(o, "keyUrl", fail),
    creditsUrl: https(o, "creditsUrl", fail),
    ...(o.downloadUrl !== undefined ? { downloadUrl: https(o, "downloadUrl", fail) } : {}),
    language: language(o.language, fail),
    title: o.title === undefined ? `BulkHours ${text(o, "name", fail)}` : text(o, "title", fail),
    prefix: prefix(o.prefix, fail),
    ...(o.tile !== undefined ? { tile: colour(o, "tile", fail) } : {}),
  };
}

// The extension's name, and its builds' file names: bulkhours-ipsa, maqi.
export function packageName(s: Pick<School, "id" | "prefix">): string {
  return s.prefix === s.id ? s.id : `${s.prefix}-${s.id}`;
}

function prefix(v: unknown, fail: (m: string) => never): string {
  if (v === undefined) return "bulkhours";
  return typeof v === "string" && /^[a-z][a-z0-9]{1,30}$/.test(v) ? v : fail(`"prefix" must be lowercase letters and digits`);
}

function language(v: unknown, fail: (m: string) => never): Lang {
  if (v === undefined) return "en";
  return v === "fr" || v === "en" ? v : fail(`"language" must be fr or en`);
}
