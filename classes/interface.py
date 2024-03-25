import pygame
import sys

pygame.init()

# Paramètres de l'écran
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Charger l'image de fond
background_image = pygame.image.load("image/bg.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
LIGHT_GREY = (220, 220, 220)
GREEN = (0, 255, 0)

# Police de caractère
font = pygame.font.SysFont("calibri", 16)

class Interface:
    def __init__(self):
        self.form_data = {"Lastname": "", "Firstname": "", "Email": "", "Password": ""}
        self.active_field = None
        self.text_input = {name: False for name in self.form_data.keys()}
        self.cursor_timer = 0
        self.connexion_button = pygame.Rect(screen_width // 2 - 150, 470, 100, 40)
        self.inscription_button = pygame.Rect(screen_width // 2 + 50, 470, 100, 40)

    def render(self):
        # Afficher l'image de fond
        screen.blit(background_image, (0, 0))

        for i, (name, text) in enumerate(self.form_data.items()):
            background = WHITE if self.active_field == name else GREY
            input_box = pygame.Rect(screen_width // 2 - 180, 270 + i * 50, 360, 30)
            pygame.draw.rect(screen, background, input_box, border_radius=5)
            if text == "" and not self.text_input[name]:
                text_surface = font.render(f"{name.capitalize()}: ", True, BLACK)
            else:
                text_surface = font.render(f"{text}", True, BLACK)
            screen.blit(text_surface, (input_box.x + 10, input_box.y + 5))
            if self.active_field == name and self.cursor_timer % 60 < 30:
                cursor_rect = pygame.Rect(input_box.x + font.size(text)[0] + 10, input_box.y + 5, 2, font.get_height())
                pygame.draw.rect(screen, BLACK, cursor_rect)
        pygame.draw.rect(screen, GREEN, self.connexion_button, border_radius=5)
        pygame.draw.rect(screen, GREEN, self.inscription_button, border_radius=5)
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
            field_rect = pygame.Rect(screen_width // 2 - 180, 270 + list(self.form_data.keys()).index(name) * 50, 360, 30)
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

    @staticmethod
    def create_instance():
        return Interface()

if __name__ == "__main__":
    Interface().run()
