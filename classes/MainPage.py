import pygame
import sys

class MainPage:
    def __init__(self, transactions=["transaction 1", "transaction 2"], balance=1000):
        self.transactions = transactions
        self.balance = balance

        # Initialize Pygame
        pygame.init()

        # Screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Budget Buddy")

        # Fonts and colors
        self.font = pygame.font.Font(None, 24)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.COLOR1 = (237,190,164)
        self.COLOR2 = (154,208,211)

        # Clock
        self.clock = pygame.time.Clock()

    def render(self):
        # Clear the screen
        self.screen.fill(self.WHITE)

        # Display transactions
        self.display_transactions()

        # Display account balance
        balance_text = self.font.render(f"Balance: ${self.balance}", True, self.BLACK)
        self.screen.blit(balance_text, (self.screen_width / 2 - 50, 20))

        # Update the display
        pygame.display.flip()

    def display_transactions(self):
        # Display each transaction
        for i, transaction in enumerate(self.transactions):
            text = self.font.render(f"{transaction}", True, self.BLACK)
            self.screen.blit(text, (20, 50 + i * 30))  # Adjust the position as needed

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run(self):
        while True:
            self.handle_events()
            self.render()
            self.clock.tick(60)

if __name__ == "__main__":
    main_page = MainPage()
    main_page.run()