import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plinko Game with Modifiers")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Game elements
pegs = []  # List of peg positions
for row in range(10):  # Create peg grid
    for col in range(11):
        x = 50 + col * 70 + (row % 2) * 35  # Staggered rows
        y = 100 + row * 50
        pegs.append((x, y))

slots = [100, 200, 500, 1000, 500, 200, 100]  # Bottom slot values
ball_radius = 10
ball_x, ball_y = WIDTH // 2, 50  # Starting position
ball_speed_y = 0
gravity = 0.5
bounce = -0.3  # For peg bounces
direction = random.choice([-1, 1])  # Initial left/right bias
score = 0
modifier = 1  # Start with 1x multiplier; can randomize or user-set

running = True
dropped = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not dropped:
                dropped = True  # Drop the ball

    # Update ball if dropped
    if dropped:
        ball_speed_y += gravity
        ball_y += ball_speed_y
        ball_x += direction * 2  # Horizontal movement

        # Check peg collisions
        for peg in pegs:
            if (ball_x - peg[0])**2 + (ball_y - peg[1])**2 < (ball_radius + 5)**2:
                ball_speed_y *= bounce
                direction = random.choice([-1, 1])  # Random bounce

        # Check bottom slots
        if ball_y > HEIGHT - 20:
            slot_index = min(max(int((ball_x / WIDTH) * len(slots)), 0), len(slots) - 1)
            score += slots[slot_index] * modifier
            print(f"Score: {score}")  # Or display on screen
            dropped = False  # Reset for next drop
            ball_x, ball_y = WIDTH // 2, 50
            ball_speed_y = 0
            modifier = random.choice([1, 2, 0.5])  # Random modifier for next round

    # Draw everything
    screen.fill(BLACK)
    for peg in pegs:
        pygame.draw.circle(screen, WHITE, peg, 5)
    if dropped or not dropped:
        pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)
    # Draw slots (add text for values)
    for i, val in enumerate(slots):
        pygame.draw.rect(screen, WHITE, (i * (WIDTH / len(slots)), HEIGHT - 50, WIDTH / len(slots), 50), 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
