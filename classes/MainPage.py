import pygame

pygame.init()

class MainPage:
    def __init__(self):
        self.screen_width = 500
        self.screen_height = 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.font = pygame.font.Font(None, 20)
        self.screen.fill((255, 255, 255))

        self.title_font = pygame.font.Font(None, 40)
        self.title_text = self.title_font.render("Main Page", True, (0, 0, 0))
        self.title_text_rect = self.title_text.get_rect(center=(self.screen_width // 2, 50))
        self.screen.blit(self.title_text, self.title_text_rect)
        self.clock = pygame.time.Clock()
        self.cursor_timer = 0



        

    def run(self):
        pygame.display.flip()
        self.clock.tick(60)
        self.cursor_timer += 1
        
accueil = MainPage()

while True:
    accueil.run()