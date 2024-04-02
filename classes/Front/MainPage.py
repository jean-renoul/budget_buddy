import pygame
import sys
import math
import random
from classes.Back.Db import Db
from classes.Back.PieChart import PieChart

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
        self.COLOR1 = (237, 190, 164)
        self.COLOR2 = (154, 208, 211)
        self.GREEN = (0, 100, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 102, 204)
        self.GREY = (200, 200, 200)

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
            "Display Pie Chart",
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
        self.menu_profile = False
        self.message_text = None  # Track the error message text
        self.message_timer = 0     # Timer to control the duration of error message display
        self.message_duration = 2000  # Duration to display the error message in milliseconds

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
        
        self.notification_logo = pygame.image.load("images/20268741-notification-icone-pour-votre-site-internet-conception-logo-application-ui-gratuit-vectoriel.jpg")
        self.notification_logo = pygame.transform.scale(self.notification_logo, (40, 40))
        self.notification_logo_rect = self.notification_logo.get_rect(x=self.screen_width - 60, y=self.screen_height - 60)

        self.pie_chart = PieChart(self.user.id)

    def main_page(self):
        self.screen.blit(self.background_image, (0, 0))
        self.display_menu()
        if self.menu_open == True:
            self.display_open_menu()

        balance_text = self.font.render(f"Balance: {self.user.get_balance()}$", True, self.BLACK)
        balance_text_rect = balance_text.get_rect(center=(self.screen_width // 2, 150))
        self.screen.blit(balance_text, balance_text_rect)
        self.screen.blit(self.notification_logo, self.notification_logo_rect)
        
        
        self.draw_graph()

        pygame.display.flip()

    def transfer_page(self):
        # Affichage de la page de transfert
        self.screen.blit(self.background_image, (0, 0))
        self.display_menu()
        if self.menu_open == True:
            self.display_open_menu()

        # Affichage des étiquettes du formulaire de transfert
        name_label = self.font.render("Name:", True, self.BLACK)
        name_rect = name_label.get_rect(x=200, y=200)
        self.screen.blit(name_label, name_rect)

        description_label = self.font.render("Description:", True, self.BLACK)
        description_rect = description_label.get_rect(x=200, y=250)
        self.screen.blit(description_label, description_rect)

        category_label = self.font.render("Category:", True, self.BLACK)
        category_rect = category_label.get_rect(x=200, y=300)
        self.screen.blit(category_label, category_rect)

        amount_label = self.font.render("Amount:", True, self.BLACK)
        amount_rect = amount_label.get_rect(x=200, y=350)
        self.screen.blit(amount_label, amount_rect)

        type_label = self.font.render("Type:", True, self.BLACK)
        type_rect = type_label.get_rect(x=200, y=400)
        self.screen.blit(type_label, type_rect)

        # Affichage des champs de saisie
        name_input_text = self.font.render(self.transfer_data.get('name', ''), True, self.BLACK)
        pygame.draw.rect(self.screen, self.COLOR2, (350, 200, 200, 30))  # Name input box
        self.screen.blit(name_input_text, (355, 205))

        description_input_text = self.font.render(self.transfer_data.get('description', ''), True, self.BLACK)
        pygame.draw.rect(self.screen, self.COLOR2, (350, 250, 200, 30))  # Description input box
        self.screen.blit(description_input_text, (355, 255))

        category_input_text = self.font.render(self.transfer_data.get('category', ''), True, self.BLACK)
        pygame.draw.rect(self.screen, self.COLOR2, (350, 300, 200, 30))  # Category input box
        self.screen.blit(category_input_text, (355, 305))

        amount_input_text = self.font.render(str(self.transfer_data.get('amount', '')), True, self.BLACK)
        pygame.draw.rect(self.screen, self.COLOR2, (350, 350, 200, 30))  # Amount input box
        self.screen.blit(amount_input_text, (355, 355))

        type_input_text = self.font.render(self.transfer_data.get('type', ''), True, self.BLACK)
        pygame.draw.rect(self.screen, self.COLOR2, (350, 400, 200, 30))  # Type input box
        self.screen.blit(type_input_text, (355, 405))

        for name, value in self.transfer_data.items():
            input_text = self.font.render(value, True, self.BLACK)
            input_rect = pygame.Rect(350, 200 + list(self.transfer_data.keys()).index(name) * 50, 200, 30)
            pygame.draw.rect(self.screen, self.COLOR2, input_rect)  # Input box
            self.screen.blit(input_text, (input_rect.x + 5, input_rect.y + 5))

        pygame.draw.rect(self.screen, self.COLOR2, self.send_button)
        send_text = self.font.render("Send", True, self.BLACK)
        self.screen.blit(send_text, (self.send_button.x + 10, self.send_button.y + 10))

        pygame.display.flip()

    def check_input_boxes(self, position):
        # Vérifie si une boîte de saisie est cliquée et la définit comme champ actif
        for name in self.transfer_data.keys():
            input_box_rect = pygame.Rect(350, 200 + list(self.transfer_data.keys()).index(name) * 50, 200, 30)
            if input_box_rect.collidepoint(position):
                self.active_field = name
                if not self.text_input[name]:
                    self.transfer_data[name] = ""
                    return
        # Si aucune boîte de saisie n'est cliquée, désactive le champ actif
        self.active_field = None

    def create_sort_buttons(self):
        # Crée les boutons de tri
        button_start_y = 350  
        for i, text in enumerate(self.button_texts):
            button_rect = pygame.Rect((self.screen_width - self.BUTTON_WIDTH) // 2, button_start_y + i * (self.BUTTON_HEIGHT + 10), self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
            self.button_rects.append(button_rect)    

    def display_menu(self):
        # Affiche le texte de bienvenue et le logo du menu
        self.screen.blit(self.welcome_text, self.welcome_text_rect)
        self.screen.blit(self.menu_logo, self.menu_logo_rect)

    def display_open_menu(self):
        # Affiche le menu déroulant
        for i, option in enumerate(self.menu_options):
            text = self.font.render(option, True, self.BLACK)
            text_rect = text.get_rect(x=self.MENU_START_X, y=self.MENU_START_Y + i * self.MENU_SPACING)
            self.menu_option_rects.append(text_rect)
            self.screen.blit(text, text_rect)
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
                                    self.welcome = True
                                    self.menu_open = False
                                    self.menu_transactions = False
                                    self.menu_transfer = False
                                    self.menu_profile = False                                    
                                if i == 1:  # If the first option is clicked
                                    self.menu_transactions = True
                                    self.menu_open = False
                                    self.menu_transfer = False
                                    self.welcome = False
                                    self.menu_profile = False
                                if i == 2:
                                    self.menu_transfer = True
                                    self.menu_open = False
                                    self.menu_transactions = False
                                    self.welcome = False
                                    self.menu_profile = False
                                if i == 3:
                                    self.menu_profile = True
                                    self.menu_open = False
                                    self.menu_transactions = False
                                    self.welcome = False
                                    self.menu_transfer = False
                                if i == 4:
                                    self.display_pie_chart()
                                elif i == 5:
                                    self.menu_transfer = False
                                    self.menu_open = False
                                    self.menu_transactions = False
                                    self.welcome = False
                                    self.menu_exit = True
                                if self.menu_exit:
                                    self.exit_page()    

    def display_pie_chart(self):
        self.pie_chart.draw()

    def message(self, message):
        self.message_text = self.font.render(message, True, self.BLACK)
        self.message_timer = pygame.time.get_ticks()  # Start the timer

    def run(self):
        self.handle_events()  # Handle events first
        self.main_page()      # Then display the main page
        self.clock.tick(60)

    def draw_graph(self):
        # Dessine le graphique de la balance
        balance = self.user.get_balance()
        # Normalise la balance pour qu'elle soit entre 0 et 1000
        normalized_balance = min(max(balance / 2000, 0), 1)
        # Dessine le rectangle du graphique
        pygame.draw.rect(self.screen, self.BLUE, (100, 200, 600, 20))
        # Dessine le rectangle rempli pour la balance
        pygame.draw.rect(self.screen, self.GREEN, (100, 200, normalized_balance * 600, 20))

# Exemple d'utilisation de la classe PieChart
if __name__ == "__main__":
    
    user = ...  

    main_page = MainPage(user)
    main_page.run()
