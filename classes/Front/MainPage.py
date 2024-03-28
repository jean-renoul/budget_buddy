import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 102, 204)

# Définition de la taille de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Accueil - Banque BNP Paribas")

# Font pour le texte
font = pygame.font.Font(None, 36)

# Texte de bienvenue
welcome_text = font.render("Bienvenue sur l'application Banque BNP Paribas", True, WHITE)
welcome_text_rect = welcome_text.get_rect(center=(WIDTH // 2, 50))

# Chargement de l'image du logo du menu et redimensionnement
menu_logo = pygame.image.load("images/Capture d'écran 2024-03-28 124959.png")  
menu_logo = pygame.transform.scale(menu_logo, (50, 50)) 
menu_logo_rect = menu_logo.get_rect(x=20, y=20)

# Options du menu
menu_options = [
    "Consulter le solde",f'r'
    "Effectuer un virement",
    "Paramètres",
    "Quitter"
]

# Position initiale du menu déroulant
MENU_START_X, MENU_START_Y = 20, 70
MENU_WIDTH, MENU_HEIGHT = 200, 40
MENU_SPACING = 40

# Détermine si le menu est affiché ou non
menu_open = False

# Fonction pour afficher le menu
def display_menu():
    for i, option in enumerate(menu_options):
        text = font.render(option, True, WHITE)
        text_rect = text.get_rect(x=MENU_START_X, y=MENU_START_Y + i * MENU_SPACING)
        pygame.draw.rect(screen, BLACK, (MENU_START_X, MENU_START_Y + i * MENU_SPACING, MENU_WIDTH, MENU_HEIGHT))
        screen.blit(text, text_rect)

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if menu_logo_rect.collidepoint(event.pos):
                menu_open = not menu_open

    # Remplir l'écran avec une couleur noire
    screen.fill(BLACK)

    # Affichage du texte de bienvenue
    screen.blit(welcome_text, welcome_text_rect)

    # Affichage du logo du menu
    screen.blit(menu_logo, menu_logo_rect)

    # Affichage du menu déroulant si ouvert
    if menu_open:
        display_menu()

    # Actualisation de l'écran
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
sys.exit()
