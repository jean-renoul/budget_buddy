import pygame
import sys
from Db import Db  # Importez votre classe Db

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Connexion à la base de données
db = Db("82.165.185.52", "budget-buddy", "database-budget-buddy", "jean-renoul_budget-buddy")

# Fonction pour récupérer les transactions d'un utilisateur spécifique
def get_transactions_by_user(user_id):
    query = "SELECT * FROM transactions WHERE user_id = %s"
    return db.fetch(query, (user_id,))

# Définition de l'ID de l'utilisateur
user_id = 4  # Remplacez par l'ID de l'utilisateur souhaité

try:
    # Récupération des transactions de l'utilisateur spécifié
    transactions = get_transactions_by_user(user_id)

    # Création de deux dictionnaires pour stocker les montants de revenus et de dépenses par catégorie
    income_sum = {}
    expense_sum = {}

    for transaction in transactions:
        category = transaction[4]
        amount = float(transaction[5])
        transaction_type = transaction[6].lower()
        if transaction_type == "expense":
            if category in expense_sum:
                expense_sum[category] += amount
            else:
                expense_sum[category] = amount
        else:
            if category in income_sum:
                income_sum[category] += amount
            else:
                income_sum[category] = amount

    # Calcul de la somme maximale pour ajuster l'échelle
    max_category_sum = max(max(income_sum.values(), default=0), max(expense_sum.values(), default=0))

finally:
    # Fermeture de la connexion à la base de données
    db.disconnect()

# Positions et tailles pour les diagrammes
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Diagrammes des Transactions")
chart_x, chart_y = 100, 100
chart_width, chart_height = 600, 500
bar_width = 20
space_between_bars = 50

# Font pour les libellés
font = pygame.font.SysFont(None, 24)

# Dessin du diagramme des dépenses
for i, (category, amount) in enumerate(expense_sum.items()):
    bar_x = chart_x + i * (bar_width + space_between_bars)
    bar_height = int(amount / max_category_sum * chart_height)
    bar_y = chart_y + chart_height - bar_height
    pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
    category_text = font.render(category, True, WHITE)
    category_text_rect = category_text.get_rect(midtop=(bar_x + bar_width // 2, bar_y - 5))
    screen.blit(category_text, category_text_rect)

# Dessin du diagramme des revenus
for i, (category, amount) in enumerate(income_sum.items()):
    bar_x = chart_x + chart_width - (i + 1) * (bar_width + space_between_bars)
    bar_height = int(amount / max_category_sum * chart_height)
    bar_y = chart_y + chart_height - bar_height
    pygame.draw.rect(screen, GREEN, (bar_x, bar_y, bar_width, bar_height))
    category_text = font.render(category, True, WHITE)
    category_text_rect = category_text.get_rect(midtop=(bar_x + bar_width // 2, bar_y - 5))
    screen.blit(category_text, category_text_rect)

# Ajouter les libellés des axes
axis_x_text = font.render("Types de Transaction", True, WHITE)
axis_x_text_rect = axis_x_text.get_rect(center=(chart_x + chart_width // 2, chart_y + chart_height + 50))
screen.blit(axis_x_text, axis_x_text_rect)

axis_y_text = font.render("Montant", True, WHITE)
axis_y_text = pygame.transform.rotate(axis_y_text, 90)
axis_y_text_rect = axis_y_text.get_rect(center=(chart_x - 30, chart_y + chart_height // 2))
screen.blit(axis_y_text, axis_y_text_rect)

# Ajouter les repères sur l'axe des ordonnées (montant)
scale_y = 100
while scale_y <= max_category_sum:
    scale_y_pos = chart_y + chart_height - int(scale_y / max_category_sum * chart_height)
    pygame.draw.line(screen, WHITE, (chart_x - 5, scale_y_pos), (chart_x, scale_y_pos))
    scale_y_text = font.render(str(scale_y), True, WHITE)
    screen.blit(scale_y_text, (chart_x - 40, scale_y_pos - 10))
    scale_y += 100

# Ajouter les repères sur l'axe des abscisses (catégories)
scale_x = chart_x + chart_width
for category in income_sum.keys():
    scale_x -= bar_width + space_between_bars
    scale_x_pos = scale_x - (bar_width + space_between_bars) // 2
    scale_x_text = font.render(category, True, WHITE)
    screen.blit(scale_x_text, (scale_x_pos, chart_y + chart_height + 10))

# Ajouter la séparation entre les dépenses et les revenus
pygame.draw.line(screen, WHITE, (chart_x + chart_width // 2, chart_y), (chart_x + chart_width // 2, chart_y + chart_height), 2)

# Ajouter les libellés "Dépenses" et "Revenus"
expense_label = font.render("Dépenses", True, WHITE)
expense_label_rect = expense_label.get_rect(midtop=(chart_x + chart_width // 4, chart_y))
screen.blit(expense_label, expense_label_rect)

income_label = font.render("Revenus", True, WHITE)
income_label_rect = income_label.get_rect(midtop=(chart_x + 3 * chart_width // 4, chart_y))
screen.blit(income_label, income_label_rect)

# Actualisation de l'écran
pygame.display.flip()

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quitter Pygame
pygame.quit()
sys.exit()

