import pygame
import sys



class Registration:
    def __init__(self):

        pygame.init()

        # Paramètres de l'écran
        self.screen_width = 600
        self.screen_height = 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Chargement de l'image de fond
        self.bacjground_image = pygame.image.load('images/inscription.png')
        self.bacjground_image = pygame.transform.scale(self.bacjground_image, (self.screen_width, self.screen_height))

        # Couleurs
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (154, 208, 211)  # Couleur des boutons
        self.BUTTON_TEXT_COLOR = self.BLACK  # Couleur du texte des boutons
        self.TEXT_INPUT_COLOR = (237, 190, 164)  # Couleur des cases de saisie
        self.TEXT_INPUT_BORDER_COLOR = (232, 143, 122)  # Couleur de la bordure des cases de saisie
        self.TEXT_INPUT_BORDER_WIDTH = 2  # Épaisseur de la bordure des cases de saisie

        # Police de caractère
        self.font = pygame.font.Font("images/survivant.ttf", 20)  # Utilisation de la police Bobby Jones

        self.form_data = {"Lastname": "", "Firstname": "", "Email": "", "Password": "", "Confirm Password": ""}
        self.active_field = None
        self.text_input = {name: False for name in self.form_data.keys()}
        self.cursor_timer = 0
        self.input_box_offset_y = 30  # Décalage vertical des cases de saisie

    def render(self):
        # Affichage de l'image de fond
        self.screen.blit(self.bacjground_image, (0, 0))

        # Dessiner les champs de formulaire
        for i, (name, text) in enumerate(self.form_data.items()):
            background = self.TEXT_INPUT_COLOR if self.active_field == name else self.WHITE
            input_box = pygame.Rect(self.screen_width // 2 - 200, 300 + i * 50 + self.input_box_offset_y, 400, 40)
            pygame.draw.rect(self.screen, background, input_box, border_radius=10)  # Border radius ajouté ici
            pygame.draw.rect(self.screen, self.TEXT_INPUT_BORDER_COLOR, input_box, self.TEXT_INPUT_BORDER_WIDTH, border_radius=10)  # Bordure de la case de saisie
            if text == "" and not self.text_input[name]:
                text_surface = self.font.render(f"{name}: ", True, self.BLACK)
                self.screen.blit(text_surface, (input_box.left + 10, input_box.centery - text_surface.get_height() // 2))
            else:
                text_surface = self.font.render(f"{text}", True, self.BLACK)
                self.screen.blit(text_surface, (input_box.left + 10, input_box.centery - text_surface.get_height() // 2))

            # Dessiner le curseur
            if self.active_field == name and self.cursor_timer % 60 < 30:
                cursor_rect = pygame.Rect(input_box.left + 10 + text_surface.get_width(), input_box.centery - self.font.get_height() // 2, 2, self.font.get_height())
                pygame.draw.rect(self.screen, self.BLACK, cursor_rect)

        # Dessiner les boutons
        button_width = 150
        button_height = 50
        button_x = (self.screen_width - 2 * button_width - 20) // 2
        pygame.draw.rect(self.screen, self.GREEN, (button_x, self.screen_height - 100, button_width, button_height), border_radius=10)
        pygame.draw.rect(self.screen, self.GREEN, (button_x + button_width + 20, self.screen_height - 100, button_width, button_height), border_radius=10)

        # Texte des boutons
        create_account_text = self.font.render("Inscription", True, self.BUTTON_TEXT_COLOR)
        return_text = self.font.render("Retour", True, self.BUTTON_TEXT_COLOR)
        self.screen.blit(create_account_text, (button_x + (button_width - create_account_text.get_width()) // 2, self.screen_height - 100 + (button_height - create_account_text.get_height()) // 2))
        self.screen.blit(return_text, (button_x + button_width + 20 + (button_width - return_text.get_width()) // 2, self.screen_height - 100 + (button_height - return_text.get_height()) // 2))

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
        button_x = (self.screen_width - 2 * button_width - 20) // 2

        create_account_rect = pygame.Rect(button_x, self.screen_height - 100, button_width, button_height)
        return_rect = pygame.Rect(button_x + button_width + 20, self.screen_height - 100, button_width, button_height)

        if create_account_rect.collidepoint(position):
            self.create_account()
        elif return_rect.collidepoint(position):
            self.go_back()
        else:
            # Vérifier si les champs de formulaire sont cliqués
            for name in self.form_data.keys():
                field_rect = pygame.Rect(self.screen_width // 2 - 200, 300 + list(self.form_data.keys()).index(name) * 50 + self.input_box_offset_y, 400, 40)
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

Registration().run()
