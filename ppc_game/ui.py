import pygame
from .utils import BLACK, BLUE, DARK_BLUE, WHITE


def dessiner_bouton(ecran, rect_bouton, texte, police_bouton, pos_souris, clic_souris):
    couleur = (
        DARK_BLUE if rect_bouton.collidepoint(pos_souris) and clic_souris else BLUE
    )
    pygame.draw.rect(ecran, couleur, rect_bouton)
    pygame.draw.rect(ecran, BLACK, rect_bouton, 2)
    surf_texte = police_bouton.render(texte, True, WHITE)
    rect_texte = surf_texte.get_rect(center=rect_bouton.center)
    ecran.blit(surf_texte, rect_texte)


def dessiner_choix(ecran, rects, items, police, pos_souris, clic_souris):
    BANANA_YELLOW = (255, 235, 59)
    for i, rect in enumerate(rects):
        center = rect.center
        rayon = rect.width // 2
        survole = rect.collidepoint(pos_souris)
        couleur = BANANA_YELLOW
        # Effet de survol/clic : bordure plus foncée
        bordure = 6 if survole and clic_souris else 3
        pygame.draw.circle(ecran, couleur, center, rayon)
        pygame.draw.circle(ecran, (200, 180, 30), center, rayon, bordure)
        # Affichage de l'image ou du texte centré dans le cercle
        if hasattr(items[i], "blit"):
            img = items[i]
            if img is not None:
                img_rect = img.get_rect(center=center)
                ecran.blit(img, img_rect)
        else:
            surf_texte = police.render(str(items[i]), True, (60, 60, 60))
            rect_texte = surf_texte.get_rect(center=center)
            ecran.blit(surf_texte, rect_texte)
