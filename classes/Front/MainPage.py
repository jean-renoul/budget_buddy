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
        self.transactions_per_page = 7

        # Clock
        self.clock = pygame.time.Clock()
        # Texte de bienvenue
        self.welcome_text = self.font.render("Budget Buddy", True, self.BLACK)
        self.welcome_text_rect = self.welcome_text.get_rect(center=(self.screen_width // 2, 50))

        # Chargement de l'image du logo du menu et redimensionnement
        self.menu_logo = pygame.image.load("images/menu_icon.png")  
        self.menu_logo = pygame.transform.scale(self.menu_logo, (40, 50)) 
        self.menu_logo_rect = self.menu_logo.get_rect(x=20, y=20)

        self.background_image = pygame.image.load("images/MainPage.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))

        # Options du menu
        self.menu_options = [
            "Main page",
            "Display transactions",
            "Transfer money",
            "Settings",
            "Quitter"
        ]

        self.menu_option_rects = []

        # Position initiale du menu déroulant
        self.MENU_START_X, self.MENU_START_Y = 20, 70
        self.MENU_WIDTH, self.MENU_HEIGHT = 200, 40
        self.MENU_SPACING = 40

        # Détermine si le menu est affiché ou non
        self.welcome = False
        self.menu_open = False
        self.menu_transactions = False
        self.menu_transfer = False
        self.menu_exit = False
        self.sort_by_amount = False
        self.sort_by_date = False
        self.sort_by_type = False
        self.sort_by_category = False
        self.add_transaction = False

        self.BUTTON_WIDTH, self.BUTTON_HEIGHT = 120, 30
        self.button_font = pygame.font.Font(None, 20)
        self.button_color = self.BLUE
        self.button_hover_color = self.GREEN
        self.button_texts = ["Sort by Date", "Sort by Amount", "Sort by Type", "Sort by Category"]
        self.button_rects = []
        self.transfer_data = {"name": "", "description": "", "category": "", "amount": "", "type": ""}
        self.active_field = None
        self.text_input = {name: False for name in self.transfer_data.keys()}
        self.send_button = pygame.Rect(350, 500, 60, 50)
        self.create_sort_buttons()


    def main_page(self):
        self.screen.blit(self.background_image, (0, 0))
        self.display_menu()
        if self.menu_open == True:
            self.display_open_menu()
        pygame.display.flip()        

    def create_sort_buttons(self):
        
        button_start_y = 350  # Adjust this value to set the starting position of buttons
        for i, text in enumerate(self.button_texts):
            button_rect = pygame.Rect((self.screen_width - self.BUTTON_WIDTH) // 2, button_start_y + i * (self.BUTTON_HEIGHT + 10), self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
            self.button_rects.append(button_rect)    
        

    def display_menu(self):

        # Affichage du texte de bienvenue
        self.screen.blit(self.welcome_text, self.welcome_text_rect)

        # Affichage du logo du menu
        self.screen.blit(self.menu_logo, self.menu_logo_rect)


    # Fonction pour afficher le menu
    def display_open_menu(self):

        for i, option in enumerate(self.menu_options):
            text = self.font.render(option, True, self.BLACK)
            text_rect = text.get_rect(x=self.MENU_START_X, y=self.MENU_START_Y + i * self.MENU_SPACING)
            self.menu_option_rects.append(text_rect)
            self.screen.blit(text, text_rect)

        # Affichage du logo du menu
        self.screen.blit(self.menu_logo, self.menu_logo_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if self.menu_logo_rect.collidepoint(event.pos):
                        self.menu_open = not self.menu_open
                    if self.menu_open:
                        for i, option_rect in enumerate(self.menu_option_rects):
                            if option_rect.collidepoint(event.pos):
                                if i == 0:
                                    self.menu_open = False
                                    self.menu_transactions = False
                                    self.menu_transfer = False
                                    self.welcome = True
                                elif i == 1:
                                    self.menu_transactions = True
                                    self.menu_open = False
                                    self.menu_transfer = False
                                    self.welcome = False
                                elif i == 2:
                                    self.menu_transfer = True
                                    self.menu_open = False
                                    self.menu_transactions = False
                                    self.welcome = False
                                elif i == 4:
                                    self.main_page = False
                                    self.menu_transfer = False
                                    self.menu_open = False
                                    self.menu_transactions = False
                                    self.welcome = False
                                    self.menu_exit = True
                               

    def run(self):
        self.handle_events()
        self.main_page()
        self.clock.tick(60)
        # Affichage du menu déroulant si ouvert
            

if __name__ == "__main__":
    # Ajouter une instance de User factice pour le test
    main_page = MainPage(user=None)
    main_page.run()
