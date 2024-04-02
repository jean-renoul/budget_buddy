import pygame
import sys

class BankProfileGUI:
    def __init__(self, email, nom, prenom, rib):
        self.email = email
        self.nom = nom
        self.prenom = prenom
        self.rib = rib

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
        self.LIGHT_BLUE =(0, 0, 0)

        # Police de caractères
        self.font = pygame.font.Font(None, 24)

        # Chargement de l'image de profil
        self.profile_picture = pygame.image.load("images/4274186-person-icon-user-interface-icon-silhouette-of-man-simple-symbol-a-glyph-symbol-in-your-web-site-design-logo-app-ui-webinar-video-chat-ect-vectoriel.jpg")
        # Ajuster la taille du cadre en fonction de la taille de l'image
        self.profile_picture = pygame.transform.scale(self.profile_picture, (150, 150))

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
        self.screen.fill(self.LIGHT_BLUE)  

        # Cadre pour l'image de profil
        profile_rect = pygame.Rect(50, 50, 150, 150)
        pygame.draw.rect(self.screen, self.LIGHT_BROWN, profile_rect)
        pygame.draw.rect(self.screen, self.BLACK, profile_rect, 2)
        # Centrer l'image dans le cadre
        profile_image_rect = self.profile_picture.get_rect(center=profile_rect.center)
        self.screen.blit(self.profile_picture, profile_image_rect)

        # Cadre pour les informations
        info_rect = pygame.Rect(220, 50, 530, 500)
        pygame.draw.rect(self.screen, self.LIGHT_BROWN, info_rect)
        pygame.draw.rect(self.screen, self.BLACK, info_rect, 2)
        self.draw_text(f"Email: {self.email}", 490, 120)
        self.draw_text(f"Nom: {self.nom}", 490, 220)
        self.draw_text(f"Prénom: {self.prenom}", 490, 320)
        self.draw_text(f"RIB: {self.rib}", 490, 420)

        # Dessiner le bouton Changer de Mot de Passe et obtenir son rectangle
        button_rect = self.draw_button(info_rect.centerx - 100, info_rect.bottom + 20, 200, 40, self.LIGHT_BROWN, "Changer de Mot de Passe")  

        pygame.display.flip()

        return button_rect

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Si le clic est le bouton gauche de la souris
                        button_rect = self.display_profile()  # Obtenir le rectangle du bouton
                        if button_rect.collidepoint(event.pos):  # Vérifier si le clic est dans le rectangle du bouton
                            print("Clic sur le bouton Changer de Mot de Passe")  # Implémenter ici la logique de changement de mot de passe
            self.display_profile()

        pygame.quit()

# Exemple d'utilisation
if __name__ == "__main__":
    profile = BankProfileGUI("example@mail.com", "Doe", "John", "1234567890")
    profile.run()
