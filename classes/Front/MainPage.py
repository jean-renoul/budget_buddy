import pygame
import sys

class MainPage:
    def __init__(self, user):
        self.user = user
        self.transactions = user.transactions

        # Initialize Pygame
        pygame.init()

        # Screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Budget Buddy")

        # Fonts and colors
        self.font = pygame.font.Font(None, 24)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.COLOR1 = (237,190,164)
        self.COLOR2 = (154,208,211)
        self.GREEN = (0, 100, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 102, 204)

        # Scroll settings
        self.scroll_offset = 0
        self.transactions_per_page = 5

        # Clock
        self.clock = pygame.time.Clock()
        # Texte de bienvenue
        self.welcome_text = self.font.render("Bienvenue sur l'application Budget Buddy", True, self.WHITE)
        self.welcome_text_rect = self.welcome_text.get_rect(center=(self.screen_width // 2, 50))

        # Chargement de l'image du logo du menu et redimensionnement
        self.menu_logo = pygame.image.load("images/Capture d'écran 2024-03-28 124959.png")  
        self.menu_logo = pygame.transform.scale(self.menu_logo, (50, 50)) 
        self.menu_logo_rect = self.menu_logo.get_rect(x=20, y=20)

        # Options du menu
        self.menu_options = [
            "Afficher les transactions",
            "Effectuer un virement",
            "Paramètres",
            "Quitter"
        ]

        self.menu_option_rects = []

        # Position initiale du menu déroulant
        self.MENU_START_X, self.MENU_START_Y = 20, 70
        self.MENU_WIDTH, self.MENU_HEIGHT = 200, 40
        self.MENU_SPACING = 40

        # Détermine si le menu est affiché ou non
        self.menu_open = False
        self.menu_transactions = False

        # Remplir l'écran avec une couleur noire
        self.screen.fill(self.BLACK)

        # Affichage du texte de bienvenue
        self.screen.blit(self.welcome_text, self.welcome_text_rect)

        # Affichage du logo du menu
        self.screen.blit(self.menu_logo, self.menu_logo_rect)

    def display_transactions(self):
        # Clear the screen
        self.screen.fill(self.COLOR1)

        # Display account balance
        balance_text = self.font.render(f"Balance: ${self.user.balance}", True, self.BLACK)
        self.screen.blit(balance_text, (self.screen_width / 2 - 50, 20))
        # Display each transaction
        transaction_text = self.font.render("Transactions", True, self.BLACK)
        self.screen.blit(transaction_text, (self.screen_width/2 - transaction_text.get_width()/2, 100))

        visible_transactions = self.transactions[self.scroll_offset:self.scroll_offset+self.transactions_per_page]

        for i, transaction in enumerate(visible_transactions):
            if transaction[5] == "expense" or transaction[5] == "Expense":
                transaction = f"-{transaction[2]}$ : {transaction[0]} ({transaction[1]}) ({transaction[3]}) category: {transaction[4]}"
                text = self.font.render(f"{transaction}", True, self.RED)
            elif transaction[5] == "income" or transaction[5] == "Income":
                transaction = f"+{transaction[2]}$ : {transaction[0]} ({transaction[1]}) ({transaction[3]}) category: {transaction[4]}"
                text = self.font.render(f"{transaction}", True, self.GREEN)
            self.screen.blit(text, (self.screen_width/2 - text.get_width()/2, 130 + i * 30))  # Adjust the position as needed

        # Draw scroll bar
        pygame.draw.rect(self.screen, self.BLACK, (self.screen_width - 20, 130, 10, self.screen_height - 160))
        bar_position = (self.scroll_offset / len(self.transactions)) * (self.screen_height - 160)
        pygame.draw.rect(self.screen, self.WHITE, (self.screen_width - 20, 130 + bar_position, 10, 40))

        # Update the display
        pygame.display.flip()


    def display_menu(self):

        # Remplir l'écran avec une couleur noire
        self.screen.fill(self.BLACK)

        # Affichage du texte de bienvenue
        self.screen.blit(self.welcome_text, self.welcome_text_rect)

        # Affichage du logo du menu
        self.screen.blit(self.menu_logo, self.menu_logo_rect)

        # Actualisation de l'écran
        pygame.display.flip()


    # Fonction pour afficher le menu
    def display_open_menu(self):
        # Remplir l'écran avec une couleur noire
        self.screen.fill(self.BLACK)

        for i, option in enumerate(self.menu_options):
            text = self.font.render(option, True, self.WHITE)
            text_rect = text.get_rect(x=self.MENU_START_X, y=self.MENU_START_Y + i * self.MENU_SPACING)
            self.menu_option_rects.append(text_rect)
            pygame.draw.rect(self.screen, self.BLACK, (self.MENU_START_X, self.MENU_START_Y + i * self.MENU_SPACING, self.MENU_WIDTH, self.MENU_HEIGHT))
            self.screen.blit(text, text_rect)        

        # Affichage du texte de bienvenue
        self.screen.blit(self.welcome_text, self.welcome_text_rect)

        # Affichage du logo du menu
        self.screen.blit(self.menu_logo, self.menu_logo_rect)

        # Actualisation de l'écran
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    self.scroll_offset = max(0, self.scroll_offset - 1)
                elif event.button == 5:  # Scroll down
                    self.scroll_offset = min(len(self.transactions) - self.transactions_per_page, self.scroll_offset + 1)
                elif event.button == 1:  # Left mouse button
                    if self.menu_logo_rect.collidepoint(event.pos):
                        self.menu_open = not self.menu_open
                    elif self.menu_open:
                        for i, option_rect in enumerate(self.menu_option_rects):
                            if option_rect.collidepoint(event.pos):
                                if i == 0:  # If the first option is clicked
                                    self.menu_transactions = True
                                    self.menu_open = False
                                    break  # No need to check further options


    def run(self):
        while True:
            self.handle_events()
            if self.menu_open == True:
                self.display_open_menu()
            elif self.menu_transactions == True:
                self.display_transactions()
            else:
                self.display_menu()
            self.clock.tick(60)
            # Affichage du menu déroulant si ouvert
            

if __name__ == "__main__":
    main_page = MainPage()
    main_page.run()