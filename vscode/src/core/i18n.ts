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
  sessionExpired: "your {brand} session expired: sign in again",
  noCredits: "no credits left for this period",
  keyServerAnswered: "the key server answered {status}",
  noToken: "the sign-in page sent no token",
  ignoredLink: "{brand}: ignored a sign-in link this window did not ask for.",
  openFolder: "open a folder first: the assistant works inside your project",
  keyRenewed: "your key was renewed: the agent restarted",
  agentPaused: "the agent was paused to free memory: it comes back, with the conversation, at your next message",
  stoppedBeforeStart: "stopped before the agent began",
  stopped: "stopped: {reason}",
  error: "error: {message}",
  reason_cancelled: "cancelled",
  reason_max_tokens: "the answer reached its length limit: if the conversation is long, Clear starts a fresh one",
  reason_max_turn_requests: "the agent reached its step limit",
  reason_refusal: "the agent declined",
  pickAgentNone: "Sign in first, or add agents in bulkhours.extraAgents.",
  pickAgentPlaceholder: "Agent for new chats",
  schoolAgent: "your school's agent",
  startingAgent: "Starting the agent… the first time on a machine can take a few minutes.",
  noImages: "this agent does not read images: they were not sent",
  compact: "Compact",
  compactHint: "Summarise this conversation and continue from the summary",
  clear: "Clear",
  clearHint: "Start a new conversation",
  thinkingVerb: "is thinking",
  budgetTitle: "Your assistant budget for this course",
  contextTitle: "What the agent keeps in mind: it compacts by itself at 75 %",
  removeImage: "Remove this image",
  suggestExplain: "Explain the file that is open",
  suggestBuild: "Why does my code not compile?",
  suggestFaster: "How can I make this kernel faster?",
  schoolModels: "School credits · $ per million tokens, in / out",
  yourAgents: "Your agents",
  mic: "Dictate",
  micWindows: "Dictation: press Win + H, then speak",
  micMac: "Dictation: press Fn twice, then speak",
  seesImages: "images",
  compactStops: "Compact stops the turn in progress. Stop it and compact?",
  stopAndCompact: "Stop and compact",
  clearStops: "Clear stops the turn in progress and starts a new conversation. Stop it?",
  stopAndClear: "Stop and clear",
  closeStops: "Closing this tab stops the turn in progress. Stop it and close?",
  stopAndClose: "Stop and close",
  tooManyRunning: "{n} conversations are already working: wait for one to finish, or stop it.",
  newTab: "New chat",
  closeTab: "Close",
  renameHint: "Double-click to rename",
  renameTab: "Rename",
  runPending: "Start",
  pendingHint: "This conversation was prepared with its first request, which has not been run yet.",
  rendersTitle: "Pages",
  pasteCode: "Paste a code instead",
  codePrompt: "Paste the code shown on the sign-in page that just opened in your browser",
  codeInvalid: "This is not a sign-in code for this extension: copy the whole code from the sign-in page.",
  recentTitle: "Your conversations in this folder",
  questionsCount: "{n} questions",
  renderNotMarimo: "Not a marimo notebook: only a .py with `import marimo` and `marimo.App(` has a rendered page.",
  renderUnreadable: "Cannot read the file: {message}",
  renderFailed: "The page could not be rendered (marimo export html):\n\n{message}\n\nSet the marimo to use in the setting « marimo » of this extension.",
  linksTitle: "Your platform's pages",
  linksPlaceholder: "Open a page of the platform",
  openInEditor: "Open in the editor",
  dashboardPort: "Port of the dashboard running on this machine (Streamlit: 8501, marimo: 2718)",
  dashboardPortInvalid: "A port number between 1024 and 65535",
  platformOnly: "{brand} works on its own servers: open this folder on one of them (Remote-SSH), where the platform gives you your key.",
  noKeyFile: "No {brand} key on this machine ({path}): open {brand} on one of its servers, where the platform gives you your key.",
  compacted: "conversation compacted: the next message starts a fresh agent session with the conversation condensed",
  lastActivity: "last sign {ago} ago",
  thisTurn: "{cost} this turn",
  historyEmpty: "No earlier conversation in this project yet.",
  historyPlaceholder: "Reopen a conversation",
  historyDetail: "{date} · {n} question(s)",
  renamePrompt: "Name of this conversation",
  updateAvailable: "{brand} {version} is available.",
  updateNow: "Update",
  updated: "{brand} {version} is installed: reload the window to use it.",
  reloadNow: "Reload",
  upToDate: "{brand} is up to date ({version}).",
  updateFailed: "The update failed: {message}",
  updateUnavailable: "This build has no download area to update from.",
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
  sessionExpired: "votre session {brand} a expiré : reconnectez-vous",
  noCredits: "plus de crédits pour cette période",
  keyServerAnswered: "le serveur de clés a répondu {status}",
  noToken: "la page de connexion n'a pas envoyé de jeton",
  ignoredLink: "{brand} : lien de connexion ignoré, cette fenêtre ne l'avait pas demandé.",
  openFolder: "ouvrez d'abord un dossier : l'assistant travaille dans votre projet",
  keyRenewed: "votre clé a été renouvelée : l'agent a redémarré",
  agentPaused: "l'agent a été mis en pause pour libérer la mémoire : il revient, avec la conversation, à votre prochain message",
  stoppedBeforeStart: "arrêté avant que l'agent ne commence",
  stopped: "arrêté : {reason}",
  error: "erreur : {message}",
  reason_cancelled: "annulé",
  reason_max_tokens: "la réponse a atteint sa longueur maximale : si la conversation est longue, Effacer en démarre une neuve",
  reason_max_turn_requests: "l'agent a atteint son nombre maximal d'étapes",
  reason_refusal: "l'agent a refusé",
  pickAgentNone: "Connectez-vous d'abord, ou ajoutez des agents dans bulkhours.extraAgents.",
  pickAgentPlaceholder: "Agent des nouvelles conversations",
  schoolAgent: "l'agent de votre école",
  startingAgent: "Démarrage de l'agent… la première fois sur une machine peut prendre quelques minutes.",
  noImages: "cet agent ne lit pas les images : elles n'ont pas été envoyées",
  compact: "Compacter",
  compactHint: "Résumer la conversation et repartir du résumé",
  clear: "Effacer",
  clearHint: "Commencer une nouvelle conversation",
  thinkingVerb: "réfléchit",
  budgetTitle: "Votre budget d'assistant pour ce cours",
  contextTitle: "Ce que l'agent garde en tête : il compacte tout seul à 75 %",
  removeImage: "Retirer cette image",
  suggestExplain: "Explique le fichier ouvert",
  suggestBuild: "Pourquoi mon code ne compile pas ?",
  suggestFaster: "Comment accélérer ce kernel ?",
  schoolModels: "Crédits de l'école · $ par million de tokens, entrée / sortie",
  yourAgents: "Vos agents",
  mic: "Dicter",
  micWindows: "Dictée : appuyez sur Win + H, puis parlez",
  micMac: "Dictée : appuyez deux fois sur Fn, puis parlez",
  seesImages: "lit les images",
  compactStops: "Compacter arrête le tour en cours. L'arrêter et compacter ?",
  stopAndCompact: "Arrêter et compacter",
  clearStops: "Effacer arrête le tour en cours et démarre une nouvelle conversation. L'arrêter ?",
  stopAndClear: "Arrêter et effacer",
  closeStops: "Fermer cet onglet arrête le tour en cours. L'arrêter et fermer ?",
  stopAndClose: "Arrêter et fermer",
  tooManyRunning: "{n} conversations travaillent déjà : attendez qu'une finisse, ou arrêtez-la.",
  newTab: "Nouvelle",
  closeTab: "Fermer",
  renameHint: "Double-clic pour renommer",
  renameTab: "Renommer",
  runPending: "Démarrer",
  pendingHint: "Cette conversation a été préparée avec sa première demande, qui n'a pas encore été lancée.",
  rendersTitle: "Pages rendues",
  pasteCode: "Coller un code à la place",
  codePrompt: "Collez le code affiché sur la page de connexion qui vient de s'ouvrir dans votre navigateur",
  codeInvalid: "Ce n'est pas un code de connexion pour cette extension : copiez le code entier depuis la page de connexion.",
  recentTitle: "Vos conversations dans ce dossier",
  questionsCount: "{n} questions posées",
  renderNotMarimo: "Ce n'est pas un notebook marimo : seul un .py avec `import marimo` et `marimo.App(` a une page rendue.",
  renderUnreadable: "Impossible de lire le fichier : {message}",
  renderFailed: "La page n'a pas pu être rendue (marimo export html) :\n\n{message}\n\nIndiquez le marimo à utiliser dans le réglage « marimo » de cette extension.",
  linksTitle: "Les pages de votre plateforme",
  linksPlaceholder: "Ouvrir une page de la plateforme",
  openInEditor: "Ouvrir dans l'éditeur",
  dashboardPort: "Port du tableau de bord lancé sur cette machine (Streamlit : 8501, marimo : 2718)",
  dashboardPortInvalid: "Un numéro de port entre 1024 et 65535",
  platformOnly: "{brand} fonctionne sur ses propres serveurs : ouvrez ce dossier sur l'un d'eux (Remote-SSH), où la plateforme vous donne votre clé.",
  noKeyFile: "Pas de clé {brand} sur cette machine ({path}) : ouvrez {brand} sur l'un de ses serveurs, où la plateforme vous donne votre clé.",
  compacted: "conversation compactée : le prochain message démarre une session neuve de l'agent, avec la conversation résumée",
  lastActivity: "dernier signe il y a {ago}",
  thisTurn: "{cost} pour ce tour",
  historyEmpty: "Pas encore d'autre conversation dans ce projet.",
  historyPlaceholder: "Rouvrir une conversation",
  historyDetail: "{date} · {n} question(s) posée(s)",
  renamePrompt: "Nom de cette conversation",
  updateAvailable: "{brand} {version} est disponible.",
  updateNow: "Mettre à jour",
  updated: "{brand} {version} est installé : rechargez la fenêtre pour l'utiliser.",
  reloadNow: "Recharger",
  upToDate: "{brand} est à jour ({version}).",
  updateFailed: "La mise à jour a échoué : {message}",
  updateUnavailable: "Cette version n'a pas d'espace de téléchargement pour se mettre à jour.",
};

export const MESSAGES: Record<Lang, typeof en> = { en, fr };
export type MessageKey = keyof typeof en;

export function pickLang(display: string, fallback: Lang): Lang {
  const base = display.toLowerCase().split("-")[0];
  return base === "fr" || base === "en" ? base : fallback;
}

// The variant's name in its messages (school.title), set once at activation.
let brand = "BulkHours";
export function setBrand(title: string): void { brand = title; }

export function t(lang: Lang, key: MessageKey, vars: Record<string, string | number> = {}): string {
  return MESSAGES[lang][key].replace(/\{(\w+)\}/g, (_, name: string) => {
    if (name === "brand" && !(name in vars)) return brand;
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
