import pygame
import random
from .ui import dessiner_choix
from .utils import WHITE, WINDOW_WIDTH, WINDOW_HEIGHT, charger_image


def afficher_score(ecran, police_bouton, etat_partie):
    score_j = etat_partie.get("score_joueur", 0)
    score_o = etat_partie.get("score_ordi", 0)
    texte_score = f"Score — Vous : {score_j}  Ordi : {score_o}"
    surf_score = police_bouton.render(texte_score, True, (60, 60, 60))
    rect_score = surf_score.get_rect(topleft=(20, 20))
    ecran.blit(surf_score, rect_score)


def afficher_attente_choix(
    ecran,
    police_bouton,
    pos_souris,
    clic_souris,
    evenements,
    etat_partie,
    rects_choix,
    choix_textes,
):
    # Affichage de base
    ecran.fill(WHITE)
    afficher_score(ecran, police_bouton, etat_partie)
    # Affichage du titre
    surf_titre = police_bouton.render("En attente de choix", True, (0, 0, 0))
    rect_titre = surf_titre.get_rect(center=(WINDOW_WIDTH // 2, 60))
    ecran.blit(surf_titre, rect_titre)
    # Affichage du rouage animé au centre
    if not hasattr(afficher_attente_choix, "gear_img"):
        gear_size = 64
        afficher_attente_choix.gear_img = charger_image(
            "rouage.png", size=(gear_size, gear_size)
        )
    gear_img = afficher_attente_choix.gear_img
    if gear_img is not None:
        gear_center_x = WINDOW_WIDTH // 2
        gear_center_y = WINDOW_HEIGHT // 2
        angle = (pygame.time.get_ticks() // 5) % 360
        gear_rotated = pygame.transform.rotate(gear_img, angle)
        gear_rect = gear_rotated.get_rect(center=(gear_center_x, gear_center_y))
        ecran.blit(gear_rotated, gear_rect)
    # Affichage des boutons de choix avec images
    if not hasattr(gerer_partie, "choix_images"):
        gerer_partie.choix_images = [
            charger_image("pierre.png", size=(80, 80)),
            charger_image("papier.png", size=(80, 80)),
            charger_image("ciseaux.png", size=(80, 80)),
        ]
    choix_images = gerer_partie.choix_images
    dessiner_choix(
        ecran, rects_choix, choix_images, police_bouton, pos_souris, clic_souris
    )
    # Gestion du clic sur un choix
    for evenement in evenements:
        if evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
            for i, rect in enumerate(rects_choix):
                if rect.collidepoint(pos_souris):
                    etat_partie["choix_joueur"] = choix_textes[i]
                    etat_partie["choix_ordi"] = random.choice(choix_textes)
                    etat_partie["etat"] = "affichage_choix"
    return etat_partie


def afficher_affichage_choix(ecran, police_bouton, etat_partie):
    ecran.fill(WHITE)
    afficher_score(ecran, police_bouton, etat_partie)
    # Affichage des choix
    texte_joueur = f"Vous : {etat_partie['choix_joueur']}"
    texte_ordi = f"Ordinateur : {etat_partie['choix_ordi']}"
    surf_joueur = police_bouton.render(texte_joueur, True, (0, 0, 128))
    surf_ordi = police_bouton.render(texte_ordi, True, (128, 0, 0))
    rect_joueur = surf_joueur.get_rect(center=(WINDOW_WIDTH // 3, 60))
    rect_ordi = surf_ordi.get_rect(center=(2 * WINDOW_WIDTH // 3, 60))
    ecran.blit(surf_joueur, rect_joueur)
    ecran.blit(surf_ordi, rect_ordi)
    # Calcul du gagnant
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
    else:
        etat_partie["resultat"] = "ordi"
    etat_partie["etat"] = "resultat"
    return etat_partie


def afficher_resultat(
    ecran, police_bouton, pos_souris, clic_souris, evenements, etat_partie
):
    ecran.fill(WHITE)
    afficher_score(ecran, police_bouton, etat_partie)
    # Affichage des choix
    texte_joueur = f"Vous : {etat_partie['choix_joueur']}"
    texte_ordi = f"Ordinateur : {etat_partie['choix_ordi']}"
    surf_joueur = police_bouton.render(texte_joueur, True, (0, 0, 128))
    surf_ordi = police_bouton.render(texte_ordi, True, (128, 0, 0))
    rect_joueur = surf_joueur.get_rect(center=(WINDOW_WIDTH // 3, 60))
    rect_ordi = surf_ordi.get_rect(center=(2 * WINDOW_WIDTH // 3, 60))
    ecran.blit(surf_joueur, rect_joueur)
    ecran.blit(surf_ordi, rect_ordi)
    # Affichage du résultat
    if etat_partie["resultat"] == "egalite":
        texte_resultat = "Égalité !"
        couleur = (100, 100, 100)
    elif etat_partie["resultat"] == "joueur":
        texte_resultat = "Gagnant : Joueur !"
        couleur = (0, 180, 0)
        # Incrémenter le score du joueur si pas déjà fait
        if not etat_partie.get("score_incremente", False):
            etat_partie["score_joueur"] = etat_partie.get("score_joueur", 0) + 1
            etat_partie["score_incremente"] = True
    elif etat_partie["resultat"] == "ordi":
        texte_resultat = "Gagnant : Ordinateur !"
        couleur = (180, 0, 0)
        # Incrémenter le score de l'ordi si pas déjà fait
        if not etat_partie.get("score_incremente", False):
            etat_partie["score_ordi"] = etat_partie.get("score_ordi", 0) + 1
            etat_partie["score_incremente"] = True
    else:
        texte_resultat = ""
        couleur = (0, 0, 0)
    if texte_resultat:
        surf_resultat = police_bouton.render(texte_resultat, True, couleur)
        rect_resultat = surf_resultat.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        )
        ecran.blit(surf_resultat, rect_resultat)
    # Bouton Nouvelle manche
    bouton_nouvelle_rect = pygame.Rect(
        WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 + 80, 300, 60
    )
    pygame.draw.rect(ecran, (200, 255, 200), bouton_nouvelle_rect)
    surf_nouvelle = police_bouton.render("Nouvelle manche", True, (0, 80, 0))
    rect_nouvelle = surf_nouvelle.get_rect(center=bouton_nouvelle_rect.center)
    ecran.blit(surf_nouvelle, rect_nouvelle)
    for evenement in evenements:
        if evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
            if bouton_nouvelle_rect.collidepoint(pos_souris):
                # Réinitialiser l'état pour une nouvelle manche
                etat_partie["etat"] = "attente_choix"
                etat_partie["choix_joueur"] = None
                etat_partie["choix_ordi"] = None
                etat_partie["resultat"] = None
                etat_partie["score_incremente"] = False
    return etat_partie


def gerer_partie(
    ecran, police_bouton, pos_souris, clic_souris, evenements, etat_partie
):
    # Préparation des boutons de choix (cercles)
    choix_textes = ["pierre", "papier", "ciseaux"]
    nb_choix = len(choix_textes)
    diametre_choix = 140
    rayon_choix = diametre_choix // 2
    espacement = 80
    total_largeur = nb_choix * diametre_choix + (nb_choix - 1) * espacement
    x_depart = (WINDOW_WIDTH - total_largeur) // 2
    y_choix = WINDOW_HEIGHT - diametre_choix - 40
    rects_choix = [
        pygame.Rect(
            x_depart + i * (diametre_choix + espacement),
            y_choix,
            diametre_choix,
            diametre_choix,
        )
        for i in range(nb_choix)
    ]
    # Routing selon l'état
    if etat_partie.get("etat", "attente_choix") == "attente_choix":
        etat_partie = afficher_attente_choix(
            ecran,
            police_bouton,
            pos_souris,
            clic_souris,
            evenements,
            etat_partie,
            rects_choix,
            choix_textes,
        )
    elif etat_partie["etat"] == "affichage_choix":
        etat_partie = afficher_affichage_choix(ecran, police_bouton, etat_partie)
    elif etat_partie["etat"] == "resultat":
        etat_partie = afficher_resultat(
            ecran, police_bouton, pos_souris, clic_souris, evenements, etat_partie
        )
    return "partie", etat_partie
