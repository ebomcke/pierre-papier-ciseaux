import os
import pygame

# Constantes pour la taille de la fenêtre
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
DARK_BLUE = (40, 90, 140)


def charger_image(nom_fichier, size=None):
    """Charge une image depuis le dossier du module, avec gestion d'erreur et redimensionnement optionnel."""
    chemin = os.path.join(os.path.dirname(__file__), nom_fichier)
    try:
        img = pygame.image.load(chemin)
        if size:
            img = pygame.transform.smoothscale(img.convert_alpha(), size)
        else:
            img = img.convert_alpha()
        return img
    except Exception as e:
        print(
            f"Erreur : Impossible de charger '{nom_fichier}'. Placez le fichier dans le dossier du module ppc_game."
        )
        print(f"Chemin attendu : {os.path.abspath(chemin)}")
        print(f"Détail de l'erreur : {e}")
        return None
