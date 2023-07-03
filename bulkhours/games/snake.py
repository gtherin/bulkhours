import pygame
import random

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
VERT = (0, 255, 0)
ROUGE = (255, 0, 0)

# Définition de la taille de la fenêtre
largeur_fenetre = 800
hauteur_fenetre = 600
taille_bloc = 20

# Création de la fenêtre
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Snake")

# Horloge pour contrôler la vitesse du jeu
horloge = pygame.time.Clock()


# Fonction pour afficher le score
def afficher_score(score):
    police = pygame.font.Font(None, 36)
    texte = police.render("Score: " + str(score), True, NOIR)
    fenetre.blit(texte, [10, 10])


# Fonction pour afficher le serpent
def afficher_serpent(serpent):
    for bloc in serpent:
        pygame.draw.rect(fenetre, VERT, [bloc[0], bloc[1], taille_bloc, taille_bloc])


# Fonction principale du jeu
def jeu_snake():
    jeu_termine = False
    jeu_gagne = False

    # Position initiale du serpent
    serpent = [[largeur_fenetre // 2, hauteur_fenetre // 2]]

    # Direction initiale du serpent
    direction = "DROITE"

    # Position initiale de la pomme
    pomme_x = round(random.randrange(0, largeur_fenetre - taille_bloc) / 20.0) * 20.0
    pomme_y = round(random.randrange(0, hauteur_fenetre - taille_bloc) / 20.0) * 20.0

    # Boucle principale du jeu
    while not jeu_termine:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jeu_termine = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "GAUCHE"
                elif event.key == pygame.K_RIGHT:
                    direction = "DROITE"
                elif event.key == pygame.K_UP:
                    direction = "HAUT"
                elif event.key == pygame.K_DOWN:
                    direction = "BAS"

        # Mise à jour de la position du serpent
        if direction == "GAUCHE":
            serpent[0][0] -= taille_bloc
        elif direction == "DROITE":
            serpent[0][0] += taille_bloc
        elif direction == "HAUT":
            serpent[0][1] -= taille_bloc
        elif direction == "BAS":
            serpent[0][1] += taille_bloc

        # Vérification des collisions avec les bords de la fenêtre
        if (
            serpent[0][0] < 0
            or serpent[0][0] >= largeur_fenetre
            or serpent[0][1] < 0
            or serpent[0][1] >= hauteur_fenetre
        ):
            jeu_termine = True

        # Vérification des collisions avec le corps du serpent
        for bloc in serpent[1:]:
            if serpent[0][0] == bloc[0] and serpent[0][1] == bloc[1]:
                jeu_termine = True

        # Vérification de la collision avec la pomme
        if serpent[0][0] == pomme_x and serpent[0][1] == pomme_y:
            serpent.append([])
            pomme_x = round(random.randrange(0, largeur_fenetre - taille_bloc) / 20.0) * 20.0
            pomme_y = round(random.randrange(0, hauteur_fenetre - taille_bloc) / 20.0) * 20.0

        # Effacement de l'écran
        fenetre.fill(BLANC)

        # Affichage de la pomme
        pygame.draw.rect(fenetre, ROUGE, [pomme_x, pomme_y, taille_bloc, taille_bloc])

        # Affichage du serpent
        afficher_serpent(serpent)

        # Mise à jour de l'écran
        pygame.display.flip()

        # Contrôle de la vitesse du jeu
        horloge.tick(10)

    # Fermeture de Pygame
    pygame.quit()


# Lancement du jeu
if __name__ == "__main__":
    jeu_snake()
