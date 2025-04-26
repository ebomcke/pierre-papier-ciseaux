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


def dessiner_choix(ecran, rects, textes, police, pos_souris, clic_souris):
    for i, rect in enumerate(rects):
        couleur = DARK_BLUE if rect.collidepoint(pos_souris) and clic_souris else BLUE
        pygame.draw.rect(ecran, couleur, rect)
        pygame.draw.rect(ecran, BLACK, rect, 2)
        surf_texte = police.render(textes[i], True, WHITE)
        rect_texte = surf_texte.get_rect(center=rect.center)
        ecran.blit(surf_texte, rect_texte)
