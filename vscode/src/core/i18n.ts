// What the extension says, in the student's language: VS Code's display
// language when we speak it, the school's otherwise. One table per language;
// a test keeps the tables in step (same keys, same placeholders).

export type Lang = "fr" | "en";

const en = {
  signInPrompt: "Sign in with your {school} account to use the assistant on your school's credits.",
  signIn: "Sign in",
  emptyChat: "Ask a question about your code. The assistant can read your files; it asks before changing them.",
  placeholder: "Ask about your code…",
  send: "Send",
  stop: "Stop",
  model: "Model",
  thinking: "thinking",
  output: "output",
  noChange: "(no change)",
  agentWantsToAct: "The agent wants to act",
  notSignedIn: "not signed in",
  sessionExpired: "your BulkHours session expired: sign in again",
  noCredits: "no credits left for this period",
  keyServerAnswered: "the key server answered {status}",
  noToken: "the sign-in page sent no token",
  ignoredLink: "BulkHours: ignored a sign-in link this window did not ask for.",
  openFolder: "open a folder first: the assistant works inside your project",
  keyRenewed: "your key was renewed: the agent restarted",
  stoppedBeforeStart: "stopped before the agent began",
  stopped: "stopped: {reason}",
  error: "error: {message}",
  reason_cancelled: "cancelled",
  reason_max_tokens: "the answer reached its length limit",
  reason_max_turn_requests: "the agent reached its step limit",
  reason_refusal: "the agent declined",
  pickAgentNone: "Sign in first, or add agents in bulkhours.extraAgents.",
  pickAgentPlaceholder: "Agent for new chats",
  schoolAgent: "your school's agent",
};

const fr: typeof en = {
  signInPrompt: "Connectez-vous avec votre compte {school} pour utiliser l'assistant sur les crédits de votre école.",
  signIn: "Se connecter",
  emptyChat: "Posez une question sur votre code. L'assistant peut lire vos fichiers ; il demande avant de les modifier.",
  placeholder: "Une question sur votre code…",
  send: "Envoyer",
  stop: "Arrêter",
  model: "Modèle",
  thinking: "réflexion",
  output: "sortie",
  noChange: "(aucun changement)",
  agentWantsToAct: "L'agent veut agir",
  notSignedIn: "non connecté",
  sessionExpired: "votre session BulkHours a expiré : reconnectez-vous",
  noCredits: "plus de crédits pour cette période",
  keyServerAnswered: "le serveur de clés a répondu {status}",
  noToken: "la page de connexion n'a pas envoyé de jeton",
  ignoredLink: "BulkHours : lien de connexion ignoré, cette fenêtre ne l'avait pas demandé.",
  openFolder: "ouvrez d'abord un dossier : l'assistant travaille dans votre projet",
  keyRenewed: "votre clé a été renouvelée : l'agent a redémarré",
  stoppedBeforeStart: "arrêté avant que l'agent ne commence",
  stopped: "arrêté : {reason}",
  error: "erreur : {message}",
  reason_cancelled: "annulé",
  reason_max_tokens: "la réponse a atteint sa longueur maximale",
  reason_max_turn_requests: "l'agent a atteint son nombre maximal d'étapes",
  reason_refusal: "l'agent a refusé",
  pickAgentNone: "Connectez-vous d'abord, ou ajoutez des agents dans bulkhours.extraAgents.",
  pickAgentPlaceholder: "Agent des nouvelles conversations",
  schoolAgent: "l'agent de votre école",
};

export const MESSAGES: Record<Lang, typeof en> = { en, fr };
export type MessageKey = keyof typeof en;

export function pickLang(display: string, fallback: Lang): Lang {
  const base = display.toLowerCase().split("-")[0];
  return base === "fr" || base === "en" ? base : fallback;
}

export function t(lang: Lang, key: MessageKey, vars: Record<string, string | number> = {}): string {
  return MESSAGES[lang][key].replace(/\{(\w+)\}/g, (_, name: string) => {
    if (!(name in vars)) throw new Error(`missing value "${name}" for message ${key}`);
    return String(vars[name]);
  });
}

// A thrown error that carries a message key, translated where it is shown.
export class Said extends Error {
  readonly key: MessageKey;
  readonly vars: Record<string, string | number>;
  constructor(key: MessageKey, vars: Record<string, string | number> = {}) {
    super(t("en", key, vars));
    this.key = key;
    this.vars = vars;
  }
}

export function sayError(lang: Lang, e: unknown): string {
  return e instanceof Said ? t(lang, e.key, e.vars) : String((e as Error)?.message ?? e);
}
