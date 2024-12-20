import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Load images
ship_img = pygame.image.load("ship.png")
asteroid_img = pygame.image.load("asteroid.png")
bullet_img = pygame.image.load("bullet.png")
explosion_img = pygame.Surface((50, 50))
explosion_img.fill(RED)

# Resize images
ship_img = pygame.transform.scale(ship_img, (50, 50))
asteroid_img = pygame.transform.scale(asteroid_img, (50, 50))
bullet_img = pygame.transform.scale(bullet_img, (10, 30))

# Player setup
ship = pygame.Rect(WIDTH // 2, HEIGHT - 100, 50, 50)
ship_speed = 5
health = 100

# Bullet setup
bullets = []
bullet_speed = -10

# Enemy shooter setup
enemy_bullets = []
enemy_bullet_speed = 3  # Slower enemy bullet speed

# Asteroid setup
asteroids = []
asteroid_speed = 3
for _ in range(5):
    x = random.randint(0, WIDTH - 50)
    y = random.randint(-150, -50)
    asteroids.append(pygame.Rect(x, y, 50, 50))

# Score and Level setup
score = 0
level = 1
font = pygame.font.Font(None, 36)

# Game loop
clock = pygame.time.Clock()

def draw():
    screen.fill(BLACK)
    screen.blit(ship_img, (ship.x, ship.y))
    for bullet in bullets:
        screen.blit(bullet_img, (bullet.x, bullet.y))
    for asteroid in asteroids:
        screen.blit(asteroid_img, (asteroid.x, asteroid.y))
    for enemy_bullet in enemy_bullets:
        pygame.draw.rect(screen, RED, enemy_bullet)
    health_text = font.render(f"Health: {health}", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(health_text, (10, 10))
    screen.blit(score_text, (10, 40))
    screen.blit(level_text, (10, 70))
    pygame.display.flip()

def move_asteroids():
    global health
    for asteroid in asteroids:
        asteroid.y += asteroid_speed
        if asteroid.y > HEIGHT:
            asteroid.y = random.randint(-150, -50)
            asteroid.x = random.randint(0, WIDTH - 50)
        if ship.colliderect(asteroid):
            health -= 25
            asteroid.y = random.randint(-150, -50)
            asteroid.x = random.randint(0, WIDTH - 50)

def check_collisions():
    global score, level
    for bullet in bullets[:]:
        for asteroid in asteroids[:]:
            if bullet.colliderect(asteroid):
                bullets.remove(bullet)
                asteroids.remove(asteroid)
                asteroids.append(pygame.Rect(random.randint(0, WIDTH - 50), random.randint(-150, -50), 50, 50))
                score += 1
                if score % 5 == 0:
                    level_up()

    for enemy_bullet in enemy_bullets[:]:
        if enemy_bullet.colliderect(ship):
            health -= 10
            enemy_bullets.remove(enemy_bullet)

def level_up():
    global level, asteroid_speed, enemy_bullet_speed
    level += 1
    asteroid_speed += 1
    enemy_bullet_speed += 0.5  # Slower increment for enemy bullet speed
    for _ in range(level):
        x = random.randint(0, WIDTH - 50)
        y = random.randint(-150, -50)
        asteroids.append(pygame.Rect(x, y, 50, 50))

def fire_enemy_bullets():
    if random.randint(1, 100) < 5 + level:  # Increase chance to fire with level
        x = random.randint(0, WIDTH - 50)
        enemy_bullets.append(pygame.Rect(x, random.randint(-150, -50), 10, 30))

# Retry or Exit Button
def game_over():
    global running
    retry_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    exit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 50)

    pygame.draw.rect(screen, BLUE, retry_button)
    pygame.draw.rect(screen, RED, exit_button)

    font = pygame.font.Font(None, 36)
    retry_text = font.render("Retry", True, WHITE)
    exit_text = font.render("Exit", True, WHITE)

    screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + 10))
    screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 70))

    pygame.display.flip()

    return retry_button, exit_button

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and ship.x > 0:
        ship.x -= ship_speed
    if keys[pygame.K_d] and ship.x < WIDTH - 50:
        ship.x += ship_speed
    if keys[pygame.K_w] and ship.y > 0:
        ship.y -= ship_speed
    if keys[pygame.K_s] and ship.y < HEIGHT - 50:
        ship.y += ship_speed
    if keys[pygame.K_SPACE]:
        if len(bullets) < 5:
            bullets.append(pygame.Rect(ship.x + 20, ship.y, 10, 30))

    # Move bullets
    for bullet in bullets[:]:
        bullet.y += bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

    # Move enemy bullets
    for enemy_bullet in enemy_bullets[:]:
        enemy_bullet.y += enemy_bullet_speed
        if enemy_bullet.y > HEIGHT:
            enemy_bullets.remove(enemy_bullet)

    # Move asteroids and check collisions
    move_asteroids()
    check_collisions()
    fire_enemy_bullets()

    # Game over check
    if health <= 0:
        print("Game Over")
        retry_button, exit_button = game_over()
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting_for_input = False
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if retry_button.collidepoint(mouse_x, mouse_y):
                        # Reset game state
                        health = 100
                        score = 0
                        level = 1
                        asteroids.clear()
                        for _ in range(5):
                            x = random.randint(0, WIDTH - 50)
                            y = random.randint(-150, -50)
                            asteroids.append(pygame.Rect(x, y, 50, 50))
                        waiting_for_input = False
                    elif exit_button.collidepoint(mouse_x, mouse_y):
                        waiting_for_input = False
                        running = False

    draw()

pygame.quit()
sys.exit()
