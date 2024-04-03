import pygame
import sys

class Registration:
    def __init__(self):
        # Screen parameters
        self.screen_width = 600
        self.screen_height = 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Load background image
        self.background_image = pygame.image.load('images/inscription.png')
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (154, 208, 211)  # Button color
        self.BUTTON_TEXT_COLOR = self.BLACK  # Button text color
        self.TEXT_INPUT_COLOR = (237, 190, 164)  # Text input box color
        self.TEXT_INPUT_BORDER_COLOR = (232, 143, 122)  # Text input box border color
        self.TEXT_INPUT_BORDER_WIDTH = 2  # Text input box border width

        # Font
        self.font = pygame.font.Font(None, 20)  # Using the Bobby Jones font

        # Initialize form data, active field, text input status, cursor timer, and vertical offset
        self.form_data = {"Lastname": "", "Firstname": "", "Email": "", "Password": "", "Confirm Password": ""}
        self.active_field = None
        self.text_input = {name: False for name in self.form_data.keys()}
        self.cursor_timer = 0
        self.input_box_offset_y = 30  # Vertical offset of text input boxes
        self.message_text = None  # Track the error message text
        self.message_timer = 0     # Timer to control the duration of error message display
        self.message_duration = 2000  # Duration to display the error message in milliseconds
        self.clock = pygame.time.Clock()
        self.back_to_login = False
        self.registration_attempt = False

    def render(self):
        # Display the background image
        self.screen.blit(self.background_image, (0, 0))

        # Draw form input fields
        for i, (name, text) in enumerate(self.form_data.items()):
            background = self.TEXT_INPUT_COLOR if self.active_field == name else self.WHITE
            input_box = pygame.Rect(self.screen_width // 2 - 200, 300 + i * 50 + self.input_box_offset_y, 400, 40)
            pygame.draw.rect(self.screen, background, input_box, border_radius=10)  # Add border radius
            pygame.draw.rect(self.screen, self.TEXT_INPUT_BORDER_COLOR, input_box, self.TEXT_INPUT_BORDER_WIDTH, border_radius=10)  # Draw text input box border

            if text == "" and not self.text_input[name]:
                text_surface = self.font.render(f"{name}: ", True, self.BLACK)
                self.screen.blit(text_surface, (input_box.left + 10, input_box.centery - text_surface.get_height() // 2))
            else:
                if name == "Password" or name == "Confirm Password":
                    # Render "*" characters instead of the actual password
                    masked_text = "*" * len(text)
                    text_surface = self.font.render(masked_text, True, self.BLACK)
                else:
                    text_surface = self.font.render(f"{text}", True, self.BLACK)
                self.screen.blit(text_surface, (input_box.left + 10, input_box.centery - text_surface.get_height() // 2))

            # Draw the cursor
            if self.active_field == name and self.cursor_timer % 60 < 30:
                cursor_rect = pygame.Rect(input_box.left + 10 + text_surface.get_width(), input_box.centery - self.font.get_height() // 2, 2, self.font.get_height())
                pygame.draw.rect(self.screen, self.BLACK, cursor_rect)

            if self.message_text:
                self.screen.blit(self.message_text, (self.screen_width // 2 - self.message_text.get_width() // 2, 670))
                # Check if the duration has elapsed
                if pygame.time.get_ticks() - self.message_timer >= self.message_duration:
                    self.message_text = None  # Clear the error message

        # Draw buttons
        button_width = 150
        button_height = 50
        button_x = (self.screen_width - 2 * button_width - 20) // 2
        pygame.draw.rect(self.screen, self.GREEN, (button_x, self.screen_height - 100, button_width, button_height), border_radius=10)
        pygame.draw.rect(self.screen, self.GREEN, (button_x + button_width + 20, self.screen_height - 100, button_width, button_height), border_radius=10)

        # Button text
        create_account_text = self.font.render("Inscription", True, self.BUTTON_TEXT_COLOR)
        return_text = self.font.render("Retour", True, self.BUTTON_TEXT_COLOR)
        self.screen.blit(create_account_text, (button_x + (button_width - create_account_text.get_width()) // 2, self.screen_height - 100 + (button_height - create_account_text.get_height()) // 2))
        self.screen.blit(return_text, (button_x + button_width + 20 + (button_width - return_text.get_width()) // 2, self.screen_height - 100 + (button_height - return_text.get_height()) // 2))

    def handle_events(self):
        # Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.check_click(event.pos)
            elif event.type == pygame.KEYDOWN and self.active_field:
                if event.key == pygame.K_BACKSPACE:
                    self.form_data[self.active_field] = self.form_data[self.active_field][:-1]
                else:
                    self.form_data[self.active_field] += event.unicode
                    self.text_input[self.active_field] = True

    def check_click(self, position):
        # Check if buttons are clicked
        button_width = 150
        button_height = 50
        button_x = (self.screen_width - 2 * button_width - 20) // 2

        create_account_rect = pygame.Rect(button_x, self.screen_height - 100, button_width, button_height)
        return_rect = pygame.Rect(button_x + button_width + 20, self.screen_height - 100, button_width, button_height)

        if create_account_rect.collidepoint(position):
            if self.form_data["Password"] != self.form_data["Confirm Password"]:
                self.message("Passwords do not match")
            else:
                self.registration_attempt = True
        elif return_rect.collidepoint(position):
            self.back_to_login = True
        else:
            # Check if form fields are clicked
            for name in self.form_data.keys():
                field_rect = pygame.Rect(self.screen_width // 2 - 200, 300 + list(self.form_data.keys()).index(name) * 50 + self.input_box_offset_y, 400, 40)
                if field_rect.collidepoint(position):
                    self.active_field = name
                    if not self.text_input[name]:
                        self.form_data[name] = ""
                    return
            self.active_field = None

    def message(self, message):
        self.message_text = self.font.render(message, True, self.BLACK)
        self.message_timer = pygame.time.get_ticks()  # Start the timer

    def run(self):
        # Main loop
        self.handle_events()
        self.render()
        pygame.display.flip()
        self.clock.tick(60)
        self.cursor_timer += 1