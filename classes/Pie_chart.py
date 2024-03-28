import pygame
import math
import random
from Db import Db
# Classe représentant le diagramme circulaire
class PieChart:
    def __init__(self, user_id):
        self.user_id = user_id
        self.db = Db("82.165.185.52", "budget-buddy", "database-budget-buddy", "jean-renoul_budget-buddy")


    # Fonction pour récupérer les catégories, les valeurs et les types à partir de la base de données
    def get_categories_values_and_types(self):
        querry = "SELECT category, SUM(amount), type FROM transactions WHERE user_id = %s GROUP BY category, type"
        arg = (self.user_id,)
        result = self.db.fetch(querry, arg)
        categories = []
        values = []
        types = []
        for row in result:
            categories.append(row[0])
            values.append(float(row[1]))
            types.append(row[2])
        return categories, values, types

    # Dessiner le diagramme circulaire
    def draw(self):
        pygame.init()

        # Définition de la palette de couleurs
        COLORS = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(10)]

        # Création de la fenêtre
        screen_width, screen_height = 800, 600
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Pie Chart")

        # Récupération des catégories, des valeurs et des types
        categories, values, types = self.get_categories_values_and_types()

        # Titre du diagramme
        font_title = pygame.font.SysFont(None, 24)
        title_text = "Diagramme des transactions"
        title_surface = font_title.render(title_text, True, (0, 0, 0))
        title_rect = title_surface.get_rect()
        title_rect.center = (screen_width // 2, 20)

        # Boucle principale
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Effacer l'écran
            screen.fill((255, 255, 255))

            # Afficher le titre
            screen.blit(title_surface, title_rect)

            # Position et taille du cercle
            circle_x, circle_y = screen_width // 2, screen_height // 2
            circle_radius = min(screen_width, screen_height) // 3

            # Initialiser l'angle de départ
            start_angle = -math.pi / 2

            # Dessiner chaque portion du diagramme circulaire
            for i, (category, value, transaction_type) in enumerate(zip(categories, values, types)):
                # Calculer l'angle de fin pour cette portion
                end_angle = start_angle + 2 * math.pi * (value / sum(values))

                # Dessiner l'arc correspondant à cette portion avec une couleur aléatoire
                color = COLORS[i % len(COLORS)]
                pygame.draw.arc(screen, color, (circle_x - circle_radius, circle_y - circle_radius, circle_radius * 2, circle_radius * 2),
                                start_angle, end_angle, circle_radius)

                # Mettre à jour l'angle de départ pour la prochaine portion
                start_angle = end_angle

                # Dessiner le nom de la catégorie, le montant et le type à côté de la portion
                font = pygame.font.SysFont(None, 20)
                percentage = value / sum(values) * 100
                text = f"{category}: {value:.2f} EUR ({transaction_type})"
                text_surface = font.render(text, True, color)  # Utiliser la même couleur que l'arc
                text_rect = text_surface.get_rect()
                text_rect.center = ((circle_x + circle_radius + 20 + screen_width) // 2, circle_y - circle_radius // 2 + i * 30)
                screen.blit(text_surface, text_rect)

            # Mettre à jour l'affichage
            pygame.display.flip()

        # Fermer la connexion à la base de données et quitter Pygame
        self.db.close()
        pygame.quit()

# Exemple d'utilisation de la classe PieChart
if __name__ == "__main__":
    pie_chart = PieChart(4)  # Remplacez par l'ID utilisateur souhaité
    pie_chart.draw()
