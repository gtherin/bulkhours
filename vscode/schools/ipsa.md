# BulkHours IPSA

L'assistant de code des étudiants de l'IPSA, dans VS Code : posez une question
sur votre projet, l'assistant lit vos fichiers, les compile s'il le faut, et
**demande votre accord avant toute modification**. Les modèles (DeepSeek et
d'autres) sont payés sur les crédits de l'école : vous n'avez aucune clé à
acheter ni à saisir.

## Installer

Pour le cours HPC, l'assistant travaille sur la machine GPU, là où se trouvent
votre code, `nvcc` et la carte graphique.

1. Faites une fois la commande d'installation reçue pour le cours : elle
   crée l'hôte `hpc` dans votre configuration SSH.
2. Dans VS Code, installez l'extension **Remote - SSH**, puis
   `F1` → **Remote-SSH: Connect to Host…** → `hpc`.
3. Dans le terminal de cette fenêtre, installez l'extension :

   ```bash
   curl -LO https://bulkhours.fr/bkfpage/vscode/bulkhours-ipsa-0.1.0.vsix
   code --install-extension bulkhours-ipsa-0.1.0.vsix
   ```

4. Ouvrez le dossier du cours, puis le panneau **BulkHours IPSA** dans la
   barre de gauche, et cliquez sur **Se connecter** avec votre compte
   BulkHours.

## Utiliser

- Écrivez votre question et appuyez sur Entrée ; le fichier ouvert dans
  l'éditeur est joint à la question.
- Avant d'écrire dans un fichier, l'assistant vous montre ce qu'il veut faire :
  **Autoriser** ou **Refuser**. Une modification d'un fichier ouvert s'annule
  avec `Ctrl+Z`.
- **Arrêter** interrompt l'assistant ; **Nouvelle conversation** repart de zéro.
- Le menu en bas du panneau choisit le modèle : `fast` pour les questions
  courantes, les autres pour les tâches plus longues.

## Vos crédits et vos données

- Chaque étudiant a un budget sur la période ; quand il est épuisé, le panneau
  l'indique.
- Les modèles sont appelés uniquement par le serveur de l'école, avec une clé
  personnelle qui expire au bout de quelques heures et se renouvelle seule.
- Rien n'est envoyé aux services propres de DeepSeek, et aucune télémétrie
  n'est collectée par l'assistant.
- Ne mettez jamais de mot de passe ou de clé dans vos fichiers : l'assistant
  peut les lire.
