import pygame
import sys

class MainPage:
    def __init__(self, user):
        self.user = user
        self.transactions = user.transactions

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
        self.GREEN = (0, 100, 0)
        self.RED = (255, 0, 0)

        # Scroll settings
        self.scroll_offset = 0
        self.transactions_per_page = 5

        # Clock
        self.clock = pygame.time.Clock()

    def display_transactions(self):
        # Clear the screen
        self.screen.fill(self.COLOR1)

        # Display account balance
        balance_text = self.font.render(f"Balance: ${self.user.balance}", True, self.BLACK)
        self.screen.blit(balance_text, (self.screen_width / 2 - 50, 20))
        # Display each transaction
        transaction_text = self.font.render("Transactions", True, self.BLACK)
        self.screen.blit(transaction_text, (self.screen_width/2 - transaction_text.get_width()/2, 100))

        visible_transactions = self.transactions[self.scroll_offset:self.scroll_offset+self.transactions_per_page]

        for i, transaction in enumerate(visible_transactions):
            if transaction[5] == "expense" or transaction[5] == "Expense":
                transaction = f"-{transaction[2]}$ : {transaction[0]} ({transaction[1]}) ({transaction[3]}) category: {transaction[4]}"
                text = self.font.render(f"{transaction}", True, self.RED)
            elif transaction[5] == "income" or transaction[5] == "Income":
                transaction = f"+{transaction[2]}$ : {transaction[0]} ({transaction[1]}) ({transaction[3]}) category: {transaction[4]}"
                text = self.font.render(f"{transaction}", True, self.GREEN)
            self.screen.blit(text, (self.screen_width/2 - text.get_width()/2, 130 + i * 30))  # Adjust the position as needed

        # Draw scroll bar
        pygame.draw.rect(self.screen, self.BLACK, (self.screen_width - 20, 130, 10, self.screen_height - 160))
        bar_position = (self.scroll_offset / len(self.transactions)) * (self.screen_height - 160)
        pygame.draw.rect(self.screen, self.WHITE, (self.screen_width - 20, 130 + bar_position, 10, 40))

        # Update the display
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    self.scroll_offset = max(0, self.scroll_offset - 1)
                elif event.button == 5:  # Scroll down
                    self.scroll_offset = min(len(self.transactions) - self.transactions_per_page, self.scroll_offset + 1)

    def run(self):
        while True:
            self.handle_events()
            self.display_transactions()
            self.clock.tick(60)

if __name__ == "__main__":
    main_page = MainPage()
    main_page.run()