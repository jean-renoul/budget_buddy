import pygame
import sys
from classes.Front.MainPage import MainPage

class BankProfile(MainPage):
    def __init__(self,user):
        super().__init__(user)
        self.rib = "1234567890"

        # Initialisation de Pygame
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Profil Bancaire")

        # Couleurs
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 128, 0)
        self.LIGHT_BROWN = (237, 190, 164)
        self.LIGHT_BLUE = (154, 208, 211)

        # Police de caractères
        self.font = pygame.font.Font(None, 24)

        # Chargement de l'image de profil
        self.profile_picture = pygame.image.load("images/4274186-person-icon-user-interface-icon-silhouette-of-man-simple-symbol-a-glyph-symbol-in-your-web-site-design-logo-app-ui-webinar-video-chat-ect-vectoriel.jpg")
        # Ajuster la taille du cadre en fonction de la taille de l'image
        self.profile_picture = pygame.transform.scale(self.profile_picture, (100, 100))
        self.show_change_password_fields = False
        self.active_field = None
        self.old_password = ""
        self.new_password = ""

    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def draw_button(self, x, y, width, height, color, text):
        button_rect = pygame.Rect(x, y, width, height)  # Créer un rectangle pour le bouton
        pygame.draw.rect(self.screen, color, button_rect)
        self.draw_text(text, x + width // 2, y + height // 2)
        return button_rect  # Retourner le rectangle du bouton pour la détection de clic

    def display_profile(self):
        self.screen.blit(self.background_image, (0, 0))

        self.display_menu()
        if self.menu_open == True:
            self.display_open_menu()

        # Cadre pour l'image de profil
        profile_rect = pygame.Rect(50, 250, 150, 150)
        pygame.draw.rect(self.screen, self.LIGHT_BROWN, profile_rect)
        pygame.draw.rect(self.screen, self.BLACK, profile_rect, 2)
        # Centrer l'image dans le cadre
        profile_image_rect = self.profile_picture.get_rect(center=profile_rect.center)
        self.screen.blit(self.profile_picture, profile_image_rect)

        # Cadre pour les informations
        info_rect = pygame.Rect(250, 100, 480, 450)
        pygame.draw.rect(self.screen, self.LIGHT_BROWN, info_rect)
        pygame.draw.rect(self.screen, self.BLACK, info_rect, 2)
        self.draw_text(f"Email: {self.user.email}", 490, 120)
        self.draw_text(f"Last-name: {self.user.last_name}", 490, 220)
        self.draw_text(f"First-name: {self.user.first_name}", 490, 320)
        self.draw_text(f"RIB: {self.rib}", 490, 420)

        # Dessiner le bouton Changer de Mot de Passe et obtenir son rectangle
        self.button_rect = self.draw_button(profile_rect.left, profile_rect.bottom + 20, 150, 40, self.LIGHT_BROWN, "Change Password")

        if self.show_change_password_fields:
            # Draw old password input box
            self.old_password_input_rect = pygame.Rect(profile_rect.left, profile_rect.bottom + 70, 150, 30)
            pygame.draw.rect(self.screen, self.LIGHT_BLUE, self.old_password_input_rect)
            self.old_password_text = self.font.render("Old Password", True, self.BLACK)
            self.screen.blit(self.old_password_text, (self.old_password_input_rect.left + 5, self.old_password_input_rect.top + 5))

            # Draw new password input box
            self.new_password_input_rect = pygame.Rect(profile_rect.left, profile_rect.bottom + 110, 150, 30)
            pygame.draw.rect(self.screen, self.LIGHT_BLUE, self.new_password_input_rect)
            self.new_password_text = self.font.render("New Password", True, self.BLACK)
            self.screen.blit(self.new_password_text, (self.new_password_input_rect.left + 5, self.new_password_input_rect.top + 5))

        pygame.display.flip()

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Si le clic est le bouton gauche de la souris
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
                                    self.welcome = False
                                if i == 2:
                                    self.menu_transfer = True
                                    self.menu_open = False
                                    self.menu_transactions = False
                                    self.welcome = False

                    if self.button_rect.collidepoint(event.pos):  # Vérifier si le clic est dans le rectangle du bouton
                        print("Clic sur le bouton Changer de Mot de Passe")  # Implémenter ici la logique de changement de mot de passe
                        self.show_change_password_fields = not self.show_change_password_fields

                    if self.show_change_password_fields:
                        # Vérifier si les champs de mot de passe sont cliqués
                        if self.old_password_input_rect.collidepoint(event.pos):
                            self.active_field = "Old Password"
                        elif self.new_password_input_rect.collidepoint(event.pos):
                            self.active_field = "New Password"
                        else:
                            self.active_field = None
            self.display_profile()


# Exemple d'utilisation
if __name__ == "__main__":
    profile = BankProfile("example@mail.com", "Doe", "John", "1234567890")
    profile.run()
