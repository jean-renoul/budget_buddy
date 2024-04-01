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
            "Accueil",
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
        self.menu_transfer = False
        self.sort_by_amount = False
        self.sort_by_date = False
        self.sort_by_type = False
        self.sort_by_category = False

        self.BUTTON_WIDTH, self.BUTTON_HEIGHT = 120, 30
        self.button_font = pygame.font.Font(None, 20)
        self.button_color = self.BLUE
        self.button_hover_color = self.GREEN
        self.button_texts = ["Sort by Date", "Sort by Amount", "Sort by Type", "Sort by Category"]
        self.button_rects = []
        self.transfer_data = {"name": "", "description": "", "category": "", "amount": "", "type": ""}
        self.create_sort_buttons()

    def transactions_page(self):
        # Clear the screen
        self.screen.blit(self.background_image, (0, 0))
        # Display each transaction
        transaction_text = self.font.render("Transactions", True, self.BLACK)
        self.screen.blit(transaction_text, (self.screen_width/2 - transaction_text.get_width()/2, 100))

        pygame.draw.rect(self.screen, self.BLACK, (self.screen_width/2 - 200, 120, 400, 2))
        pygame.draw.rect(self.screen, self.COLOR2, (self.screen_width/2 - 300, 125, self.screen_width/2 + 200, 225))
        pygame.draw.rect(self.screen, self.COLOR1, (self.screen_width/2 - 100, 125 + 225, 200, 160))

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
        pygame.draw.rect(self.screen, self.COLOR1, (self.screen_width - 20, 130, 10, self.screen_height - 160))
        bar_position = (self.scroll_offset / len(self.transactions)) * (self.screen_height - 160)
        pygame.draw.rect(self.screen, self.COLOR2, (self.screen_width - 20, 130 + bar_position, 10, 40))

        # Display buttons
        self.display_sort_buttons()
        self.display_menu()
        if self.menu_open == True:
            self.display_open_menu()

        # Update the display
        pygame.display.flip()

    def main_page(self):
        self.screen.blit(self.background_image, (0, 0))
        self.display_menu()
        if self.menu_open == True:
            self.display_open_menu()
        pygame.display.flip()

    def transfer_page(self):
        self.screen.blit(self.background_image, (0, 0))
        self.display_menu()
        if self.menu_open == True:
            self.display_open_menu()

        # Display transfer form labels
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

        # Display input boxes
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

        pygame.display.flip()
        

    def create_sort_buttons(self):
        
        button_start_y = 350  # Adjust this value to set the starting position of buttons
        for i, text in enumerate(self.button_texts):
            button_rect = pygame.Rect((self.screen_width - self.BUTTON_WIDTH) // 2, button_start_y + i * (self.BUTTON_HEIGHT + 10), self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
            self.button_rects.append(button_rect)

    def display_sort_buttons(self):

        for i, rect in enumerate(self.button_rects):
            pygame.draw.rect(self.screen, self.button_color, rect)
            button_text = self.button_font.render(self.button_texts[i], True, self.WHITE)
            text_rect = button_text.get_rect(center=rect.center)
            self.screen.blit(button_text, text_rect)

    
        

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
                if event.button == 4:  # Scroll up
                    self.scroll_offset = max(0, self.scroll_offset - 1)
                elif event.button == 5:  # Scroll down
                    self.scroll_offset = min(len(self.transactions) - self.transactions_per_page, self.scroll_offset + 1)

                elif event.button == 1:  # Left mouse button
                    if self.menu_logo_rect.collidepoint(event.pos):
                        self.menu_open = not self.menu_open
                        
                    if self.menu_open:
                        for i, option_rect in enumerate(self.menu_option_rects):
                            if option_rect.collidepoint(event.pos):
                                if i == 0:
                                    self.menu_open = False
                                    self.menu_transactions = False
                                    self.menu_transfer = False
                                if i == 1:  # If the first option is clicked
                                    self.menu_transactions = True
                                    self.menu_open = False
                                    self.menu_transfer = False

                                if i == 2:
                                    self.menu_transfer = True
                                    self.menu_open = False
                                    self.menu_transactions = False


                    if self.menu_transactions == True:
                        for i, button_rect in enumerate(self.button_rects):
                            if button_rect.collidepoint(event.pos):
                                if i == 0:
                                    self.sort_by_date = True
                                elif i == 1:
                                    self.sort_by_amount = True
                                elif i == 2:
                                    self.sort_by_type = True
                                elif i == 3:
                                    self.sort_by_category = True



    def run(self):
        self.handle_events()
        if self.menu_transactions == True:
            self.transactions_page()
        elif self.menu_transfer == True:
            self.transfer_page()
        else:
            self.main_page()
        self.clock.tick(60)
        # Affichage du menu déroulant si ouvert
            

if __name__ == "__main__":
    main_page = MainPage()
    main_page.run()