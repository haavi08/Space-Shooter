import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Creating the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Title and Icon
pygame.display.set_caption("Space Shooter")
icon = pygame.image.load("ufo.png") 
pygame.display.set_icon(icon)

# Loading player image and position
player_img = pygame.image.load("spaceship.png")  
player_x = 370
player_y = 480
player_x_change = 0

# alien
alien_img = []
alien_x = []
alien_y = []
alien_x_change = []
alien_y_change = []
num_of_enemies = 6

def init_enemies():
    for i in range(num_of_enemies):
        alien_img.append(pygame.image.load("alien.png")) 
        alien_x.append(random.randint(0, 736))
        alien_y.append(random.randint(50, 150))
        alien_x_change.append(1)
        alien_y_change.append(20)

# Loading bullet image and position
bullet_img = pygame.image.load("bullet.png") 
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

#when player chooses to reset game
def reset_game():
    global player_x, player_x_change, bullet_x, bullet_y, bullet_state, score_value, start_ticks
    player_x = 370
    player_x_change = 0
    bullet_x = 0
    bullet_y = 480
    bullet_state = "ready"
    score_value = 0
    start_ticks = pygame.time.get_ticks()
    alien_img.clear()
    alien_x.clear()
    alien_y.clear()
    alien_x_change.clear()
    alien_y_change.clear()
    init_enemies()

#score
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

#high score
def show_high_score(x, y):
    high_score_display = font.render("High Score : " + str(high_score), True, (255, 255, 255))
    screen.blit(high_score_display, (x, y))

#timer
def show_timer(x, y, time_left):
    timer = font.render("Time : " + str(time_left), True, (255, 255, 255))
    screen.blit(timer, (x, y))

#game over
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

#restart
def restart_text():
    restart_msg = font.render("Press 'R' to Restart", True, (255, 255, 255))
    screen.blit(restart_msg, (250, 320))

def player(x, y):
    screen.blit(player_img, (x, y))

def alien(x, y, i):
    screen.blit(alien_img[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 43, y + 10))

def is_collision(alien_x, alien_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(alien_x - bullet_x, 2) + math.pow(alien_y - bullet_y, 2))
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

        # alien Movement
        for i in range(num_of_enemies):
            # Game Over if alien reaches below certain point
            if alien_y[i] > 440:
                game_over = True
                break

            alien_x[i] += alien_x_change[i]
            if alien_x[i] <= 0:
                alien_x_change[i] = 1
                alien_y[i] += alien_y_change[i]
            elif alien_x[i] >= 736:
                alien_x_change[i] = -1
                alien_y[i] += alien_y_change[i]

            # Collision
            collision = is_collision(alien_x[i], alien_y[i], bullet_x, bullet_y)
            if collision:
                bullet_y = 480
                bullet_state = "ready"
                score_value += 1
                alien_x[i] = random.randint(0, 736)
                alien_y[i] = random.randint(50, 150)

            alien(alien_x[i], alien_y[i], i)

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
