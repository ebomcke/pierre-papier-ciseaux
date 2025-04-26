import pygame
import random
from .ui import dessiner_choix
from .utils import WHITE, WINDOW_WIDTH, WINDOW_HEIGHT, charger_image


def gerer_partie(
    ecran, police_bouton, pos_souris, clic_souris, evenements, etat_partie
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
    if not etat_partie["manche_terminee"]:
        for evenement in evenements:
            if evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
                for i, rect in enumerate(rects_choix):
                    if (
                        rect.collidepoint(pos_souris)
                        and etat_partie["choix_joueur"] is None
                    ):
                        etat_partie["choix_joueur"] = choix_textes[i]
                        etat_partie["choix_ordi"] = random.choice(choix_textes)
                        # Déterminer le gagnant
                        cj = etat_partie["choix_joueur"]
                        co = etat_partie["choix_ordi"]
                        if cj == co:
                            etat_partie["resultat"] = "egalite"
                        elif (
                            (cj == "pierre" and co == "ciseaux")
                            or (cj == "papier" and co == "pierre")
                            or (cj == "ciseaux" and co == "papier")
                        ):
                            etat_partie["resultat"] = "joueur"
                            etat_partie["manche_terminee"] = True
                        else:
                            etat_partie["resultat"] = "ordi"
                            etat_partie["manche_terminee"] = True

    # Affichage
    ecran.fill(WHITE)

    # Affichage des choix en haut de l'écran
    if (
        etat_partie["choix_joueur"] is not None
        and etat_partie["choix_ordi"] is not None
    ):
        texte_joueur = f"Vous : {etat_partie['choix_joueur']}"
        texte_ordi = f"Ordinateur : {etat_partie['choix_ordi']}"
        surf_joueur = police_bouton.render(texte_joueur, True, (0, 0, 128))
        surf_ordi = police_bouton.render(texte_ordi, True, (128, 0, 0))
        rect_joueur = surf_joueur.get_rect(center=(WINDOW_WIDTH // 3, 60))
        rect_ordi = surf_ordi.get_rect(center=(2 * WINDOW_WIDTH // 3, 60))
        ecran.blit(surf_joueur, rect_joueur)
        ecran.blit(surf_ordi, rect_ordi)
    elif gear_img is not None:
        gear_center_x = WINDOW_WIDTH // 2
        gear_center_y = WINDOW_HEIGHT // 2
        angle = (pygame.time.get_ticks() // 5) % 360
        gear_rotated = pygame.transform.rotate(gear_img, angle)
        gear_rect = gear_rotated.get_rect(center=(gear_center_x, gear_center_y))
        ecran.blit(gear_rotated, gear_rect)

    # Affichage du résultat au centre
    if (
        etat_partie["choix_joueur"] is not None
        and etat_partie["choix_ordi"] is not None
    ):
        if etat_partie["resultat"] == "egalite":
            texte_resultat = "Égalité ! Rejouez."
            couleur = (100, 100, 100)
        elif etat_partie["resultat"] == "joueur":
            texte_resultat = "Gagnant : Joueur !"
            couleur = (0, 180, 0)
        elif etat_partie["resultat"] == "ordi":
            texte_resultat = "Gagnant : Ordinateur !"
            couleur = (180, 0, 0)
        else:
            texte_resultat = ""
            couleur = (0, 0, 0)
        if texte_resultat:
            surf_resultat = police_bouton.render(texte_resultat, True, couleur)
            rect_resultat = surf_resultat.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
            )
            ecran.blit(surf_resultat, rect_resultat)

    # Bouton Accueil si manche terminée
    bouton_accueil_rect = pygame.Rect(
        WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 80, 200, 60
    )
    if etat_partie["manche_terminee"]:
        pygame.draw.rect(ecran, (200, 200, 255), bouton_accueil_rect)
        surf_accueil = police_bouton.render("Accueil", True, (0, 0, 80))
        rect_accueil = surf_accueil.get_rect(center=bouton_accueil_rect.center)
        ecran.blit(surf_accueil, rect_accueil)
        for evenement in evenements:
            if evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
                if bouton_accueil_rect.collidepoint(pos_souris):
                    # Réinitialiser l'état pour la prochaine partie si besoin
                    return "accueil", etat_partie

    # Si égalité, réinitialiser pour rejouer
    if etat_partie["resultat"] == "egalite":
        # On attend un clic pour réinitialiser
        for evenement in evenements:
            if evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
                etat_partie["choix_joueur"] = None
                etat_partie["choix_ordi"] = None
                etat_partie["resultat"] = None
                etat_partie["manche_terminee"] = False

    dessiner_choix(
        ecran, rects_choix, choix_textes, police_bouton, pos_souris, clic_souris
    )
    return "partie", etat_partie
