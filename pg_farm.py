import pygame
import random

# Initialize pygame
pygame.init()

# Constants
GRID_SIZE = 64
SCREEN_WIDTH = GRID_SIZE * 10
SCREEN_HEIGHT = GRID_SIZE * 8
WHITE = (255, 255, 255)

# Load images for crop stages
crop_images = {
    1: pygame.transform.scale(pygame.image.load('crop_seed.png'), (GRID_SIZE, GRID_SIZE)),    
    2: pygame.transform.scale(pygame.image.load('crop_2.png'), (GRID_SIZE, GRID_SIZE)),    
    3: pygame.transform.scale(pygame.image.load('crop_3.png'), (GRID_SIZE, GRID_SIZE)),    
    4: pygame.transform.scale(pygame.image.load('crop_4.png'), (GRID_SIZE, GRID_SIZE)),    
    5: pygame.transform.scale(pygame.image.load('crop_5.png'), (GRID_SIZE, GRID_SIZE))      # Fully grown crop
}
tile_image = pygame.image.load('tile.png')
tile_image = pygame.transform.scale(tile_image, (GRID_SIZE, GRID_SIZE))
FULLY_GROWN_STAGE = 5

"""
CROP_COLORS = {
    'carrot': (255, 100, 0),
    'wheat': (255, 255, 0),
    'onion': (139, 69, 19)
}
"""
FULLY_GROWN_STAGE = 4

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Farm Game")

# Player's position and character sprite
player_x = GRID_SIZE // 2
player_y = GRID_SIZE // 2
player_speed = 4
player_image = pygame.image.load('character_downview.png')

# Create a list to represent the farm grid
farm_grid = [[None for _ in range(64)] for _ in range(64)]

# Score variable
score = 0

# Function to draw crops
def draw_crop(screen, crop, x, y):
    if crop is not None:
        crop_image = crop_images.get(crop['growth_stage'])
        if crop_image:
            # Scale the image to 60% of its size
            scaled_image = pygame.transform.scale(crop_image, (int(GRID_SIZE * 0.6), int(GRID_SIZE * 0.6)))

            # Calculate the new position to keep the image centered in the grid
            new_x = x + (GRID_SIZE - scaled_image.get_width()) // 2
            new_y = y + (GRID_SIZE - scaled_image.get_height()) // 2

            screen.blit(scaled_image, (new_x, new_y))

"""
# Function to draw crops
def draw_crop(screen, crop, x, y):
    if crop is not None:
        color = CROP_COLORS[crop['crop_type']]
        # Adjust color based on health
        color = tuple(max(0, component - (100 - crop['health'])) for component in color)
        # Adjust size based on growth stage
        size = GRID_SIZE * (0.25 * crop['growth_stage'])
        pygame.draw.rect(screen, color, (x + (GRID_SIZE - size) / 2, y + (GRID_SIZE - size) / 2, size, size))
"""

# Game loop
running = True
clock = pygame.time.Clock()
day_counter = 0  # Counter to simulate day passing

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x = max(0, player_x - player_speed)
    if keys[pygame.K_RIGHT]:
        player_x = min(SCREEN_WIDTH - GRID_SIZE, player_x + player_speed)
    if keys[pygame.K_UP]:
        player_y = max(0, player_y - player_speed)
    if keys[pygame.K_DOWN]:
        player_y = min(SCREEN_HEIGHT - GRID_SIZE, player_y + player_speed)
        
    # Handle planting, watering, and harvesting
    x_index = player_x // GRID_SIZE
    y_index = player_y // GRID_SIZE
    if keys[pygame.K_SPACE]:
        crop_type = 'carrot'  # Change this based on player's choice
        if 0 <= x_index < 64 and 0 <= y_index < 64:
            # Plant a new crop
            if farm_grid[x_index][y_index] is None:
                farm_grid[x_index][y_index] = {
                    'crop_type': crop_type,
                    'health': random.randint(50, 100),
                    'wet': True,
                    'growth_stage': 1
                }

    if keys[pygame.K_TAB]:
        # Water the crop
        if 0 <= x_index < 64 and 0 <= y_index < 64:
            crop = farm_grid[x_index][y_index]
            if crop is not None:
                crop['health'] = min(crop['health'] + 20, 100)
                crop['wet'] = True

    if keys[pygame.K_RETURN]:  # Using Return/Enter key for harvesting
        # Harvest the crop
        if 0 <= x_index < 64 and 0 <= y_index < 64:
            crop = farm_grid[x_index][y_index]
            if crop is not None and crop['growth_stage'] == FULLY_GROWN_STAGE:
                print(f"{crop['crop_type']} harvested: current score: {score}")
                score += 10
                farm_grid[x_index][y_index] = None

    # Day progression logic
    day_counter += 1
    if day_counter >= 180:  # Assuming 1 day = 60 frames for simplicity
        day_counter = 0
        for x, row in enumerate(farm_grid):
            for y, crop in enumerate(row):
                if crop is not None:
                    # Update health and growth stage
                    crop['health'] -= random.randint(10, 20)
                    if not crop['wet']:
                        crop['health'] -= random.randint(10, 20)
                    if crop['health'] < 20:
                        print(f"Crop {crop['crop_type']} at x:{x}, y:{y} has dried up...")
                        farm_grid[x][y] = None
                    elif crop['growth_stage'] < FULLY_GROWN_STAGE and crop['health'] > 50:
                        crop['growth_stage'] = min(crop['growth_stage'] + 1, FULLY_GROWN_STAGE)

    # Draw tiles for each grid cell
    for x in range(64):
        for y in range(64):
            screen.blit(tile_image, (x * GRID_SIZE, y * GRID_SIZE))
    
    # Draw the player character
    screen.blit(player_image, (player_x, player_y))

    # Draw the crops
    for x in range(64):
        for y in range(64):
            draw_crop(screen, farm_grid[x][y], x * GRID_SIZE, y * GRID_SIZE)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(30)

# Quit pygame
pygame.quit()
