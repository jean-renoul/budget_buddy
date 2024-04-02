import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Taille de la fenêtre
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Création de la fenêtre
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Accueil Compte Bancaire")

# Font
font = pygame.font.SysFont(None, 50)

def main_menu():
    running = True
    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

        # Effacer l'écran
        window.fill(WHITE)

        # Dessiner le texte
        title_text = font.render("Bienvenue dans votre banque", True, BLACK)
        window.blit(title_text, (WINDOW_WIDTH//2 - title_text.get_width()//2, 200))

        instruction_text = font.render("Appuyez sur Q pour quitter", True, BLACK)
        window.blit(instruction_text, (WINDOW_WIDTH//2 - instruction_text.get_width()//2, 300))

        # Actualiser l'affichage
        pygame.display.update()

# Lancement du menu principal
main_menu()

# Quitter Pygame
pygame.quit()
sys.exit()
