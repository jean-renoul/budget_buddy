import pygame
import sys

pygame.init()

# Paramètres de l'écran
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
LIGHT_GREY = (220, 220, 220)
GREEN = (0, 255, 0)

# Police de caractère
font = pygame.font.SysFont("calibri", 14)

class Interface:
    def __init__(self):
        self.form_data = {"Nom d'utilisateur": "", "Prénom": "", "Email": "", "Mot de passe": ""}
        self.active_field = None
        self.text_input = {name: False for name in self.form_data.keys()}
        self.cursor_timer = 0
        self.frame_rect = pygame.Rect(screen_width // 2 - 250, 70, 500, 380)
        self.connexion_button = pygame.Rect(screen_width // 2 - 150, 470, 100, 40)
        self.inscription_button = pygame.Rect(screen_width // 2 + 50, 470, 100, 40)

    def render(self):
        screen.fill((0, 128, 128))  # Couleur de fond
        pygame.draw.rect(screen, GREEN, (50, 20, 700, 40))  # Cadre vert pour le titre
        title_text = font.render("Bienvenue à mon compte", True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 30))
        pygame.draw.rect(screen, WHITE, self.frame_rect, border_radius=10)  # Cadre avec bordure arrondie
        for i, (name, text) in enumerate(self.form_data.items()):
            background = WHITE if self.active_field == name else GREY
            input_box = pygame.Rect(screen_width // 2 - 200, 100 + i*50, 400, 40)
            pygame.draw.rect(screen, background, input_box)
            if text == "" and not self.text_input[name]:
                text_surface = font.render(f"{name}: ", True, BLACK)
            else:
                text_surface = font.render(f"{text}", True, BLACK)
            screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
            if self.active_field == name and self.cursor_timer % 60 < 30:
                cursor_rect = pygame.Rect(input_box.x + font.size(text)[0] + 5, input_box.y + 5, 2, font.get_height())
                pygame.draw.rect(screen, BLACK, cursor_rect)
        pygame.draw.rect(screen, GREEN, self.connexion_button)  # Bouton Connexion
        pygame.draw.rect(screen, GREEN, self.inscription_button)  # Bouton Inscription
        conn_text = font.render("Connexion", True, BLACK)
        screen.blit(conn_text, (self.connexion_button.x + 15, self.connexion_button.y + 10))
        insc_text = font.render("Inscription", True, BLACK)
        screen.blit(insc_text, (self.inscription_button.x + 15, self.inscription_button.y + 10))

    def handle_events(self):
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
        for name in self.form_data.keys():
            field_rect = pygame.Rect(screen_width // 2 - 200, 100 + list(self.form_data.keys()).index(name) * 50, 400, 40)
            if field_rect.collidepoint(position):
                self.active_field = name
                if not self.text_input[name]:
                    self.form_data[name] = ""
                return
        self.active_field = None
        if self.connexion_button.collidepoint(position):
            print("Bouton Connexion cliqué !")
        elif self.inscription_button.collidepoint(position):
            print("Bouton Inscription cliqué !")

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.handle_events()
            self.render()
            pygame.display.flip()
            clock.tick(60)
            self.cursor_timer += 1

Interface().run()
