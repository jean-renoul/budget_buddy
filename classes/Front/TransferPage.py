from classes.Front.MainPage import MainPage
import pygame
import sys

class TransferPage(MainPage):
    def __init__(self, user):
        super().__init__(user)
        self.menu_transfer = True

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

        for name, value in self.transfer_data.items():
            input_text = self.font.render(value, True, self.BLACK)
            input_rect = pygame.Rect(350, 200 + list(self.transfer_data.keys()).index(name) * 50, 200, 30)
            pygame.draw.rect(self.screen, self.COLOR2, input_rect)  # Input box
            self.screen.blit(input_text, (input_rect.x + 5, input_rect.y + 5))

        pygame.draw.rect(self.screen, self.COLOR2, self.send_button)
        send_text = self.font.render("Send", True, self.BLACK)
        self.screen.blit(send_text, (self.send_button.x + 10, self.send_button.y + 10))

        if self.message_text:
            self.screen.blit(self.message_text, (self.screen_width // 2 - self.message_text.get_width() // 2, 450))
            # Check if the duration has elapsed
            if pygame.time.get_ticks() - self.message_timer >= self.message_duration:
                self.message_text = None  # Clear the error message


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
                                    self.welcome = True
                                if i == 1:  # If the first option is clicked
                                    self.menu_transactions = True
                                    self.menu_open = False
                                    self.menu_transfer = False
                                if i == 2:
                                    self.menu_transfer = True
                                    self.menu_open = False
                                    self.menu_transactions = False

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
        self.handle_events()
        self.transfer_page()