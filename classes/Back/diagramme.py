import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 102, 204)
GRAY = (200, 200, 200)

# Définition de la taille de la fenêtre
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Diagramme des Transactions")

# Données de test pour le diagramme
categories = ["Food", "DIY", "Work"]
amounts = [200, 150, 300]  # Montants des transactions par catégorie

# Positions et tailles pour le diagramme
chart_x, chart_y = 100, 100
chart_width, chart_height = 600, 500
bar_width = 50
space_between_bars = 50

# Font pour les libellés
font = pygame.font.SysFont(None, 24)

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Effacer l'écran
    screen.fill(WHITE)
    
    # Affichage du diagramme
    max_amount = max(amounts)
    for i, (category, amount) in enumerate(zip(categories, amounts)):
        # Calculer la position et la taille de la barre
        bar_x = chart_x + i * (bar_width + space_between_bars)
        bar_height = int(amount / max_amount * chart_height)
        bar_y = chart_y + chart_height - bar_height
        
        # Dessiner la barre
        pygame.draw.rect(screen, BLUE, (bar_x, bar_y, bar_width, bar_height))
        
        # Ajouter le libellé de la catégorie
        category_text = font.render(category, True, BLACK)
        category_text_rect = category_text.get_rect(center=(bar_x + bar_width // 2, chart_y + chart_height + 20))
        screen.blit(category_text, category_text_rect)
    
    # Ajouter les libellés des axes
    axis_x_text = font.render("Categories", True, BLACK)
    axis_x_text_rect = axis_x_text.get_rect(center=(chart_x + chart_width // 2, chart_y + chart_height + 50))
    screen.blit(axis_x_text, axis_x_text_rect)
    
    axis_y_text = font.render("Amount", True, BLACK)
    axis_y_text = pygame.transform.rotate(axis_y_text, 90)
    axis_y_text_rect = axis_y_text.get_rect(center=(chart_x - 30, chart_y + chart_height // 2))
    screen.blit(axis_y_text, axis_y_text_rect)
    
    # Actualisation de l'écran
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
sys.exit()
