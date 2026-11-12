// One school = one build file = one extension. The file holds what must be
// known before sign-in (identity and addresses); models and the agent come
// from the school's key server after it. Checked once, at build time.
import { colour, failer, https, text } from "./fields.ts";
import { parseOffer } from "./keys.ts";

// status: the platform's own status bar, a command printing its items
// (src/core/platformStatus.ts). Optional.
export type Connection = { keyFile: string; offer: Record<string, unknown>; status?: { command: string; args: string[] } };
import type { Lang } from "./i18n.ts";

export type School = {
  id: string;
  name: string;
  accent: string;
  // The school's sign-in page and key server (BulkHours' Moodle): absent
  // for a variant on its platform's own connection.
  signInUrl?: string;
  keyUrl?: string;
  // What this student spent of their budget, for the panel's meter.
  creditsUrl?: string;
  // The platform's own connection (MaQI, owner 2026-11-12): the person's key
  // in a file the platform writes and renews (${user} = the account), and
  // what goes with it (models, agent), as a key server would send them.
  connection?: Connection;
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
  // The variant's own folder for conversations and agent files, e.g. ~/.maqi
  // (owner, 2026-11-12). Optional: XDG's ~/.local/state/gateka otherwise.
  stateDir?: string;
  // The platform's own pages (portal, docs, forge, chat...), one button away
  // in the panel header, as JupyterLab's MaQI menu (owner, 2026-11-12).
  links: Link[];
  // The person's picture, as the platform shows it (${user} = the account):
  // drawn in the panel, beside the links. Optional.
  avatar?: string;
};

export type Link = { label: string; url: string; icon?: string };

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
    // On its platform's own connection a variant has no sign-in addresses.
    ...(o.connection !== undefined ? { connection: connection(o.connection, fail) } : {
      signInUrl: https(o, "signInUrl", fail),
      keyUrl: https(o, "keyUrl", fail),
      creditsUrl: https(o, "creditsUrl", fail),
    }),
    ...(o.downloadUrl !== undefined ? { downloadUrl: https(o, "downloadUrl", fail) } : {}),
    language: language(o.language, fail),
    title: o.title === undefined ? `BulkHours ${text(o, "name", fail)}` : text(o, "title", fail),
    prefix: prefix(o.prefix, fail),
    ...(o.tile !== undefined ? { tile: colour(o, "tile", fail) } : {}),
    ...(o.stateDir !== undefined ? { stateDir: stateDir(o.stateDir, fail) } : {}),
    links: links(o.links, fail),
    ...(o.avatar !== undefined ? { avatar: https(o, "avatar", fail) } : {}),
  };
}

// The extension's name, and its builds' file names: bulkhours-ipsa, maqi.
export function packageName(s: Pick<School, "id" | "prefix">): string {
  return s.prefix === s.id ? s.id : `${s.prefix}-${s.id}`;
}

function connection(v: unknown, fail: (m: string) => never): Connection {
  const o = (v ?? {}) as Record<string, unknown>;
  const keyFile = typeof o.keyFile === "string" && o.keyFile.startsWith("/") ? o.keyFile : fail(`"keyFile" must be an absolute path`);
  const offer = (o.offer ?? {}) as Record<string, unknown>;
  try { parseOffer(offer, fail); } catch (e) { fail((e as Error).message.replace(/^school \S+: /, "")); }
  return { keyFile, offer, ...(o.status !== undefined ? { status: statusCommand(o.status, fail) } : {}) };
}

function statusCommand(v: unknown, fail: (m: string) => never): { command: string; args: string[] } {
  const o = (v ?? {}) as Record<string, unknown>;
  const command = typeof o.command === "string" && o.command.startsWith("/") ? o.command : fail(`"status.command" must be an absolute path`);
  const args = o.args ?? [];
  return Array.isArray(args) && args.every((a) => typeof a === "string") ? { command, args: args as string[] }
    : fail(`"status.args" must be a list of strings`);
}

function links(v: unknown, fail: (m: string) => never): Link[] {
  if (v === undefined) return [];
  const ok = (l: Record<string, unknown>) => typeof l?.label === "string" && l.label.trim() !== ""
    && typeof l.url === "string" && l.url.startsWith("https://") && (l.icon === undefined || (typeof l.icon === "string" && /^[a-z-]+$/.test(l.icon)));
  if (!Array.isArray(v) || !v.every(ok)) fail(`"links" must be {label, https url, icon?} items`);
  return (v as Link[]).map((l) => ({ label: l.label, url: l.url, ...(l.icon ? { icon: l.icon } : {}) }));
}

function stateDir(v: unknown, fail: (m: string) => never): string {
  return typeof v === "string" && /^(~\/|\/)\S*$/.test(v) ? v : fail(`"stateDir" must start with ~/ or /`);
}

function prefix(v: unknown, fail: (m: string) => never): string {
  if (v === undefined) return "bulkhours";
  return typeof v === "string" && /^[a-z][a-z0-9]{1,30}$/.test(v) ? v : fail(`"prefix" must be lowercase letters and digits`);
}

function language(v: unknown, fail: (m: string) => never): Lang {
  if (v === undefined) return "en";
  return v === "fr" || v === "en" ? v : fail(`"language" must be fr or en`);
}
