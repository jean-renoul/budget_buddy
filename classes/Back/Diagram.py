import pygame
import sys
from classes.Back.Db import Db  # Importez votre classe Db

class Diagram:
    def __init__(self, user_id):
        self.user_id = user_id
        self.transactions = None
        self.income_sum = {}
        self.expense_sum = {}
        self.max_category_sum = 0

    def fetch_transactions(self):
        # Connexion à la base de données
        db = Db("82.165.185.52", "budget-buddy", "database-budget-buddy", "jean-renoul_budget-buddy")
        try:
            # Récupération des transactions de l'utilisateur spécifié
            query = "SELECT * FROM transactions WHERE user_id = %s"
            self.transactions = db.fetch(query, (self.user_id,))
        finally:
            # Fermeture de la connexion à la base de données
            db.disconnect()

    def calculate_sums(self):
        # Création de deux dictionnaires pour stocker les montants de revenus et de dépenses par catégorie
        for transaction in self.transactions:
            category = transaction[4]
            amount = float(transaction[5])
            transaction_type = transaction[6].lower()
            if transaction_type == "expense":
                if category in self.expense_sum:
                    self.expense_sum[category] += amount
                else:
                    self.expense_sum[category] = amount
            else:
                if category in self.income_sum:
                    self.income_sum[category] += amount
                else:
                    self.income_sum[category] = amount

        # Calcul de la somme maximale pour ajuster l'échelle
        self.max_category_sum = max(max(self.income_sum.values(), default=0), max(self.expense_sum.values(), default=0))

    def draw_diagram(self):
        # Initialisation de Pygame
        pygame.init()

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
        for i, (category, amount) in enumerate(self.expense_sum.items()):
            bar_x = chart_x + i * (bar_width + space_between_bars)
            bar_height = int(amount / self.max_category_sum * chart_height)
            bar_y = chart_y + chart_height - bar_height
            pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
            category_text = font.render(category, True, (255, 255, 255))
            category_text_rect = category_text.get_rect(midtop=(bar_x + bar_width // 2, bar_y - 5))
            screen.blit(category_text, category_text_rect)

        # Dessin du diagramme des revenus
        for i, (category, amount) in enumerate(self.income_sum.items()):
            bar_x = chart_x + chart_width - (i + 1) * (bar_width + space_between_bars)
            bar_height = int(amount / self.max_category_sum * chart_height)
            bar_y = chart_y + chart_height - bar_height
            pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width, bar_height))
            category_text = font.render(category, True, (255, 255, 255))
            category_text_rect = category_text.get_rect(midtop=(bar_x + bar_width // 2, bar_y - 5))
            screen.blit(category_text, category_text_rect)

        # Ajouter les libellés des axes
        axis_x_text = font.render("Types de Transaction", True, (255, 255, 255))
        axis_x_text_rect = axis_x_text.get_rect(center=(chart_x + chart_width // 2, chart_y + chart_height + 50))
        screen.blit(axis_x_text, axis_x_text_rect)

        axis_y_text = font.render("Montant", True, (255, 255, 255))
        axis_y_text = pygame.transform.rotate(axis_y_text, 90)
        axis_y_text_rect = axis_y_text.get_rect(center=(chart_x - 30, chart_y + chart_height // 2))
        screen.blit(axis_y_text, axis_y_text_rect)

        # Ajouter les repères sur l'axe des ordonnées (montant)
        scale_y = 100
        while scale_y <= self.max_category_sum:
            scale_y_pos = chart_y + chart_height - int(scale_y / self.max_category_sum * chart_height)
            pygame.draw.line(screen, (255, 255, 255), (chart_x - 5, scale_y_pos), (chart_x, scale_y_pos))
            scale_y_text = font.render(str(scale_y), True, (255, 255, 255))
            screen.blit(scale_y_text, (chart_x - 40, scale_y_pos - 10))
            scale_y += 100

        # Ajouter les repères sur l'axe des abscisses (catégories)
        scale_x = chart_x + chart_width
        for category in self.income_sum.keys():
            scale_x -= bar_width + space_between_bars
            scale_x_pos = scale_x - (bar_width + space_between_bars) // 2
            scale_x_text = font.render(category, True, (255, 255, 255))
            screen.blit(scale_x_text, (scale_x_pos, chart_y + chart_height + 10))

        # Ajouter la séparation entre les dépenses et les revenus
        pygame.draw.line(screen, (255, 255, 255), (chart_x + chart_width // 2, chart_y), (chart_x + chart_width // 2, chart_y + chart_height), 2)

        # Ajouter les libellés "Dépenses" et "Revenus"
        expense_label = font.render("Dépenses", True, (255, 255, 255))
        expense_label_rect = expense_label.get_rect(midtop=(chart_x + chart_width // 4, chart_y))
        screen.blit(expense_label, expense_label_rect)

        income_label = font.render("Revenus", True, (255, 255, 255))
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

# Utilisation de la classe TransactionDiagram
if __name__ == "__main__":
    user_id = 4  # Remplacez par l'ID de l'utilisateur souhaité
    diagram = Diagram(user_id)
    diagram.fetch_transactions()
    diagram.calculate_sums()
    diagram.draw_diagram()
