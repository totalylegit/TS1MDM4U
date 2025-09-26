import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plinko Game with Pascal's Triangle")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)  # For bar graph

# Font for Pascal's triangle numbers, slot values, and graph labels
font = pygame.font.SysFont('arial', 20)

# Game elements
pegs = []  # List of peg positions (Pascal's Triangle shape)
pascal_values = []  # Store binomial coefficients for each peg
rows = 12  # 12 rows for Pascal's Triangle (row 0 to row 11)
peg_spacing_x = 70
peg_spacing_y = 40
start_y = 120  # Starting y-position for pegs
for row in range(rows):
    num_pegs = row + 1
    y = start_y + row * peg_spacing_y
    row_width = num_pegs * peg_spacing_x
    start_x = (WIDTH - row_width) // 2 + peg_spacing_x // 2  # Center the row
    row_values = []
    for col in range(num_pegs):
        x = start_x + col * peg_spacing_x
        pegs.append((x, y))
        # Calculate binomial coefficient C(row, col)
        value = math.comb(row, col)
        row_values.append(value)
    pascal_values.append(row_values)

# Slots: 10 slots (12 pegs in row 11, remove 1 from each end)
slots = pascal_values[rows - 1][1:-1]  # Row 11 values excluding first/last 1s
slot_counts = [0] * len(slots)  # Track landings in each slot
ball_radius = 10
balls = []  # List of balls, each with x, y, speed_y, direction, dropped, collided_pegs
score = 0
gravity = 0.5  # Gravity for ball physics
bounce = -0.3  # For peg bounces
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Spawn a new ball
                balls.append({
                    'x': WIDTH // 2,
                    'y': 50,
                    'speed_y': 0,
                    'direction': random.choice([-1, 1]),
                    'dropped': True,
                    'collided_pegs': set()
                })

    # Update all balls
    for ball in balls[:]:  # Copy list to allow removal
        if ball['dropped']:
            ball['speed_y'] += gravity
            ball['y'] += ball['speed_y']
            ball['x'] += ball['direction'] * 2  # Horizontal movement

            # Check peg collisions (one per peg per drop, skip row 11)
            peg_index = 0
            for row in range(rows - 1):  # Exclude row 11
                for col in range(row + 1):
                    peg = pegs[peg_index]
                    if peg in ball['collided_pegs']:
                        peg_index += 1
                        continue  # Skip pegs already hit
                    if (ball['x'] - peg[0])**2 + (ball['y'] - peg[1])**2 < (ball_radius + 5)**2:
                        ball['speed_y'] *= bounce
                        ball['direction'] = random.choice([-1, 1])  # Random bounce direction
                        ball['collided_pegs'].add(peg)  # Mark peg as hit
                        peg_index += 1
                        break  # Only one collision per frame
                    peg_index += 1
                else:
                    continue  # Continue outer loop if no break
                break  # Break outer loop if collision occurs

            # Check bottom slots (row 11)
            if ball['y'] > HEIGHT - 20:
                # Get the 12 pegs in row 11
                last_row_pegs = pegs[-len(pascal_values[-1]):]  # 12 pegs
                # Use middle 10 pegs (index 1 to 10)
                slot_pegs = last_row_pegs[1:-1]  # 10 pegs
                # Calculate slot index based on ball_x
                min_x = slot_pegs[0][0] - peg_spacing_x / 2
                max_x = slot_pegs[-1][0] + peg_spacing_x / 2
                if ball['x'] < min_x:
                    slot_index = 0
                elif ball['x'] > max_x:
                    slot_index = len(slots) - 1
                else:
                    slot_index = min(max(int((ball['x'] - min_x) / peg_spacing_x), 0), len(slots) - 1)
                # Update slot count
                slot_counts[slot_index] += 1
                # Score uses 1000 / row 10 Pascal's value
                row_10_value = pascal_values[rows - 2][slot_index + 1]  # Shift by 1 to match slot_pegs
                balls.remove(ball)  # Remove ball after landing

    # Draw everything
    screen.fill(BLACK)
    # Draw pegs and Pascal's triangle values
    peg_index = 0
    for row in range(rows):
        for col in range(row + 1):
            peg = pegs[peg_index]
            # Draw peg (invisible for row 11, visible for others)
            color = BLACK if row == rows - 1 else WHITE
            pygame.draw.circle(screen, color, (int(peg[0]), int(peg[1])), 5)
            # Draw Pascal's triangle value above peg (for row 0 and rows 1 to 10)
            if row < rows - 1:
                value_text = font.render(str(pascal_values[row][col]), True, WHITE)
                text_rect = value_text.get_rect(center=(peg[0], peg[1] - 20))  # 20 pixels above peg
                screen.blit(value_text, text_rect)
            peg_index += 1

    # Draw all balls
    for ball in balls:
        pygame.draw.circle(screen, RED, (int(ball['x']), int(ball['y'])), ball_radius)

    # Draw slots (aligned with middle 10 pegs of row 11)
    last_row_pegs = pegs[-len(pascal_values[-1]):]  # 12 pegs in row 11
    slot_pegs = last_row_pegs[1:-1]  # Middle 10 pegs
    slot_width = peg_spacing_x  # Slot width matches peg spacing
    # Use Pascal's triangle values from row 11 (excluding first and last 1s) for slot display
    row_11_values = pascal_values[rows - 1][1:-1]  # Middle 10 values of row 11
    for i, val in enumerate(row_11_values):
        x = slot_pegs[i][0] - slot_width / 2  # Center slot under peg
        pygame.draw.rect(screen, WHITE, (x, HEIGHT - 50, slot_width, 50), 2)
        # Draw Pascal's triangle value from row 11 centered in slot
        value_text = font.render(str(val), True, WHITE)
        text_rect = value_text.get_rect(center=(x + slot_width / 2, HEIGHT - 25))
        screen.blit(value_text, text_rect)

    # Draw bar graph for slot landings (top-right corner)
    graph_x, graph_y = 550, 20  # Top-right corner
    graph_width, graph_height = 200, 150  # Graph dimensions
    bar_width = 15  # Width of each bar
    bar_spacing = 5  # Space between bars
    max_height = 100  # Max height of bars
    max_count = max(slot_counts, default=1)  # Avoid division by zero
    # Draw graph background
    pygame.draw.rect(screen, BLACK, (graph_x - 5, graph_y - 5, graph_width + 10, graph_height + 30), 2)
    # Draw bars
    for i, count in enumerate(slot_counts):
        bar_height = (count / max_count) * max_height if max_count > 0 else 0
        bar_x = graph_x + i * (bar_width + bar_spacing)
        bar_y = graph_y + max_height - bar_height
        pygame.draw.rect(screen, BLUE, (bar_x, bar_y, bar_width, bar_height))
        # Draw count inside bar (if count > 0)
        if count > 0:
            count_text = font.render(str(count), True, WHITE)
            count_rect = count_text.get_rect(center=(bar_x + bar_width / 2, bar_y + bar_height / 2))
            screen.blit(count_text, count_rect)
        # Draw slot number below bar
        label_text = font.render(str(i + 1), True, WHITE)
        label_rect = label_text.get_rect(center=(bar_x + bar_width / 2, graph_y + max_height + 20))
        screen.blit(label_text, label_rect)
    # Draw graph title
    title_text = font.render("Slot Landings", True, WHITE)
    title_rect = title_text.get_rect(center=(graph_x + graph_width / 2, graph_y - 10))
    screen.blit(title_text, title_rect)
    # Draw y-axis label
    y_label_text = font.render("Count", True, WHITE)
    y_label_rect = y_label_text.get_rect(center=(graph_x - 30, graph_y + max_height / 2))
    screen.blit(y_label_text, y_label_rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()