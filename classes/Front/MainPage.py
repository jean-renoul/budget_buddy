import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Définition de la taille de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Banque App - Accueil")

# Définition de la police
font = pygame.font.Font(None, 36)

# Options du menu
menu_options = [
    "Consulter le solde",
    "Quitter"
]

# Position initiale du menu
menu_x, menu_y = 20, 20
menu_spacing = 40

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Effacer l'écran
    screen.fill(WHITE)
    
    # Affichage du menu
    for i, option in enumerate(menu_options):
        text = font.render(option, True, BLACK)
        text_rect = text.get_rect(x=menu_x, y=menu_y + i * menu_spacing)
        screen.blit(text, text_rect)
    
    # Actualisation de l'écran
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
sys.exit()
