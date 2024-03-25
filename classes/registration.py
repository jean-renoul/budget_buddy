import pygame
import sys

pygame.init()

# Paramètres de l'écran
screen_width = 700
screen_height = 650
screen = pygame.display.set_mode((screen_width, screen_height))

# Chargement de l'image de fond
background_image = pygame.image.load('image/bg.jpg')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Police de caractère
font = pygame.font.SysFont("calibri", 20)

class InscriptionPage:
    def __init__(self):
        self.form_data = {"Lastname": "", "Firstname": "", "Email": "", "Password": "", "Confirm Password": ""}
        self.active_field = None
        self.text_input = {name: False for name in self.form_data.keys()}
        self.cursor_timer = 0

    def render(self):
        # Affichage de l'image de fond
        screen.blit(background_image, (0, 0))

        # Dessiner les champs de formulaire
        for i, (name, text) in enumerate(self.form_data.items()):
            background = WHITE if self.active_field == name else GREEN
            input_box = pygame.Rect(screen_width // 2 - 200, 300 + i * 50, 400, 40)
            pygame.draw.rect(screen, background, input_box, border_radius=10)  # Border radius ajouté ici
            if text == "" and not self.text_input[name]:
                text_surface = font.render(f"{name}: ", True, BLACK)
                screen.blit(text_surface, (input_box.left + 10, input_box.centery - text_surface.get_height() // 2))
            else:
                text_surface = font.render(f"{text}", True, BLACK)
                screen.blit(text_surface, (input_box.left + 10, input_box.centery - text_surface.get_height() // 2))

            # Dessiner le curseur
            if self.active_field == name and self.cursor_timer % 60 < 30:
                cursor_rect = pygame.Rect(input_box.left + 10 + text_surface.get_width(), input_box.centery - font.get_height() // 2, 2, font.get_height())
                pygame.draw.rect(screen, BLACK, cursor_rect)

        # Dessiner les boutons
        button_width = 150
        button_height = 50
        button_x = (screen_width - 2 * button_width - 20) // 2
        pygame.draw.rect(screen, GREEN, (button_x, screen_height - 100, button_width, button_height), border_radius=10)
        pygame.draw.rect(screen, GREEN, (button_x + button_width + 20, screen_height - 100, button_width, button_height), border_radius=10)

        # Texte des boutons
        create_account_text = font.render("Créer un compte", True, BLACK)
        return_text = font.render("Retour", True, BLACK)
        screen.blit(create_account_text, (button_x + (button_width - create_account_text.get_width()) // 2, screen_height - 100 + (button_height - create_account_text.get_height()) // 2))
        screen.blit(return_text, (button_x + button_width + 20 + (button_width - return_text.get_width()) // 2, screen_height - 100 + (button_height - return_text.get_height()) // 2))

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
        # Vérifier si les boutons sont cliqués
        button_width = 150
        button_height = 50
        button_x = (screen_width - 2 * button_width - 20) // 2

        create_account_rect = pygame.Rect(button_x, screen_height - 100, button_width, button_height)
        return_rect = pygame.Rect(button_x + button_width + 20, screen_height - 100, button_width, button_height)

        if create_account_rect.collidepoint(position):
            self.create_account()
        elif return_rect.collidepoint(position):
            self.go_back()
        else:
            # Vérifier si les champs de formulaire sont cliqués
            for name in self.form_data.keys():
                field_rect = pygame.Rect(screen_width // 2 - 200, 300 + list(self.form_data.keys()).index(name) * 50, 400, 40)
                if field_rect.collidepoint(position):
                    self.active_field = name
                    if not self.text_input[name]:
                        self.form_data[name] = ""
                    return
            self.active_field = None

    def create_account(self):
        print("Compte créé avec succès !")

    def go_back(self):
        print("Retour à la page principale")

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.handle_events()
            self.render()
            pygame.display.flip()
            clock.tick(60)
            self.cursor_timer += 1

InscriptionPage().run()
