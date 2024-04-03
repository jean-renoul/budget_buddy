import pygame
import sys
from classes.Front.MainPage import MainPage

class BankProfile(MainPage):
    def __init__(self, user):
        super().__init__(user)
        self.rib = "1234567890"

        # Initialize Pygame
        pygame.init()

        # Screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Profil Bancaire")

        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 128, 0)
        self.LIGHT_BROWN = (237, 190, 164)
        self.LIGHT_BLUE = (154, 208, 211)

        # Font
        self.font = pygame.font.Font(None, 24)

        # Load profile image
        self.profile_picture = pygame.image.load("images/4274186-person-icon-user-interface-icon-silhouette-of-man-simple-symbol-a-glyph-symbol-in-your-web-site-design-logo-app-ui-webinar-video-chat-ect-vectoriel.jpg")
        # Resize profile image
        self.profile_picture = pygame.transform.scale(self.profile_picture, (100, 100))
        self.show_change_password_fields = False
        self.active_field = None
        self.old_password = ""
        self.new_password = ""
        self.profile_rect = pygame.Rect(50, 250, 150, 150)
        self.old_password_input_rect = pygame.Rect(self.profile_rect.left, self.profile_rect.bottom + 70, 150, 30)
        self.new_password_input_rect = pygame.Rect(self.profile_rect.left, self.profile_rect.bottom + 110, 150, 30)
        self.submit_button = pygame.Rect(self.profile_rect.left, self.profile_rect.bottom + 150, 150, 40)
        self.password_modification = False

    def draw_text(self, text, x, y):
        # Draw text on the screen
        text_surface = self.font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def draw_button(self, x, y, width, height, color, text):
        # Draw a button on the screen
        button_rect = pygame.Rect(x, y, width, height)  # Create a rectangle for the button
        pygame.draw.rect(self.screen, color, button_rect)
        self.draw_text(text, x + width // 2, y + height // 2)
        return button_rect  # Return the button rectangle for click detection

    def display_profile(self):
        # Display user profile
        self.screen.blit(self.background_image, (0, 0))

        self.display_menu()
        if self.menu_open == True:
            self.display_open_menu()

        # Profile image frame
        pygame.draw.rect(self.screen, self.LIGHT_BROWN, self.profile_rect)
        pygame.draw.rect(self.screen, self.BLACK, self.profile_rect, 2)
        # Center the image in the frame
        profile_image_rect = self.profile_picture.get_rect(center=self.profile_rect.center)
        self.screen.blit(self.profile_picture, profile_image_rect)

        # Information frame
        info_rect = pygame.Rect(250, 100, 480, 450)
        pygame.draw.rect(self.screen, self.LIGHT_BROWN, info_rect)
        pygame.draw.rect(self.screen, self.BLACK, info_rect, 2)
        self.draw_text(f"Email: {self.user.email}", 490, 120)
        self.draw_text(f"Last-name: {self.user.last_name}", 490, 220)
        self.draw_text(f"First-name: {self.user.first_name}", 490, 320)
        self.draw_text(f"RIB: {self.rib}", 490, 420)

        # Draw the Change Password button and get its rectangle
        self.button_rect = self.draw_button(self.profile_rect.left, self.profile_rect.bottom + 20, 150, 40, self.LIGHT_BROWN, "Change Password")

        if self.show_change_password_fields:
            # Draw old password input box
            pygame.draw.rect(self.screen, self.LIGHT_BLUE, self.old_password_input_rect)
            if self.active_field == "Old Password" or self.old_password != "":
                self.old_password_text = self.font.render(self.old_password, True, self.BLACK)
            else:
                self.old_password_text = self.font.render("Old Password", True, self.BLACK)
            self.screen.blit(self.old_password_text, (self.old_password_input_rect.left + 5, self.old_password_input_rect.top + 5))

            # Draw new password input box
            pygame.draw.rect(self.screen, self.LIGHT_BLUE, self.new_password_input_rect)
            if self.active_field == "New Password" or self.new_password != "":
                self.new_password_text = self.font.render(self.new_password, True, self.BLACK)
            else:
                self.new_password_text = self.font.render("New Password", True, self.BLACK)
            self.screen.blit(self.new_password_text, (self.new_password_input_rect.left + 5, self.new_password_input_rect.top + 5))

            # Draw the Submit button
            pygame.draw.rect(self.screen, self.GREY, self.submit_button)
            self.draw_text("Submit", self.submit_button.left + self.submit_button.width // 2, self.submit_button.top + self.submit_button.height // 2)

        if self.message_text:
            self.screen.blit(self.message_text, (self.profile_rect.left, self.profile_rect.bottom + 70, 150, 30))
            # Check if the duration has elapsed
            if pygame.time.get_ticks() - self.message_timer >= self.message_duration:
                self.message_text = None  # Clear the error message

        pygame.display.flip()

    def run(self):
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
                                if i == 1:  # If the first option is clicked
                                    self.menu_transactions = True
                                if i == 2:
                                    self.menu_transfer = True
                                if i == 4:
                                    pygame.quit()
                                    sys.exit()

                    if self.button_rect.collidepoint(event.pos):  # Check if the click is inside the button rectangle
                        self.show_change_password_fields = not self.show_change_password_fields

                    # Check if the password fields are clicked
                    if self.old_password_input_rect.collidepoint(event.pos) and self.show_change_password_fields:
                        self.active_field = "Old Password"
                    elif self.new_password_input_rect.collidepoint(event.pos) and self.show_change_password_fields:
                        self.active_field = "New Password"
                    else:
                        self.active_field = None

                    # Check if the Submit button is clicked
                    if self.show_change_password_fields and self.submit_button.collidepoint(event.pos):
                        self.password_modification = True
                        self.show_change_password_fields = False
                        self.active_field = None

            elif event.type == pygame.KEYDOWN and self.active_field:
                if event.key == pygame.K_BACKSPACE:
                    if self.active_field == "Old Password":
                        self.old_password = self.old_password[:-1]
                    elif self.active_field == "New Password":
                        self.new_password = self.new_password[:-1]
                else:
                    if self.active_field == "Old Password":
                        self.old_password += event.unicode
                    elif self.active_field == "New Password":
                        self.new_password += event.unicode
            self.display_profile()


# Example of usage
if __name__ == "__main__":
    profile = BankProfile("example@mail.com", "Doe", "John", "1234567890")
    profile.run()