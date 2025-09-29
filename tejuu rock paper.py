import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 840, 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 100, 200)

# Fonts
font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 60)

# Game variables
choices = ["Rock", "Paper", "Scissors"]
player_score = 0
computer_score = 0
max_score = 3  # Best of 3 by default

# Utility functions
def draw_text(text, x, y, color=BLACK, center=False, big=False):
    f = big_font if big else font
    img = f.render(text, True, color)
    if center:
        rect = img.get_rect(center=(x, y))
        screen.blit(img, rect)
    else:
        screen.blit(img, (x, y))

def draw_button(text, x, y, w, h, color=GRAY):
    pygame.draw.rect(screen, color, (x, y, w, h))
    draw_text(text, x + w // 2, y + h // 2, BLACK, center=True)

def get_winner(player, computer):
    if player == computer:
        return "Tie"
    elif (player == "Rock" and computer == "Scissors") or \
         (player == "Paper" and computer == "Rock") or \
         (player == "Scissors" and computer == "Paper"):
        return "Player"
    else:
        return "Computer"

def draw_health_bar(x, y, score):
    bar_width = 200
    filled = (score / max_score) * bar_width
    pygame.draw.rect(screen, RED, (x, y, bar_width, 20))
    pygame.draw.rect(screen, GREEN, (x, y, filled, 20))

def reset_game():
    global player_score, computer_score, result, player_choice, computer_choice
    player_score = 0
    computer_score = 0
    result = ""
    player_choice = ""
    computer_choice = ""

# Main loop
running = True
result = ""
player_choice = ""
computer_choice = ""
game_over = False

# Game mode selection
selecting_mode = True
while selecting_mode:
    screen.fill(WHITE)
    draw_text("Select Game Mode (Best of ...)", WIDTH // 2, 100, BLUE, center=True, big=True)
    draw_button("3", 200, 200, 100, 60)
    draw_button("5", 370, 200, 100, 60)
    draw_button("7", 540, 200, 100, 60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if 200 <= mx <= 300 and 200 <= my <= 260:
                max_score = 3
                selecting_mode = False
            elif 370 <= mx <= 470 and 200 <= my <= 260:
                max_score = 5
                selecting_mode = False
            elif 540 <= mx <= 640 and 200 <= my <= 260:
                max_score = 7
                selecting_mode = False

    pygame.display.update()

# Gameplay loop
while running:
    screen.fill(WHITE)

    draw_text("Rock Paper Scissors", WIDTH // 2, 30, BLUE, center=True, big=True)

    draw_button("Rock", 150, 100, 150, 60)
    draw_button("Paper", 350, 100, 150, 60)
    draw_button("Scissors", 550, 100, 150, 60)

    draw_text(f"Your Choice: {player_choice}", 50, 200)
    draw_text(f"Computer: {computer_choice}", 50, 250)
    draw_text(f"Result: {result}", 50, 300)

    draw_text("Player HP", 50, 400)
    draw_health_bar(210, 405, player_score)

    draw_text("Computer HP", 410, 400)
    draw_health_bar(600, 405, computer_score)

    if game_over:
        draw_text("Game Over!", WIDTH // 2, 350, RED, center=True, big=True)
        draw_button("Restart", WIDTH // 2 - 75, 400, 150, 60, color=GREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if 150 <= mx <= 300 and 100 <= my <= 160:
                player_choice = "Rock"
            elif 350 <= mx <= 500 and 100 <= my <= 160:
                player_choice = "Paper"
            elif 550 <= mx <= 700 and 100 <= my <= 160:
                player_choice = "Scissors"
            else:
                continue

            computer_choice = random.choice(choices)
            winner = get_winner(player_choice, computer_choice)

            if winner == "Player":
                result = "You Win!"
                player_score += 1
            elif winner == "Computer":
                result = "You Lose!"
                computer_score += 1
            else:
                result = "It's a Tie!"

            if player_score == max_score or computer_score == max_score:
                game_over = True

        elif game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if WIDTH // 2 - 75 <= mx <= WIDTH // 2 + 75 and 400 <= my <= 460:
                reset_game()
                game_over = False

    pygame.display.update()

pygame.quit()
sys.exit()
