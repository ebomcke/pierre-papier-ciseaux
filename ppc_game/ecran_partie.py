import pygame
from .ui import dessiner_choix
from .utils import WHITE, WINDOW_WIDTH, WINDOW_HEIGHT, charger_image


def gerer_partie(
    ecran, police_bouton, pos_souris, clic_souris, evenements, choix_joueur
):
    # Chargement paresseux du rouage (statique)
    if not hasattr(gerer_partie, "gear_img"):
        gear_size = 64
        gerer_partie.gear_img = charger_image("rouage.png", size=(gear_size, gear_size))
    gear_img = gerer_partie.gear_img

    # Définir les choix pour la partie
    choix_textes = ["pierre", "papier", "ciseaux"]
    nb_choix = len(choix_textes)
    largeur_choix, hauteur_choix = 200, 100
    espacement = 60
    total_largeur = nb_choix * largeur_choix + (nb_choix - 1) * espacement
    x_depart = (WINDOW_WIDTH - total_largeur) // 2
    y_choix = WINDOW_HEIGHT - hauteur_choix - 40
    rects_choix = [
        pygame.Rect(
            x_depart + i * (largeur_choix + espacement),
            y_choix,
            largeur_choix,
            hauteur_choix,
        )
        for i in range(nb_choix)
    ]
    # Gestion du clic sur un choix
    for evenement in evenements:
        if evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
            for i, rect in enumerate(rects_choix):
                if rect.collidepoint(pos_souris):
                    print(choix_textes[i])
                    choix_joueur = choix_textes[i]
    # Affichage
    ecran.fill(WHITE)
    if choix_joueur is None and gear_img is not None:
        gear_center_x = WINDOW_WIDTH // 2
        gear_center_y = WINDOW_HEIGHT // 2
        angle = (pygame.time.get_ticks() // 5) % 360
        gear_rotated = pygame.transform.rotate(gear_img, angle)
        gear_rect = gear_rotated.get_rect(center=(gear_center_x, gear_center_y))
        ecran.blit(gear_rotated, gear_rect)
    if choix_joueur is not None:
        texte_choix_joueur = f"Votre choix : {choix_joueur}"
        surf_choix_joueur = police_bouton.render(texte_choix_joueur, True, (0, 0, 0))
        rect_choix_joueur = surf_choix_joueur.get_rect(
            center=(WINDOW_WIDTH // 2, rects_choix[0].top - 20)
        )
        ecran.blit(surf_choix_joueur, rect_choix_joueur)
    dessiner_choix(
        ecran, rects_choix, choix_textes, police_bouton, pos_souris, clic_souris
    )
    return "partie", choix_joueur
