import pygame
import sys

class Login:
    def __init__(self):
        # Initialize form data, active field, text input status, cursor timer, and vertical offset
        self.form_data = {"Lastname": "", "Firstname": "", "Email": "", "Password": ""}
        self.active_field = None  # Track currently active text input field
        self.text_input = {name: False for name in self.form_data.keys()}  # Track whether text input is occurring in each field
        self.cursor_timer = 0  # Timer for cursor blinking animation
        self.y_offset = 150  # Additional offset for positioning elements slightly higher

        # Screen parameters
        self.screen_width = 500
        self.screen_height = 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Load background image
        self.background_image = pygame.image.load("images/Login.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))

        # Colors
        self.WHITE = (237, 190, 164)  # Color of text boxes before click
        self.BLACK = (0, 0, 0)
        self.GREY = (200, 200, 200)
        self.WHITE_GREY = (220, 220, 220)
        self.BUTTON_COLOR = (154, 208, 211)  # Color of buttons
        self.BUTTON_TEXT_COLOR = self.BLACK
        # Font
        self.font = pygame.font.Font(None, 16)

        # Calculate the vertical position of the last input box
        last_input_box_y = self.y_offset + 200 + (len(self.form_data) - 1) * 50

        # Coordinates of login and registration buttons
        self.connexion_button = pygame.Rect(self.screen_width // 2 + 50, last_input_box_y + 50, 200, 40)  # Connexion Button
        self.inscription_button = pygame.Rect(self.screen_width // 2 - 250, last_input_box_y + 50, 200, 40)  # Registration Button         
        self.message_text = None  # Track the error message text
        self.message_timer = 0     # Timer to control the duration of error message display
        self.message_duration = 2000  # Duration to display the error message in milliseconds
        self.login_attempt = False  # Flag for attempting login
        self.register = False  # Flag for attempting registration
        self.clock = pygame.time.Clock()

    def render(self):
        # Draw the background image
        self.screen.blit(self.background_image, (0, 0))

        # Render form input fields and labels
        for i, (name, text) in enumerate(self.form_data.items()):
            background = self.WHITE if self.active_field == name else self.GREY  # Highlight the active field
            input_box = pygame.Rect(self.screen_width // 2 - 200, self.y_offset + 200 + i * 50, 400, 40)  # Use the offset
            pygame.draw.rect(self.screen, background, input_box, border_radius=10)  # Rounded corners
            if text == "" and not self.text_input[name]:
                text_surface = self.font.render(f"{name}: ", True, self.BLACK)
            else:
                if name == "Password":
                    masked_text = "*" * len(text)  # Mask the password text with "*"
                    text_surface = self.font.render(masked_text, True, self.BLACK)
                else:
                    text_surface = self.font.render(f"{text}", True, self.BLACK)
                
            self.screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
            
            # Render cursor if the field is active and blinking
            if self.active_field == name and self.cursor_timer % 60 < 30:
                if name == "Password" and text != "":
                    cursor_rect = pygame.Rect(input_box.x + self.font.size(masked_text)[0] + 5, input_box.y + 5, 2, self.font.get_height())
                    pygame.draw.rect(self.screen, self.BLACK, cursor_rect)
                else:
                    cursor_rect = pygame.Rect(input_box.x + self.font.size(text)[0] + 5, input_box.y + 5, 2, self.font.get_height())
                    pygame.draw.rect(self.screen, self.BLACK, cursor_rect)
            # Add border if the field is active
            if self.active_field == name:
                pygame.draw.rect(self.screen, self.BUTTON_COLOR, input_box, 2)

        # Display login and registration buttons with visual effects
        pygame.draw.rect(self.screen, self.BUTTON_COLOR, self.connexion_button, border_radius=5)  # Connexion Button
        pygame.draw.rect(self.screen, self.BUTTON_COLOR, self.inscription_button, border_radius=5)  # Registration Button
        conn_text = self.font.render("Connexion", True, self.BUTTON_TEXT_COLOR)
        self.screen.blit(conn_text, (self.connexion_button.x + 50, self.connexion_button.y + 10))
        insc_text = self.font.render("Inscription", True, self.BUTTON_TEXT_COLOR)
        self.screen.blit(insc_text, (self.inscription_button.x + 50, self.inscription_button.y + 10))
        if self.message_text:
            self.screen.blit(self.message_text, (self.screen_width // 2 - self.message_text.get_width() // 2, 600))
            # Check if the duration has elapsed
            if pygame.time.get_ticks() - self.message_timer >= self.message_duration:
                self.message_text = None  # Clear the error message

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
                    # Remove the last character if backspace is pressed
                    self.form_data[self.active_field] = self.form_data[self.active_field][:-1]
                else:
                    # Add typed character to the active field
                    self.form_data[self.active_field] += event.unicode
                    self.text_input[self.active_field] = True

    def check_click(self, position):
        # Check if the user clicks on a field or button
        for name in self.form_data.keys():
            field_rect = pygame.Rect(self.screen_width // 2 - 200, self.y_offset + 200 + list(self.form_data.keys()).index(name) * 50, 400, 40)  # Use the offset
            if field_rect.collidepoint(position):
                self.active_field = name
                if not self.text_input[name]:
                    self.form_data[name] = ""
                return
        self.active_field = None
        if self.connexion_button.collidepoint(position):
            self.login_attempt = True
            print("Login")
        elif self.inscription_button.collidepoint(position):
            self.register = True
            print("Registration")
        
    def get_identifier(self):
        # Return form data
        return self.form_data
    
    def message(self, message):
        # Display error message
        self.message_text = self.font.render(message, True, self.BLACK)
        self.message_timer = pygame.time.get_ticks()  # Start the timer

    def run(self):
        # Main loop
        self.handle_events()
        self.render()
        pygame.display.flip()
        self.clock.tick(60)
        self.cursor_timer += 1