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
  // The interface language when VS Code's own is one we do not speak.
  language: Lang;
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
    language: language(o.language, fail),
  };
}

function language(v: unknown, fail: (m: string) => never): Lang {
  if (v === undefined) return "en";
  return v === "fr" || v === "en" ? v : fail(`"language" must be fr or en`);
}
