import pygame
from .ui import dessiner_bouton
from .utils import WHITE, BLACK, WINDOW_WIDTH, WINDOW_HEIGHT, charger_image


def gerer_accueil(ecran, police, police_bouton, pos_souris, clic_souris, evenements):
    # Chargement paresseux de l'image de fond
    if not hasattr(gerer_accueil, "bg_img"):
        gerer_accueil.bg_img = charger_image(
            "banana_Sam.png", size=(WINDOW_WIDTH, WINDOW_HEIGHT)
        )
    bg_img = gerer_accueil.bg_img
    if bg_img is not None:
        ecran.blit(bg_img, (0, 0))
    else:
        ecran.fill(WHITE)
    # Création du bouton
    largeur_bouton, hauteur_bouton = 350, 80
    rect_bouton = pygame.Rect(
        (WINDOW_WIDTH - largeur_bouton) // 2,
        (WINDOW_HEIGHT) // 2,
        largeur_bouton,
        hauteur_bouton,
    )
    # Afficher le titre
    surf_titre = police.render("Pierre Papier Ciseaux", True, BLACK)
    rect_titre = surf_titre.get_rect(
        center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 120)
    )
    ecran.blit(surf_titre, rect_titre)
    # Afficher le bouton
    dessiner_bouton(
        ecran,
        rect_bouton,
        "Commencer la partie",
        police_bouton,
        pos_souris,
        clic_souris,
    )
    # Gestion du clic
    for evenement in evenements:
        if evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
            if rect_bouton.collidepoint(pos_souris):
                return "partie"
    return "accueil"
