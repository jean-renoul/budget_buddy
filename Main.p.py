import pygame
from classes.Back.Transactions import TransactionManager

# Initialisation de Pygame
pygame.init()

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Dimensions de la fenêtre
WIDTH, HEIGHT = 400, 300

class UserInterface:
    def __init__(self):
        self.transaction_manager = TransactionManager()

        # Création de la fenêtre
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Gestionnaire de Transactions")

        # Police de texte
        self.font = pygame.font.Font(None, 36)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Vous pouvez ajouter ici la gestion des clics de souris pour ajouter une transaction

            # Efface l'écran
            self.screen.fill(WHITE)

            # Affiche la balance
            balance_text = self.font.render("Balance: " + str(self.transaction_manager.balance_updater.get_user_balance(4)), True, BLACK)
            self.screen.blit(balance_text, (50, 50))

            # Rafraîchit l'affichage
            pygame.display.flip()

        pygame.quit()

def main():
    ui = UserInterface()
    ui.run()

if __name__ == "__main__":
    main()
