import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Create the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")  # Replace with your own icon
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load("spaceship.png")  # Replace with your own player image
player_x = 370
player_y = 480
player_x_change = 0

# alien2
alien2_img = []
alien2_x = []
alien2_y = []
alien2_x_change = []
alien2_y_change = []
num_of_enemies = 6

def init_enemies():
    for i in range(num_of_enemies):
        alien2_img.append(pygame.image.load("alien2.png"))  # Replace with your own alien2 image
        alien2_x.append(random.randint(0, 736))
        alien2_y.append(random.randint(50, 150))
        alien2_x_change.append(1)
        alien2_y_change.append(20)

# Bullet
bullet_img = pygame.image.load("bullet.png")  # Replace with your own bullet image
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"

# Score
score_value = 0
high_score = 0  # Initialize the high score
font = pygame.font.Font('freesansbold.ttf', 32)

text_x = 10
text_y = 10

# Timer
start_ticks = pygame.time.get_ticks()  # Start counting ticks

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def reset_game():
    global player_x, player_x_change, bullet_x, bullet_y, bullet_state, score_value, start_ticks
    player_x = 370
    player_x_change = 0
    bullet_x = 0
    bullet_y = 480
    bullet_state = "ready"
    score_value = 0
    start_ticks = pygame.time.get_ticks()
    alien2_img.clear()
    alien2_x.clear()
    alien2_y.clear()
    alien2_x_change.clear()
    alien2_y_change.clear()
    init_enemies()

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def show_high_score(x, y):
    high_score_display = font.render("High Score : " + str(high_score), True, (255, 255, 255))
    screen.blit(high_score_display, (x, y))

def show_timer(x, y, time_left):
    timer = font.render("Time : " + str(time_left), True, (255, 255, 255))
    screen.blit(timer, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def restart_text():
    restart_msg = font.render("Press 'R' to Restart", True, (255, 255, 255))
    screen.blit(restart_msg, (250, 320))

def player(x, y):
    screen.blit(player_img, (x, y))

def alien2(x, y, i):
    screen.blit(alien2_img[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 43, y + 10))

def is_collision(alien2_x, alien2_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(alien2_x - bullet_x, 2) + math.pow(alien2_y - bullet_y, 2))
    return distance < 27

# Initialize enemies
init_enemies()

# Game Loop
running = True
game_over = False

while running:

    # RGB - Red, Green, Blue
    screen.fill((0, 0, 0))  # Black background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over:
            # If keystroke is pressed check whether it's right or left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_x_change = -1
                if event.key == pygame.K_RIGHT:
                    player_x_change = 1
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bullet_x = player_x
                        fire_bullet(bullet_x, bullet_y)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_x_change = 0
        else:
            # Check if the player presses 'R' to restart the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_game()
                game_over = False

    if not game_over:
        # Player Movement
        player_x += player_x_change
        if player_x <= 0:
            player_x = 0
        elif player_x >= 736:
            player_x = 736

        # alien2 Movement
        for i in range(num_of_enemies):
            # Game Over if alien2 reaches below certain point
            if alien2_y[i] > 440:
                game_over = True
                break

            alien2_x[i] += alien2_x_change[i]
            if alien2_x[i] <= 0:
                alien2_x_change[i] = 1
                alien2_y[i] += alien2_y_change[i]
            elif alien2_x[i] >= 736:
                alien2_x_change[i] = -1
                alien2_y[i] += alien2_y_change[i]

            # Collision
            collision = is_collision(alien2_x[i], alien2_y[i], bullet_x, bullet_y)
            if collision:
                bullet_y = 480
                bullet_state = "ready"
                score_value += 1
                alien2_x[i] = random.randint(0, 736)
                alien2_y[i] = random.randint(50, 150)

            alien2(alien2_x[i], alien2_y[i], i)

        # Bullet Movement
        if bullet_y <= 0:
            bullet_y = 480
            bullet_state = "ready"
        if bullet_state == "fire":
            fire_bullet(bullet_x, bullet_y)
            bullet_y -= bullet_y_change

        # Timer
        seconds = 60 - (pygame.time.get_ticks() - start_ticks) // 1000
        if seconds <= 0:
            game_over = True

        player(player_x, player_y)
        show_score(text_x, text_y)
        show_high_score(text_x, text_y + 40)  # Display the high score below the current score
        show_timer(screen_width - 150, text_y, seconds)

    if game_over:
        # Update the high score if the current score is greater
        if score_value > high_score:
            high_score = score_value
        game_over_text()
        restart_text()

    pygame.display.update()
