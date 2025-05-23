import pygame
import sys
from .utils import WINDOW_WIDTH, WINDOW_HEIGHT
from .ecran_accueil import gerer_accueil
from .ecran_partie import gerer_partie


# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
DARK_BLUE = (40, 90, 140)


def main():
    pygame.init()

    ecran = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pierre Papier Ciseaux")

    horloge = pygame.time.Clock()
    police = pygame.font.SysFont(None, 60)
    police_bouton = pygame.font.SysFont(None, 48)

    etat_jeu = "accueil"
    etat_partie = {
        "choix_joueur": None,
        "choix_ordi": None,
        "resultat": None,
        "manche_terminee": False,
    }

    while True:
        pos_souris = pygame.mouse.get_pos()
        clic_souris = False
        evenements = pygame.event.get()
        for evenement in evenements:
            if evenement.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if etat_jeu == "accueil":
            nouvel_etat = gerer_accueil(
                ecran,
                police,
                police_bouton,
                pos_souris,
                pygame.mouse.get_pressed()[0],
                evenements,
            )
            etat_jeu = nouvel_etat
            if etat_jeu == "partie":
                etat_partie = {
                    "choix_joueur": None,
                    "choix_ordi": None,
                    "resultat": None,
                    "manche_terminee": False,
                }
        elif etat_jeu == "partie":
            nouvel_etat, etat_partie = gerer_partie(
                ecran,
                police_bouton,
                pos_souris,
                pygame.mouse.get_pressed()[0],
                evenements,
                etat_partie,
            )
            etat_jeu = nouvel_etat

        pygame.display.flip()
        horloge.tick(60)


if __name__ == "__main__":
    main()
