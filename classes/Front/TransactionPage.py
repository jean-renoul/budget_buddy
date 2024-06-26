from classes.Front.MainPage import MainPage  # Import MainPage class from the Front package
import pygame  # Import the pygame library
import sys  # Import the sys module

class TransactionPage(MainPage):
    def __init__(self, user):
        super().__init__(user)  # Call the __init__() method of the superclass (MainPage)
        self.menu_transactions = True  # Initialize the menu_transactions attribute to True

    def display_transactions(self):
        # Clear the screen
        self.screen.blit(self.background_image, (0, 0))
        
        # Display the "Transactions" text
        transaction_text = self.font.render("Transactions", True, self.BLACK)
        self.screen.blit(transaction_text, (self.screen_width/2 - transaction_text.get_width()/2, 100))

        # Draw separator lines
        pygame.draw.rect(self.screen, self.BLACK, (self.screen_width/2 - 200, 120, 400, 2))
        pygame.draw.rect(self.screen, self.COLOR2, (self.screen_width/2 - 300, 125, self.screen_width/2 + 200, 225))
        pygame.draw.rect(self.screen, self.COLOR1, (self.screen_width/2 - 100, 125 + 225, 200, 160))

        # Display transactions
        visible_transactions = self.transactions[self.scroll_offset:self.scroll_offset+self.transactions_per_page]

        for i, transaction in enumerate(visible_transactions):
            if transaction[5] == "expense" or transaction[5] == "Expense":
                transaction = f"-{transaction[2]}$ : {transaction[0]} ({transaction[1]}) ({transaction[3]}) category: {transaction[4]}"
                text = self.font.render(f"{transaction}", True, self.RED)
            elif transaction[5] == "income" or transaction[5] == "Income":
                transaction = f"+{transaction[2]}$ : {transaction[0]} ({transaction[1]}) ({transaction[3]}) category: {transaction[4]}"
                text = self.font.render(f"{transaction}", True, self.GREEN)
            self.screen.blit(text, (self.screen_width/2 - text.get_width()/2, 130 + i * 30))

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

    def display_sort_buttons(self):
        # Display sorting buttons
        for i, rect in enumerate(self.button_rects):
            pygame.draw.rect(self.screen, self.button_color, rect)
            button_text = self.button_font.render(self.button_texts[i], True, self.WHITE)
            text_rect = button_text.get_rect(center=rect.center)
            self.screen.blit(button_text, text_rect)

    def handle_events(self):
        # Handle pygame events
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
                                    self.welcome = True
                                if i == 1:
                                    self.menu_transactions = True
                                if i == 2:
                                    self.menu_transfer = True
                                if i == 3:
                                    self.menu_profile = True
                                if i == 4:
                                    pygame.quit()
                                    sys.exit()

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
        self.display_transactions()  # Display transactions
        self.handle_events()  # Handle events
        self.clock.tick(60)  # Cap the frame rate at 60 FPS