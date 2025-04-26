import pygame
import sys

# Constantes pour la taille de la fenêtre
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
DARK_BLUE = (40, 90, 140)


def dessiner_bouton(ecran, rect_bouton, texte, police_bouton, pos_souris, clic_souris):
    couleur = DARK_BLUE if rect_bouton.collidepoint(pos_souris) and clic_souris else BLUE
    pygame.draw.rect(ecran, couleur, rect_bouton)
    pygame.draw.rect(ecran, BLACK, rect_bouton, 2)
    surf_texte = police_bouton.render(texte, True, WHITE)
    rect_texte = surf_texte.get_rect(center=rect_bouton.center)
    ecran.blit(surf_texte, rect_texte)


def main():
    pygame.init()

    ecran = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Pierre Papier Ciseaux')

    horloge = pygame.time.Clock()
    police = pygame.font.SysFont(None, 60)
    police_bouton = pygame.font.SysFont(None, 48)

    # États du jeu : 'menu' ou 'partie'
    etat_jeu = 'menu'

    # Définir le bouton
    largeur_bouton, hauteur_bouton = 350, 80
    rect_bouton = pygame.Rect(
        (WINDOW_WIDTH - largeur_bouton) // 2,
        (WINDOW_HEIGHT) // 2,
        largeur_bouton,
        hauteur_bouton
    )

    en_cours = True
    while en_cours:
        pos_souris = pygame.mouse.get_pos()
        clic_souris = False
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                en_cours = False
            if evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
                clic_souris = True
                if etat_jeu == 'menu' and rect_bouton.collidepoint(pos_souris):
                    etat_jeu = 'partie'

        ecran.fill(WHITE)

        if etat_jeu == 'menu':
            # Afficher le titre
            surf_titre = police.render('Pierre Papier Ciseaux', True, BLACK)
            rect_titre = surf_titre.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 120))
            ecran.blit(surf_titre, rect_titre)
            # Afficher le bouton
            dessiner_bouton(ecran, rect_bouton, 'Commencer la partie', police_bouton, pos_souris, pygame.mouse.get_pressed()[0])
        elif etat_jeu == 'partie':
            # Afficher l'écran de jeu (pour l'instant, juste un fond blanc)
            pass

        pygame.display.flip()
        horloge.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 