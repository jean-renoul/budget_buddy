from classes.Front.MainPage import MainPage  # Import MainPage class from the Front package
import pygame  # Import the pygame library
import sys  # Import the sys module

class TransferPage(MainPage):
    def __init__(self, user):
        super().__init__(user)  # Call the __init__() method of the superclass (MainPage)
        self.menu_transfer = True  # Initialize the menu_transfer attribute to True

    def transfer_page(self):
        # Display transfer page elements
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
        for name, value in self.transfer_data.items():
            input_text = self.font.render(value, True, self.BLACK)
            input_rect = pygame.Rect(350, 200 + list(self.transfer_data.keys()).index(name) * 50, 200, 30)
            pygame.draw.rect(self.screen, self.COLOR2, input_rect)  # Input box
            self.screen.blit(input_text, (input_rect.x + 5, input_rect.y + 5))

        # Display the send button
        pygame.draw.rect(self.screen, self.COLOR2, self.send_button)
        send_text = self.font.render("Send", True, self.BLACK)
        self.screen.blit(send_text, (self.send_button.x + 10, self.send_button.y + 10))

        # Display error message if present
        if self.message_text:
            self.screen.blit(self.message_text, (self.screen_width // 2 - self.message_text.get_width() // 2, 450))
            # Check if the duration has elapsed
            if pygame.time.get_ticks() - self.message_timer >= self.message_duration:
                self.message_text = None  # Clear the error message

        # Update the display
        pygame.display.flip()

    def check_input_boxes(self, position):
        # Check if any input box is clicked, and set it as the active field
        for name in self.transfer_data.keys():
            input_box_rect = pygame.Rect(350, 200 + list(self.transfer_data.keys()).index(name) * 50, 200, 30)
            if input_box_rect.collidepoint(position):
                self.active_field = name
                if not self.text_input[name]:
                    self.transfer_data[name] = ""
                return
        # If no input box is clicked, deactivate the active field
        self.active_field = None

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

                    if self.menu_transfer == True:
                        self.check_input_boxes(event.pos)
                        if self.send_button.collidepoint(event.pos):

                            for data in self.transfer_data.values():
                                if data == "":
                                    self.message("Please fill in all fields")
                                    break
                                elif self.transfer_data['amount'].isdigit() == False:
                                    self.message("Amount must be a number")
                                    break
                                elif self.transfer_data['type'] not in ['income', 'expense']:
                                    self.message("Type must be either 'income' or 'expense'")
                                    break
                                else:                                
                                    # Send the transaction data to the server
                                    self.add_transaction = True

            elif event.type == pygame.KEYDOWN and self.active_field:
                # If an input box is active and a key is pressed, update the corresponding field in transfer_data
                if event.key == pygame.K_BACKSPACE:
                    self.transfer_data[self.active_field] = self.transfer_data[self.active_field][:-1]
                else:
                    self.transfer_data[self.active_field] += event.unicode
                    self.text_input[self.active_field] = True

    def run(self):
        self.handle_events()  # Handle events
        self.transfer_page()  # Display the transfer page