import pygame
import sys

class Interface:
    def __init__(self):
        self.form_data = {"Lastname": "", "Firstname": "", "Email": "", "Password": ""}
        self.active_field = None
        self.text_input = {name: False for name in self.form_data.keys()}
        self.cursor_timer = 0
        self.y_offset = 150  # Décalage supplémentaire pour placer les éléments un peu plus haut

        pygame.init()

        # Paramètres de l'écran
        self.screen_width = 500
        self.screen_height = 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Chargez l'image de fond
        self.background_image = pygame.image.load("images/Login.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))  # Redimensionnez l'image

        # Couleurs
        self.WHITE = (237, 190, 164)  # Couleur des cases d'écriture avant clic #EDBEA4
        self.BLACK = (0, 0, 0)
        self.GREY = (200, 200, 200)
        self.WHITE_GREY = (220, 220, 220)
        self.BUTTON_COLOR = (154, 208, 211)  # Couleur des boutons #9AD0D3
        self.BUTTON_TEXT_COLOR = self.BLACK
        # Police de caractère
        self.font = pygame.font.Font("images/survivant.ttf", 16)

        # Calcul de la position verticale de la dernière boîte de texte
        last_input_box_y = self.y_offset + 200 + (len(self.form_data) - 1) * 50

        # Coordonnées des boutons de connexion et d'inscription
        self.connexion_button = pygame.Rect(self.screen_width // 2 + 50, last_input_box_y + 50, 200, 40)  # Bouton Connexion
        self.inscription_button = pygame.Rect(self.screen_width // 2 - 250, last_input_box_y + 50, 200, 40)  # Bouton Inscription
        self.login_attempt = False
        self.message_text = None  # Track the error message text
        self.message_timer = 0     # Timer to control the duration of error message display
        self.message_duration = 2000  # Duration to display the error message in milliseconds

    def render(self):
        # Dessiner l'image de fond
        self.screen.blit(self.background_image, (0, 0))

        for i, (name, text) in enumerate(self.form_data.items()):
            background = self.WHITE if self.active_field == name else self.GREY
            input_box = pygame.Rect(self.screen_width // 2 - 200, self.y_offset + 200 + i*50, 400, 40)  # Utilisation du décalage
            pygame.draw.rect(self.screen, background, input_box, border_radius=10)  # Coins arrondis
            if text == "" and not self.text_input[name]:
                text_surface = self.font.render(f"{name}: ", True, self.BLACK)
            else:
                text_surface = self.font.render(f"{text}", True, self.BLACK)
            self.screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
            if self.active_field == name and self.cursor_timer % 60 < 30:
                cursor_rect = pygame.Rect(input_box.x + self.font.size(text)[0] + 5, input_box.y + 5, 2, self.font.get_height())
                pygame.draw.rect(self.screen, self.BLACK, cursor_rect)
            # Ajout d'une bordure si le champ est actif
            if self.active_field == name:
                pygame.draw.rect(self.screen, self.BUTTON_COLOR, input_box, 2)

        # Affichage des boutons de connexion et d'inscription avec des effets visuels
        pygame.draw.rect(self.screen, self.BUTTON_COLOR, self.connexion_button, border_radius=5)  # Bouton Connexion
        pygame.draw.rect(self.screen, self.BUTTON_COLOR, self.inscription_button, border_radius=5)  # Bouton Inscription
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
            field_rect = pygame.Rect(self.screen_width // 2 - 200, self.y_offset + 200 + list(self.form_data.keys()).index(name) * 50, 400, 40)  # Utilisation du décalage
            if field_rect.collidepoint(position):
                self.active_field = name
                if not self.text_input[name]:
                    self.form_data[name] = ""
                return
        self.active_field = None
        if self.connexion_button.collidepoint(position):
            self.login_attempt = True
        elif self.inscription_button.collidepoint(position):
            self.get_identifier()
        
    def get_identifier(self):
        return self.form_data
    
    def message(self, message):
        self.message_text = self.font.render(message, True, self.BLACK)
        self.message_timer = pygame.time.get_ticks()  # Start the timer

    

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.handle_events()
            self.render()
            pygame.display.flip()
            clock.tick(60)
            self.cursor_timer += 1