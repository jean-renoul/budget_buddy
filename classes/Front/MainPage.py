# Import necessary libraries
import pygame
import sys
import math
import random
from classes.Back.Db import Db
from classes.Back.PieChart import PieChart
from classes.Back.diagramme import Diagram

# Define the MainPage class
class MainPage:
    # Constructor method
    def __init__(self, user):
        # Initialize user and transactions attributes
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
        # Welcome text
        self.welcome_text = self.font.render("Budget Buddy", True, self.BLACK)
        self.welcome_text_rect = self.welcome_text.get_rect(center=(self.screen_width // 2, 50))

        # Load and resize menu logo image
        self.menu_logo = pygame.image.load("images/menu_icon.png")  
        self.menu_logo = pygame.transform.scale(self.menu_logo, (40, 50)) 
        self.menu_logo_rect = self.menu_logo.get_rect(x=20, y=20)

        # Load and resize background image
        self.background_image = pygame.image.load("images/MainPage.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))
        
        # Set up rectangle for diagram button
        self.diagram_button_rect = pygame.Rect(50, 400, 200, 50)
        self.diagram_button_rect.x = self.diagram_button_rect.right + 20

        # Define menu options
        self.menu_options = [
            "Main page",
            "Display transactions",
            "Transfer money",
            "Settings",
            "Quitter"
        ]

        # Initialize list to store menu option rectangles
        self.menu_option_rects = []

        # Set initial position and dimensions for dropdown menu
        self.MENU_START_X, self.MENU_START_Y = 20, 70
        self.MENU_WIDTH, self.MENU_HEIGHT = 200, 40
        self.MENU_SPACING = 40

        # Flags to track various states of the application
        self.welcome = False
        self.menu_open = False
        self.menu_transactions = False
        self.menu_transfer = False
        self.sort_by_amount = False
        self.sort_by_date = False
        self.sort_by_type = False
        self.sort_by_category = False
        self.add_transaction = False
        self.menu_profile = False
        self.message_text = None  # Track the error message text
        self.message_timer = 0     # Timer to control the duration of error message display
        self.message_duration = 2000  # Duration to display the error message in milliseconds

        # Set up button properties
        self.BUTTON_WIDTH, self.BUTTON_HEIGHT = 120, 30
        self.button_font = pygame.font.Font(None, 20)
        self.button_color = self.COLOR2
        self.button_hover_color = self.GREEN
        self.button_texts = ["Sort by Date", "Sort by Amount", "Sort by Type", "Sort by Category"]
        self.button_rects = []
        self.transfer_data = {"name": "", "description": "", "category": "", "amount": "", "type": ""}
        self.active_field = None
        self.text_input = {name: False for name in self.transfer_data.keys()}
        self.send_button = pygame.Rect(350, 500, 60, 50)

        # Create sort buttons
        self.create_sort_buttons()
        
        # Initialize PieChart instance
        self.pie_chart = PieChart(self.user.id)

        # Set up button for displaying pie chart
        self.pie_chart_button_rect = pygame.Rect(50, 300, 150, 50)
        self.diagram_button_rect = pygame.Rect(600, 300, 150, 50)

    # Method to display the main page
    def main_page(self):
        self.screen.blit(self.background_image, (0, 0))
        self.display_menu()
        if self.menu_open == True:
            self.display_open_menu()

        balance_text = self.font.render(f"Balance: {self.user.get_balance()}$", True, self.BLACK)
        balance_text_rect = balance_text.get_rect(center=(self.screen_width // 2, 150))
        self.screen.blit(balance_text, balance_text_rect)
        balance_frame_rect = pygame.Rect(200, 130, 400, 50) 
        pygame.draw.rect(self.screen, self.COLOR1, balance_frame_rect, 2)
        
        pygame.draw.rect(self.screen, self.COLOR2, self.diagram_button_rect)
        diagram_button_text = self.font.render("Show Diagram", True, self.BLACK)
        diagram_button_text_rect = diagram_button_text.get_rect(center=self.diagram_button_rect.center)
        self.screen.blit(diagram_button_text, diagram_button_text_rect)

        self.draw_graph()
        self.draw_pie_chart_button()

        pygame.display.flip()

    # Method to display the transfer page
    def transfer_page(self):
        self.screen.blit(self.background_image, (0, 0))
        self.display_menu()
        if self.menu_open == True:
            self.display_open_menu()

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

        name_input_text = self.font.render(self.transfer_data.get('name', ''), True, self.BLACK)
        pygame.draw.rect(self.screen, self.COLOR2, (350, 200, 200, 30))  
        self.screen.blit(name_input_text, (355, 205))

        description_input_text = self.font.render(self.transfer_data.get('description', ''), True, self.BLACK)
        pygame.draw.rect(self.screen, self.COLOR2, (350, 250, 200, 30))  
        self.screen.blit(description_input_text, (355, 255))

        category_input_text = self.font.render(self.transfer_data.get('category', ''), True, self.BLACK)
        pygame.draw.rect(self.screen, self.COLOR2, (350, 300, 200, 30))  
        self.screen.blit(category_input_text, (355, 305))

        amount_input_text = self.font.render(str(self.transfer_data.get('amount', '')), True, self.BLACK)
        pygame.draw.rect(self.screen, self.COLOR2, (350, 350, 200, 30))  
        self.screen.blit(amount_input_text, (355, 355))

        type_input_text = self.font.render(self.transfer_data.get('type', ''), True, self.BLACK)
        pygame.draw.rect(self.screen, self.COLOR2, (350, 400, 200, 30))  
        self.screen.blit(type_input_text, (355, 405))

        for name, value in self.transfer_data.items():
            input_text = self.font.render(value, True, self.BLACK)
            input_rect = pygame.Rect(350, 200 + list(self.transfer_data.keys()).index(name) * 50, 200, 30)
            pygame.draw.rect(self.screen, self.COLOR2, input_rect)  
            self.screen.blit(input_text, (input_rect.x + 5, input_rect.y + 5))

        pygame.draw.rect(self.screen, self.COLOR2, self.send_button)
        send_text = self.font.render("Send", True, self.BLACK)
        self.screen.blit(send_text, (self.send_button.x + 10, self.send_button.y + 10))
        
        pygame.display.flip()

    # Method to check input boxes for mouse clicks
    def check_input_boxes(self, position):
        for name in self.transfer_data.keys():
            input_box_rect = pygame.Rect(350, 200 + list(self.transfer_data.keys()).index(name) * 50, 200, 30)
            if input_box_rect.collidepoint(position):
                self.active_field = name
                if not self.text_input[name]:
                    self.transfer_data[name] = ""
                    return
        self.active_field = None

    # Method to create sort buttons
    def create_sort_buttons(self):
        button_start_y = 350  
        for i, text in enumerate(self.button_texts):
            button_rect = pygame.Rect((self.screen_width - self.BUTTON_WIDTH) // 2, button_start_y + i * (self.BUTTON_HEIGHT + 10), self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
            self.button_rects.append(button_rect)    

    # Method to display the menu
    def display_menu(self):
        self.screen.blit(self.welcome_text, self.welcome_text_rect)
        self.screen.blit(self.menu_logo, self.menu_logo_rect)

    # Method to display the open menu
    def display_open_menu(self):
        for i, option in enumerate(self.menu_options):
            text = self.font.render(option, True, self.BLACK)
            text_rect = text.get_rect(x=self.MENU_START_X, y=self.MENU_START_Y + i * self.MENU_SPACING)
            self.menu_option_rects.append(text_rect)
            self.screen.blit(text, text_rect)
        self.screen.blit(self.menu_logo, self.menu_logo_rect)

    # Method to handle events
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
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
                                if i == 1:  
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
                    if self.pie_chart_button_rect.collidepoint(event.pos):
                        self.display_pie_chart()
                    if self.diagram_button_rect.collidepoint(event.pos):
                        self.display_diagram()  

    # Method to display the pie chart
    def display_pie_chart(self):
        self.pie_chart.draw()

    # Method to display a message
    def message(self, message):
        self.message_text = self.font.render(message, True, self.BLACK)
        self.message_timer = pygame.time.get_ticks()  

    # Method to run the application
    def run(self):
        self.handle_events()  
        self.main_page()      
        self.clock.tick(60)

    # Method to draw the graph
    def draw_graph(self):
        balance = self.user.get_balance()
        normalized_balance = min(max(balance / 2000, 0), 1)
        pygame.draw.rect(self.screen, self.COLOR2, (100, 200, 600, 20))
        pygame.draw.rect(self.screen, self.COLOR1, (100, 200, normalized_balance * 600, 20))

    # Method to draw the pie chart button
    def draw_pie_chart_button(self):
        pygame.draw.rect(self.screen, self.COLOR1, self.pie_chart_button_rect)
        button_text = self.font.render("Display Pie Chart", True, self.BLACK)
        button_text_rect = button_text.get_rect(center=self.pie_chart_button_rect.center)
        self.screen.blit(button_text, button_text_rect)

    # Method to display the diagram
    def display_diagram(self):
        diagram = Diagram(self.user.id)
        diagram.fetch_transactions()
        diagram.calculate_sums()
        diagram.draw_diagram()

# Entry point of the program
if __name__ == "__main__":
    user = ...  # Initialize user object

    main_page = MainPage(user)
    main_page.run()
